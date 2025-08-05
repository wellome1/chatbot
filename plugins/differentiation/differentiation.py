from pluginBase import Plugin
import cmath

# Highest Level
class Math:
    pass

# Atoms
class Atom(Math):
    def __init__(self,value):
        self.value = value

class Constant(Atom):
    def __init__(self,value):
        super().__init__(value)

    def differentiate(self):
        return Constant(0)

class Variable(Atom):
    def __init__(self,value):
        super().__init__(value)

    def differentiate(self):
        # Assume no power
        return Constant(1)

# Binary Operations
class BinaryOperator(Math):
    def __init__(self, a, b, operator):
        self.left = a
        self.right = b
        self.operator = operator

    def makeConstant(self):
        if isinstance(self.left, Constant) and isinstance(self.right, Constant):
            match self.operator:
                case "+":
                    return Constant(self.left.value + self.right.value)
                case "-":
                    return Constant(self.left.value - self.right.value)
                case "*":
                    return Constant(self.left.value * self.right.value)
                case "/":
                    return Constant(self.left.value / self.right.value)
                case "**":
                    return Constant(self.left.value ** self.right.value)
                case _:
                    raise ValueError("Invalid operator.")
        else:
            return None

    def differentiate(self):
        pass

class Addition(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "+")

    def __str__(self):
        return f"{self.left} + {self.right}"

class Subtraction(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "-")

    def __str__(self):
        return f"{self.left} - {self.right}"

class Multiplication(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "*")

    def __str__(self):
        return f"{self.left} * {self.right}"

    def differentiate(self):
        f = self.left
        g = self.right

        fDiff = f.differentiate()
        gDiff = g.differentiate()

        return Addition(Multiplication(f,gDiff), Multiplication(g,fDiff))

class Division(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "/")

    def __str__(self):
        return f"{self.left} / {self.right}"

    def differentiate(self):
        f = self.left
        g = self.right

        fDiff = f.differentiate()
        gDiff = g.differentiate()

        numerator = Subtraction(Multiplication(g, fDiff), Multiplication(f, gDiff))
        denominator = Power(g, Constant(2))

        return Division(numerator, denominator)

class Power(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "**")

    def __str__(self):
        return f"{self.left} ** {self.right}"

    def differentiate(self):
        base = self.left
        exponent = self.right

        if isinstance(exponent, Constant):
            newExponent = Constant(exponent.value - 1)
            outer = Multiplication(exponent, Power(base, newExponent))
            inner = base.differentiate()
            return Multiplication(outer, inner)

        return Constant(0) # Both are constants, therefore, it differentiates to 0.

# Unary Functions
class UnaryFunction(Math):
    def __init__(self, operand, name=None):
        self.operand = operand
        self.name = name

    def __str__(self):
        return f"{self.name}({self.operand})"

class Log(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "log")

class Exp(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "exp")

class Negation(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "-")

class Parentheses(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand)

    def __str__(self):
        return f"({self.operand})"

class Function(UnaryFunction):
    def __init__(self,operand, name="f"):
        super().__init__(operand, name)

## Trig Functions
class TrigFunction(UnaryFunction):
    def __init__(self,operand,name=None):
        super().__init__(operand, name)

class Sin(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "sin")

class Cos(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "cos")

class Tan(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "tan")

class Csc(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "csc")

class Sec(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "sec")

class Cot(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "cot")

### Inverse Trig Functions
class InverseTrigFunc(TrigFunction):
    pass

class Arcsin(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arcsin")

class Arccos(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arccos")

class Arctan(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arctan")

# Simplification
class Simplify:
    @staticmethod
    def simplify(node):
        if isinstance(node, BinaryOperator):
            node.left = Simplify.simplify(node.left)
            node.right = Simplify.simplify(node.right)

            folded = node.makeConstant()
            if folded:
                return folded

            if node.operator == "+":
                if isinstance(node.left, Constant) and node.left.value == 0:
                    return node.right
                elif isinstance(node.right, Constant) and node.right.value == 0:
                    return node.left

            if node.operator == "*":
                if (isinstance(node.left, Constant) and node.left.value == 0) or (isinstance(node.right, Constant) and node.right.value == 0):
                    return Constant(0)

                if isinstance(node.left, Constant) and node.left.value == 1:
                    return node.right
                elif isinstance(node.right, Constant) and node.right.value == 1:
                    return node.left

            return node

        elif isinstance(node, UnaryFunction):
            node.operand = Simplify.simplify(node.operand)
            return node

        else:
            return node