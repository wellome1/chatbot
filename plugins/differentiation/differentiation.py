from pluginBase import Plugin

# Highest Level
class Math:
    pass

# Atoms
class Atom(Math):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Constant(Atom):
    def __init__(self,value):
        super().__init__(value)

    def differentiate(self):
        return Constant(0)

class Variable(Atom):
    def __init__(self,value):
        super().__init__(value)

    def differentiate(self):
        # Assume no power if it got here.
        return Constant(1)

# MathTerms
class MathTerms(Atom):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"{self.value}"

    def differentiate(self):
        return Constant(0)

class Pi(MathTerms):
    def __init__(self):
        super().__init__(Division(22, 7))

    def __str__(self):
        return "π"

class E(MathTerms):
    def __init__(self):
        super().__init__(2.71828)

    def __str__(self):
        return "e"

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

    def differentiate(self):
        return Addition(self.left.differentiate(), self.right.differentiate())

class Subtraction(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "-")

    def __str__(self):
        return f"{self.left} - {self.right}"

    def differentiate(self):
        return Subtraction(self.left.differentiate(), self.right.differentiate())

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

    def differentiate(self):
        return Division(self.operand.differentiate(), self.operand)

class Ln(UnaryFunction):
    def __init__(self, operand):
        super().__init__(operand, "ln")

    def differentiate(self):
        return Division(self.operand.differentiate(), self.operand)

class Exp(UnaryFunction):
    def __init__(self,operand):
        self.operand = Power(E, operand)
        super().__init__(operand, "exp")

    def differentiate(self):
        return Multiplication(self, self.operand.differentiate())

class Negation(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "-")

    def differentiate(self):
        return Negation(self.operand.differentiate())

class Parentheses(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand)

    def __str__(self):
        return f"({self.operand})"

class Function(UnaryFunction):
    def __init__(self,operand, name="f"):
        super().__init__(operand, name)

class Sqrt(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "sqrt")

    def isPerfectSquare(self):
        n = self.operand

        if n < 0:
            return False

        z = n
        y = (z + 1) // 2

        while y < z:
            z = y
            y = (z + n // z) // 2

        return z * z == n

    def intSqrt(self):
        n = self.operand.value

        if n < 0:
            raise ValueError("Cannot sqrt negative numbers.")

        z = n
        y = (z+1) // 2
        while y < z:
            z = y
            y = (z + n // z) // 2

        return Constant(z) if z * z == n else None

    def differentiate(self):
        return Division(1, Multiplication(2, Sqrt(self.operand)))

class Abs(UnaryFunction):
    def __init__(self,operand):
        if isinstance(operand, Negation):
            operand = Constant(operand.operand)

        super().__init__(operand)

    def __str__(self):
        return f"|{self.operand}|"

## Trig Functions
class TrigFunction(UnaryFunction):
    def __init__(self,operand,name=None):
        super().__init__(operand, name)

class Sin(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "sin")
        self.x = self.operand

    def differentiate(self):
        inner = Cos(self.x)
        outer = self.x.differentiate()
        return Multiplication(inner, outer)

class Cos(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "cos")
        self.x = self.operand

    def differentiate(self):
        inner = Negation(Sin(self.x))
        outer = self.x.differentiate()
        return Multiplication(outer, inner)

class Tan(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "tan")
        self.x = self.operand

    def differentiate(self):
        inner = Power(Sec(self.x), Constant(2))
        outer = self.x.differentiate()
        return Multiplication(outer, inner)

class Csc(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "csc")
        self.x = self.operand

    def differentiate(self):
        inner = Negation(Multiplication(Csc(self.x), Cot(self.x)))
        outer = self.x.differentiate()
        return Multiplication(inner, outer)

class Sec(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "sec")
        self.x = self.operand

    def differentiate(self):
        inner = Multiplication(Sec(self.x), Tan(self.x))
        outer = self.x.differentiate()
        return Multiplication(outer, inner)

class Cot(TrigFunction):
    def __init__(self, operand):
        super().__init__(operand, "cot")
        self.x = self.operand

    def differentiate(self):
        inner = Negation(Power(Csc(self.x), Constant(2)))
        outer = self.x.differentiate()
        return Multiplication(outer, inner)

### Inverse Trig Functions
class InverseTrigFunc(TrigFunction):
    pass

class Arcsin(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arcsin")
        self.x = self.operand

    def differentiate(self):
        numerator = self.x.differentiate()
        denominator = Sqrt(Subtraction(Constant(1), Power(self.x, Constant(2))))
        return Division(numerator, denominator)

class Arccos(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arccos")
        self.x = self.operand

    def differentiate(self):
        numerator = Negation(self.x.differentiate())
        denominator = Sqrt(Subtraction(Constant(1), Power(self.x, Constant(2))))
        return Division(numerator, denominator)

class Arctan(InverseTrigFunc):
    def __init__(self,operand):
        super().__init__(operand, "arctan")
        self.x = self.operand

    def differentiate(self):
        numerator = self.x.differentiate()
        denominator = Addition(1, Power(self.x, Constant(2)))
        return Division(numerator, denominator)

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

            if node.operator == "-":
                if isinstance(node.left, Constant) and node.left.value == 0:
                    return node.right
                elif isinstance(node.right, Constant) and node.right.value == 0:
                    return node.left

            if node.operator == "/":
                if isinstance(node.left, Constant) and node.left.value == 0:
                    return Constant(0)
                if isinstance(node.right, Constant) and node.right.value == 1:
                    return node.left


            return node

        elif isinstance(node, UnaryFunction):
            if isinstance(node, Sqrt):
                if (isinstance(node.operand, Constant) and node.operand.value == 0) or (
                        isinstance(node.operand, Constant) and node.operand.value == 1):
                    return Constant(node.operand.value)
                if isinstance(node.operand, Power) and node.operand.right.value == 2:
                    return node.operand.left

                if node.isPerfectSquare():
                    sqrtResult = node.intSqrt()
                    return sqrtResult if isinstance(sqrtResult, Constant) else node

                return node

            if isinstance(node, Negation):
                if isinstance(node.operand, Negation):
                    return node.operand.operand

            node.operand = Simplify.simplify(node.operand)
            return node

        else:
            return node

x = Variable("x")
expr = Addition(
    Addition(
        Multiplication(Constant(3), Power(x, Constant(4))),
        Sin(Division(Constant(3),Constant(5)))
    ),
    Negation(Constant(2))
)

derivative = expr.differentiate()
print(derivative)

simplified = Simplify.simplify(derivative)
print(simplified)