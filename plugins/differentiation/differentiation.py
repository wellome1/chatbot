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
        left = Constant(self.left.value) if isinstance(self.left, Constant) else self.left
        right = Constant(self.right.value) if isinstance(self.right, Constant) else self.right

        left = left.differentiate()
        right = right.differentiate()

        return Addition(left, right)

class Subtraction(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "-")

    def __str__(self):
        return f"{self.left} - {self.right}"

    def differentiate(self):
        left = Constant(self.left.value) if isinstance(self.left, Constant) else self.left
        right = Constant(self.right.value) if isinstance(self.right, Constant) else self.right

        left = left.differentiate()
        right = right.differentiate()

        return Subtraction(left, right)

class Multiplication(BinaryOperator):
    def __init__(self,a,b):
        super().__init__(a,b, "*")

    def __str__(self):
        return f"{self.left} * {self.right}"

    def differentiate(self):
        f = self.left
        g = self.right

        if isinstance(f, Constant):
            if f.value == 0:
                return Constant(0)
            return Multiplication(Constant(f.value), g.differentiate())
        if isinstance(g, Constant):
            if g.value == 0:
                return Constant(0)
            return Multiplication(Constant(g.value), f.differentiate())

        return Addition(Multiplication(f,g.differentiate()), Multiplication(g,f.differentiate()))

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
        operand = self.operand
        operandDiff = self.operand.differentiate()

        return Division(operandDiff, operand)

class Ln(UnaryFunction):
    def __init__(self, operand):
        super().__init__(operand, "ln")

    def differentiate(self):
        operand = self.operand
        operandDiff = self.operand.differentiate()

        return Division(operandDiff, operand)

class Exp(UnaryFunction):
    def __init__(self,operand):
        self.operand = Power(E, operand)
        super().__init__(operand, "exp")

    def differentiate(self):
        exponent = self.operand
        exponentDiff = self.operand.differentiate()

        return Multiplication(exponent, exponentDiff)

class Negation(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "-")

    def differentiate(self):
        operandDiff = self.operand.differentiate()

        return Negation(operandDiff)

class Parentheses(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand)

    def __str__(self):
        return f"({self.operand})"

    def differentiate(self):
        operandDiff = self.operand.differentiate()

        return Parentheses(operandDiff)

class Function(UnaryFunction):
    def __init__(self,operand, name="f"):
        super().__init__(operand, name)

    def differentiate(self):
        operandDiff = self.operand.differentiate()

        return Function(operandDiff, f"{self.name}'")

