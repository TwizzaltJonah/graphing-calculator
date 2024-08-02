import globals
import math

NUMBERS = "123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
OPERATORS = "+-*/^"
SHORTCUTS = {
    # "log": lambda x: math.log(x, 10),
    "sqrt": lambda x: x ** 0.5,
    "sin": lambda x: math.sin(x)
}

def strToEquation(input: str):
    isEqualsSign = False
    equation = []
    charactersToSkip = 0

    leftBrackets = 0
    rightBrackets = 0

    for i in range(len(input)):
        if charactersToSkip > 0:
            charactersToSkip -= 1
            continue

        for j in SHORTCUTS:
            if input.lower()[i:i+len(j)] == j:
                charactersToSkip = len(j) - 1
                equation.append(j)

        if input[i] in "123456789.":
            numberCheckerIndex = i
            while input[numberCheckerIndex] in "1234567890.":
                numberCheckerIndex += 1
                if numberCheckerIndex == len(input):
                    break
            if "." in input[i:numberCheckerIndex]:
                equation.append(float(input[i:numberCheckerIndex]))
            else:
                equation.append(int(input[i:numberCheckerIndex]))
            charactersToSkip = numberCheckerIndex - i - 1

        elif input.lower()[i] in "=xy()+-*/^":
            if input.lower()[i] == "(":
                leftBrackets += 1

            if input.lower()[i] == ")":
                rightBrackets += 1

            if input.lower()[i] == "=":
                if not isEqualsSign:
                    # equation.append(input.lower()[i])
                    equalsSignEquationIndex = len(equation)
                isEqualsSign = True
            else:
                equation.append(input.lower()[i])

        if len(equation) > 1:
            if equation[-1] == "(" and not (equation[-2] in SHORTCUTS.keys() or str(equation[-2]) in "=(+-*/^"):
                equation.insert(-1, "*")

    # if "=" in equation:
    #     equationStringLeft = equation.split("=")[0]
    #     equationStringRight = equation.split("=")[1]
    # else:
    #     # error message
    #     equationStringLeft = None
    #     equationStringRight = None

    if leftBrackets != rightBrackets:
        pass # error message

    return (equation[:equalsSignEquationIndex], equation[equalsSignEquationIndex:], "=")

