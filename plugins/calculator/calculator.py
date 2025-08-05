from pluginBase import Plugin; import sympy
import os; import json

class CalculatorPlugin(Plugin):
    def __init__(
            self,
            pluginName:str,
            pluginDesc:str,
            pluginTags:list[str],
            triggerWords:list[str],
            api:str,
            function:callable=None,
            overwrite=False
    ):
        if function is None: function = self.getResponse
        super().__init__(
            pluginName=pluginName,
            pluginDesc=pluginDesc,
            pluginTags=pluginTags,
            triggerWords=triggerWords,
            api=api,
            function=function,
            overwrite=overwrite
        )

        formulasFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "formulas.json")
        with open(formulasFile, "r", encoding="UTF-8") as f:
            self.formulas = json.load(f)

        self.formulaFuncs = {
            "quadraticEquation": self.quadraticEquation,
            "sineRuleAngle": self.sineRuleAngle,
        }

    def getResponse(self, query):
        query = query.split(",")
        commandToRun = None
        angleFormat = "degrees"
        for formulaName, formulaData in self.formulas.items():
            for querySection in query:
                querySection = querySection.strip()
                if querySection in formulaData["triggers"]:
                    commandToRun = self.formulaFuncs[formulaData["command"]]
                if querySection == "radians":
                    angleFormat = "radians"
                if commandToRun is not None:
                    break
            if commandToRun is not None:
                break
        if commandToRun is None: raise Exception("No command to run")

        variables = {
            "a": 1.0,
            "b": None,
            "c": None,
        }
        for part in query[1:]:
            part = part.strip()
            if "=" in part:
                key, value = part.split("=")
                variables[key.strip()] = sympy.Rational(value.strip())

        for var in ["b", "c"]:
            if variables[var] is None:
                raise ValueError(f"Variable '{var}' must be defined in the query!")

        match commandToRun:
            case self.quadraticEquation:
                if len(variables) not in (2,3): raise Exception("Invalid command. Too many/not enough variables.")
                self.quadraticEquation(variables, self.formulas["quadratic"]["steps"])

            case self.sineRuleAngle:
                if len(variables) != 3: raise Exception("Invalid command. Too many/not enough variables.")
                self.sineRuleAngle(variables, self.formulas["sineRuleAngle"]["steps"], angleFormat)

    def checkRealness(self, num):
        if num.is_real:
            return "Real"
        else:
            return "Imaginary"

    def goThroughSteps(self, formula, stepValues, variables, steps, stepNum=0):
        a = variables["a"]
        b = variables["b"]
        c = variables["c"]

        print(f"Formula running: {formula}")

        match formula:
            case "Quadratic Equation":
                theDiscriminant = variables["theDiscriminant"]
                sqrtDiscriminant = variables["sqrtDiscriminant"]
                print(f"Values: a={a}, b={b}, c={c}")
                stringStart = "x = "
            case "Sine Rule (Angle)":
                aRad = variables["aRad"]
                print(f"Values: Angle={a}, b={b}, c={c}")
                stringStart = "θ = "
            case "Sine Rule (Side)":
                aRad = variables["aRad"]
                bRad = variables["bRad"]
                print(f"Values: Side={c}, Angle A={a}, Angle B={b}")
                stringStart = "x = "

            case _:
                stringStart = "Value = "

        for step in steps:
            print(f"{stringStart}{step.format(**variables)}")
            print(f"→ {stepValues[stepNum]}")
            if stepNum == (len(stepValues) - 1):
                break
            stepNum += 1

        finalStepNum = len(stepValues) - 1
        print(f"Result: {self.checkRealness(stepValues[finalStepNum])}")

    def quadraticEquation(self, variables, steps):
        a = variables.get("a",1)
        b = variables["b"]
        c = variables["c"]

        theDiscriminant = b**2 - 4*a*c
        sqrtDiscriminant = sympy.sqrt(theDiscriminant)

        stepValues = {
            0: theDiscriminant,
            1: sqrtDiscriminant,
            2: (-b + sqrtDiscriminant)/(2*a),
            3: (-b - sqrtDiscriminant) / (2 * a)
        }

        self.goThroughSteps(
            formula="Quadratic Equation",
            stepValues=stepValues,
            variables={
                "a": a,
                "b": b,
                "c": c,
                "theDiscriminant": theDiscriminant,
                "sqrtDiscriminant": sqrtDiscriminant,
            },
            steps=steps
        )

        print(f"x_1 = {stepValues[2].evalf()}")
        print(f"x_2 = {stepValues[3].evalf()}")
        print("Making it look better...")
        print(f"x_1 = {stepValues[2]}\nx_2 = {stepValues[3]}")

    def sineRuleAngle(self, variables, steps, angleFormat):
        a = variables["a"]
        b = variables["b"]
        c = variables["c"]

        aRad = sympy.rad(a)
        stepValues = {
            0: aRad,
            1: sympy.sin(aRad),
            2: (b * sympy.sin(aRad)) / c,
            3: sympy.asin((b * sympy.sin(aRad)) / c),
            4: sympy.deg(sympy.asin((b * sympy.sin(aRad)) / c))
        }

        variables["aRad"] = aRad

        if angleFormat == "radians":
            self.goThroughSteps(
                formula="Sine Rule (Angle)",
                stepValues=stepValues,
                variables=variables,
                steps=steps,
                stepNum=1
            )

        else:
            self.goThroughSteps(
                formula="Sine Rule (Angle)",
                stepValues=stepValues,
                variables=variables,
                steps=steps,
                stepNum=0
            )

        print(f"Computed Angle (θ) = {stepValues[4].evalf()} degrees")

    def sineRuleSide(self, variables, steps, angleFormat):
        a = variables["a"]
        b = variables["b"]
        c = variables["c"]

        aRad = sympy.rad(a)
        bRad = sympy.rad(b)

        stepValues = {
            0: f"A_rad = {aRad}, B_rad = {bRad}",
            1: f"Sin(A) = {sympy.sin(aRad)}, Sin(B) = {sympy.sin(bRad)}",
            2: (c * sympy.sin(bRad)) / sympy.sin(aRad),
            3: sympy.simplify((c * sympy.sin(bRad)) / sympy.sin(aRad))
        }

        variables["aRad"] = aRad
        variables["bRad"] = bRad

        if angleFormat == "radians":
            self.goThroughSteps(
                formula="Sine Rule (Side)",
                stepValues=stepValues,
                variables=variables,
                steps=steps,
                stepNum=1
            )

        else:
            self.goThroughSteps(
                formula="Sine Rule (Side)",
                stepValues=stepValues,
                variables=variables,
                steps=steps,
                stepNum=0
            )

        print(f"Computed side = {stepValues[3].evalf()}")
        print("Making it look better...")
        print(f"Side = {stepValues[3]}")