class Sqrt(UnaryFunction):
    def __init__(self,operand):
        super().__init__(operand, "√")

    def isPerfectSquare(self):
        n = self.operand

        if not isinstance(n, Constant):
            n = Simplify.simplify(n)
            if not isinstance(n, Constant):
                return f"{n} is cannot be simplified into an integer."

        if n.value < 0:
            return False

        z = n.value
        y = (z + 1) // 2

        while y < z:
            z = y
            y = (z + n.value // z) // 2

        return z * z == n

    def intSqrt(self):
        n = self.operand

        if not isinstance(n, Constant):
            n = Simplify.simplify(n)
            if not isinstance(n, Constant):
                return f"{n} is cannot be simplified into an integer."

        if n.value < 0:
            raise ValueError("Cannot sqrt negative numbers.")

        z = n.value
        y = (z+1) // 2
        while y < z:
            z = y
            y = (z + n.value // z) // 2

        return Constant(z) if z * z == n else None

    def differentiate(self):
        operand = self.operand

        return Division(1, Multiplication(2, Sqrt(operand)))

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
        print(f"Current node: {node}")

        if isinstance(node, BinaryOperator):
            print(f"Node classes:\nnode.left: {type(node.left).__name__}\nnode.right: {type(node.left).__name__}.")

            print(f"Unsimplified node.left: {node.left}")
            node.left = Simplify.simplify(node.left)
            print(f"Simplified node.left: {node.left}")

            print(f"Unsimplified node.right: {node.right}")
            node.right = Simplify.simplify(node.right)
            print(f"Simplified node.right: {node.right}")

            folded = node.makeConstant()
            if folded:
                return folded

            if node.operator == "+":
                print("Addition selected.")

                if isinstance(node.left, Constant) and node.left.value == 0:
                    print("(Addition) Left node is empty. Returning right node...")
                    return node.right
                elif isinstance(node.right, Constant) and node.right.value == 0:
                    print(f"(Addition) Right node is empty. Returning left node...")
                    return node.left

                # Negation in addition = Subtraction
                if isinstance(node.left, Negation) and not isinstance(node.right, Negation):
                    print("Negation found on left node. Making into subtraction...")
                    return Subtraction(node.right, node.left.operand)
                if isinstance(node.right, Negation) and not isinstance(node.left, Negation):
                    print("Negation found on right node. Making into subtraction...")
                    return Subtraction(node.left, node.right.operand)
                if isinstance(node.right, Negation) and isinstance(node.left, Negation):
                    print("Negation found on both nodes. Removing Negation.")
                    return Addition(node.right.operand, node.right.operand)

            if node.operator == "*":
                print("Multiplication selected.")
                # One node is Constant(0)
                if (isinstance(node.left, Constant) and node.left.value == 0) or (isinstance(node.right, Constant) and node.right.value == 0):
                    print("One factor is 0. Returning 0...")
                    return Constant(0)

                # One node is Constant(1)
                if isinstance(node.left, Constant) and node.left.value == 1:
                    print("node.left is 1, returning node.right...")
                    return node.right
                if isinstance(node.right, Constant) and node.right.value == 1:
                    print("node.right is 1, returning node.left...")
                    return node.left

                if isinstance(node.left, Constant) and isinstance(node.right, Multiplication):
                    print(f"node.left is Constant: {node.left}. node.right is Multiplication: {node.right}.")
                    if isinstance(node.right.left, Constant):
                        return Simplify.simplify(Multiplication(Multiplication(node.left, node.right.left), node.right.right))
                    if isinstance(node.right.right, Constant):
                        return Simplify.simplify(Multiplication(Multiplication(node.left, node.right.right), node.right.right))

                if isinstance(node.right, Constant) and isinstance(node.left, Multiplication):
                    print(f"node.right is Constant: {node.right}. node.left is Multiplication: {node.left}.")
                    if isinstance(node.left.left, Constant):
                        return Simplify.simplify(Multiplication(Multiplication(node.left.left, node.right), node.left.right))
                    if isinstance(node.left.right, Constant):
                        return Simplify.simplify(Multiplication(Multiplication(node.left.right, node.right), node.left.left))

                # Both nodes are multiplication
                if isinstance(node.left, Multiplication) and isinstance(node.right, Multiplication):
                    print(f"Both nodes are multiplication:\nnode.left: {node.left}\nnode.right: {node.right}")
                    if isinstance(node.left.left, Constant):
                        if isinstance(node.left.right, Constant):
                            return Simplify.simplify(
                                Multiplication(
                                    Multiplication(
                                        node.left.left,
                                        node.left.right
                                    ),
                                    Multiplication(
                                        node.right.left,
                                        node.right.right
                                    )
                                )
                            )

                        if isinstance(node.right.left, Constant):
                            return Simplify.simplify(
                                Multiplication(
                                    Multiplication(
                                        node.left.left,
                                        node.right.left
                                    ),
                                    Multiplication(
                                        node.left.right,
                                        node.right.right
                                    )
                                )
                            )

                        if isinstance(node.right.right, Constant):
                            return Simplify.simplify(
                                Multiplication(
                                    Multiplication(
                                        node.left.left,
                                        node.right.right
                                    ),
                                    Multiplication(
                                        node.left.right,
                                        node.right.left
                                    )
                                )
                            )

                    if isinstance(node.left.right, Constant) and not isinstance(node.left.left, Constant):
                        if isinstance(node.right.left, Constant):
                            return Simplify.simplify(
                                Multiplication(
                                    Multiplication(
                                        node.left.right,
                                        node.right.left
                                    ),
                                    Multiplication(
                                        node.left.left,
                                        node.right.right
                                    )
                                )
                            )

                        if isinstance(node.right.right, Constant):
                            return Simplify.simplify(
                                Multiplication(
                                    Multiplication(
                                        node.left.right,
                                        node.right.right
                                    ),
                                    Multiplication(
                                        node.left.left,
                                        node.right.left
                                    )
                                )
                            )

                # One node is Power
                if isinstance(node.right, Power):
                    print(f"node.right is Power: {node.right}")
                    if isinstance(node.right.left, Variable) and isinstance(node.left, Constant):
                        print(f"node.right.left is Variable: {node.right.left}, node.left is Constant: {node.left}")
                        node.left = Power(Multiplication(node.left, node.right.left), node.right.right)
                        return Simplify.simplify(node.left)
                    if isinstance(node.right.left, Constant) and isinstance(node.left, Constant):
                        print(f"node.right.left is Constant: {node.right.left}, node.left is Constant: {node.left}")
                        node.left = Power(Multiplication(node.right.left, node.left), node.right.right)
                        return Simplify.simplify(node.left)
                    if isinstance(node.right.left, Multiplication) and isinstance(node.left, Constant):
                        # Multiplication(Power(Multiplication(...))) - node.right.left
                        # Multiplication(Constant(...)) - node.left

                        if isinstance(node.right.left.left, Constant):
                            return Simplify.simplify(
                                    Multiplication(
                                        Multiplication(
                                            node.right.left.left,
                                            node.left
                                        ),
                                       Power(node.right.left.right, node.right.right)
                                    )
                                )
                        if isinstance(node.right.left.right, Constant):
                            return Simplify.simplify(
                                    Multiplication(
                                        Multiplication(
                                            node.right.left.right,
                                            node.left
                                        ),
                                        Power(node.right.left.left, node.right.right)
                                    )
                                )

                elif isinstance(node.left, Power):
                    print(f"node.left is Power: {node.left}")
                    if isinstance(node.left.left, Variable) and isinstance(node.right, Constant):
                        print(f"node.left.left is Variable: {node.left.left}, node.right is Constant: {node.right}")
                        node.right = Power(Multiplication(node.right, node.left.left), node.left.right)
                        return Simplify.simplify(node.right)
                    if isinstance(node.left.left, Constant) and isinstance(node.right, Constant):
                        print(f"node.left.left is Constant: {node.left.left}, node. right is Constant: {node.right}")
                        node.right = Power(Constant(Multiplication(node.left.left, node.right)), node.left.right)
                        return Simplify.simplify(node.right)

                # Both nodes are Constant
                if isinstance(node.left, Constant) and isinstance(node.right, Constant):
                    print(f"Both node.left ({node.left}) and node.right ({node.right}) are Constant.")
                    return Simplify.simplify(Multiplication(Constant(node.left.value), Constant(node.right.value)))

                # One node is Negation
                if isinstance(node.left, Negation) and isinstance(node.right, Atom):
                    print(f"node.left is negation: {node.left}, node.right is Atom: {node.right}.")
                    return Simplify.simplify(Negation(Multiplication(node.left.operand, node.right)))
                if isinstance(node.right, Negation) and isinstance(node.left, Atom):
                    print(f"node.right is negation: {node.right}, node.left is Atom: {node.left}.")
                    return Simplify.simplify(Negation(Multiplication(node.left, node.right.operand)))

                # Both nodes are Negation
                if isinstance(node.left, Negation) and isinstance(node.right, Negation):
                    print(f"Both nodes are negation: Left: {node.left}, Right: {node.right}")
                    return Simplify.simplify(Multiplication(node.left.operand, node.right.operand))

                # Both nodes are Sqrt
                if isinstance(node.left, Sqrt) and isinstance(node.right, Sqrt):
                    print(f"Both nodes are Sqrt: Left: {node.left}, Right: {node.right}")
                    return Simplify.simplify(Sqrt(Multiplication(node.left.operand, node.right.operand)))

                # Both nodes are Power
                if isinstance(node.right, Power) and isinstance(node.left, Power):
                    print(f"Both nodes are Power. Left: {node.left}, Right: {node.right}.")
                    return Simplify.simplify(Power(Multiplication(node.left.left, node.right.left), Addition(node.left.right, node.right.right)))

            if node.operator == "-":
                if isinstance(node.left, Constant) and node.left.value == 0:
                    return Simplify.simplify(node.right)
                elif isinstance(node.right, Constant) and node.right.value == 0:
                    return Simplify.simplify(node.left)

                if isinstance(node.left, Negation) and isinstance(node.right, Negation):
                    return Addition(node.left.operand, node.right.operand)

            if node.operator == "/":
                if isinstance(node.left, Constant) and node.left.value == 0:
                    return Constant(0)
                if isinstance(node.right, Constant) and node.right.value == 1:
                    return Simplify.simplify(node.right)

            return node

        elif isinstance(node, UnaryFunction):
            print(f"Operand class: {node.operand.__class__.__name__}")
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
                elif isinstance(node.operand, Constant):
                    if node.operand.value == 0:
                        return Constant(0)

            node.operand = Simplify.simplify(node.operand)
            return node

        else:
            return node

class PrettyPrinter:
    @staticmethod
    def print(node, simplify=False):
        if simplify: node = Simplify.simplify(node)
        return PrettyPrinter.printRecursively(node)

    @staticmethod
    def printRecursively(node):
        if isinstance(node, Atom):
            return str(node)

        elif isinstance(node, BinaryOperator):
            if isinstance(node, Multiplication):
                # Constant/Variable
                if isinstance(node.left, Constant) and isinstance(node.right, Variable):
                    return f"{node.left}{node.right}"
                if isinstance(node.right, Constant) and isinstance(node.left, Variable):
                    return f"{node.right}{node.left}"

                # One node is a part of Parenthesis
                if isinstance(node.left, Parentheses) and isinstance(node.right, Atom):
                    return f"{node.right}{node.left}"
                elif isinstance(node.right, Parentheses) and isinstance(node.left, Atom):
                    return f"{node.left}{node.right}"

                # Both nodes are Parenthesis
                if isinstance(node.left, Parentheses) and isinstance(node.right, Parentheses):
                    return f"({node.left})({node.right})"

            leftStr = PrettyPrinter.printRecursively(node.left)
            rightStr = PrettyPrinter.printRecursively(node.right)
            return f"{leftStr} {node.operator} {rightStr}"

        elif isinstance(node, UnaryFunction):
            operand = PrettyPrinter.printRecursively(node.operand)

            if isinstance(node, Abs):
                return f"|{operand}|"
            elif isinstance(node, Parentheses):
                return f"({operand})"
            else:
                return f"{node.name}({operand})"

        else:
            return str(node)

x = Variable("x")
expr = Addition(
    Addition(
        Multiplication(Constant(3), Power(x, Constant(4))),
        Sin(Division(Constant(3),Constant(5)))
    ),
    Negation(Constant(2))
)

differentiate = expr.differentiate()

print(PrettyPrinter.print(differentiate, True))