def evaluate(expression: list, x: float|int, y: float|int):
    returnExpression = expression.copy()

    for i in range(len(returnExpression)):
        if returnExpression[i] == "x":
            returnExpression[i] = x
        elif returnExpression[i] == "y":
            returnExpression[i] = y

    if returnExpression.count("(") != 0:
        openParenthesisIndex = returnExpression.index("(")

        # returnExpression.reverse()
        # closeParenthesisIndex = len(returnExpression) - returnExpression.index(")") - 1
        # returnExpression.reverse()

        openParenthesisCount = 0
        closeParenthesisCount = 0
        for i in range(len(returnExpression)):
            if returnExpression[i] == "(":
                openParenthesisCount += 1
            elif returnExpression[i] == ")":
                closeParenthesisCount += 1
                if closeParenthesisCount == openParenthesisCount:
                    closeParenthesisIndex = i

        returnExpression.insert(openParenthesisIndex, evaluate(returnExpression[openParenthesisIndex+1:closeParenthesisIndex], x, y)[0])

        for i in range(closeParenthesisIndex-openParenthesisIndex+1):
            returnExpression.pop(openParenthesisIndex+1)

    returnExpressionCopy = returnExpression.copy()
    for i in range(len(returnExpression)):
        if returnExpression[i] in SHORTCUTS:
            returnExpressionCopy.insert(i, SHORTCUTS[returnExpression[i]](returnExpression[i+1]))
            returnExpressionCopy.pop(i+1)
            returnExpressionCopy.pop(i+1)
    returnExpression = returnExpressionCopy

    # returnExpressionCopy = returnExpression.copy()
    # for i in range(len(returnExpression)):
    #     if returnExpression[i] == "^":
    #         returnExpressionCopy.insert(i-1, returnExpression[i-1] ** returnExpression[i+1])
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    # returnExpression = returnExpressionCopy

    for i in range(returnExpression.count("^")):
        operationIndex = returnExpression.index("^")
        returnExpression.insert(operationIndex - 1, returnExpression[operationIndex - 1] ** returnExpression[operationIndex + 1])
        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)

    # returnExpressionCopy = returnExpression.copy()
    # for i in range(len(returnExpression)):
    #     if returnExpression[i] == "*":
    #         returnExpressionCopy.insert(i-1, returnExpression[i-1] * returnExpression[i+1])
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #     elif returnExpression[i] == "/":
    #         returnExpressionCopy.insert(i-1, returnExpression[i-1] / returnExpression[i+1])
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #     elif i-1 >= 0:
    #         if type(returnExpression[i-1]) in (int, float) and type(returnExpression[i]) in (int, float):
    #             returnExpressionCopy.insert(i - 1, returnExpression[i - 1] * returnExpression[i])
    #             returnExpressionCopy.pop(i)
    #             returnExpressionCopy.pop(i)
    # returnExpression = returnExpressionCopy

    for i in range(returnExpression.count("*") + returnExpression.count("/")):
        if returnExpression.count("*") == 0 and returnExpression.count("/") != 0:
            operationIndex = returnExpression.index("/")
        elif returnExpression.count("/") == 0 and returnExpression.count("*") != 0:
            operationIndex = returnExpression.index("*")
        else:
            operationIndex = min(returnExpression.index("*"), returnExpression.index("/"))

        if returnExpression[operationIndex] == "*":
            returnExpression.insert(operationIndex - 1, returnExpression[operationIndex - 1] * returnExpression[operationIndex + 1])
        else:
            returnExpression.insert(operationIndex - 1, returnExpression[operationIndex - 1] / returnExpression[operationIndex + 1])

        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)

    # returnExpressionCopy = returnExpression.copy()
    # indexShift = 0
    # for i in range(len(returnExpression)):
    #     if returnExpression[i] == "+":
    #         returnExpressionCopy.insert(i - indexShift - 1, returnExpression[i - indexShift - 1] + returnExpression[i - indexShift + 1])
    #         returnExpressionCopy.pop(i - indexShift)
    #         returnExpressionCopy.pop(i - indexShift)
    #         returnExpressionCopy.pop(i - indexShift)
    #         indexShift += 2
    #         print(returnExpression, returnExpressionCopy, 2)
    #     elif returnExpression[i] == "-":
    #         returnExpressionCopy.insert(i - 1, returnExpression[i - 1] - returnExpression[i + 1])
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    #         returnExpressionCopy.pop(i)
    # returnExpression = returnExpressionCopy

    for i in range(returnExpression.count("+") + returnExpression.count("-")):
        if returnExpression.count("+") == 0 and returnExpression.count("-") != 0:
            operationIndex = returnExpression.index("-")
        elif returnExpression.count("-") == 0 and returnExpression.count("+") != 0:
            operationIndex = returnExpression.index("+")
        else:
            operationIndex = min(returnExpression.index("+"), returnExpression.index("-"))

        if returnExpression[operationIndex] == "+":
            returnExpression.insert(operationIndex - 1,
                                    returnExpression[operationIndex - 1] + returnExpression[operationIndex + 1])
        else:
            returnExpression.insert(operationIndex - 1,
                                    returnExpression[operationIndex - 1] - returnExpression[operationIndex + 1])

        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)
        returnExpression.pop(operationIndex)

    return returnExpression

def is_greater_than(x, y, equation):
    try:
        return float(evaluate(equation[0], x, y)[0]) > float(evaluate(equation[1], x, y)[0])
    except TypeError:
        return float(evaluate(equation[0], x, y)[0].real) > float(evaluate(equation[1], x, y)[0].real)
