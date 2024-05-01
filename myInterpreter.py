import re

operationalKeys = ["mod", "plus", "minus", "times", "divided by"]

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def varmap(targetVar, state):
   if targetVar in state:
       return state[targetVar]
   else:
       raise ValueError("Error: Var not found")


def checkState(dic, key):
    if key in dic.keys():
         return True
    else:
         return False

def evalOperand(operand, state):
    if checkState(state, operand):
        temp = state[operand]
        if (is_number_tryexcept(temp)):
            return int(temp)
        return temp
    elif is_number_tryexcept(operand):
        return (int(operand))
        

def isOperExpr(expression):
    for op in operationalKeys:
        if op in expression:
            return True
    return False
    
def evalOperExpr(expression, state):
    if "mod" in expression:
        op1, op2 = expression.split(" mod ")
        out1 = evalOperand(op1, state)
        out2 = evalOperand(op2, state)
        try:
            return out1 % out2
        except TypeError:
            return False
    elif "plus" in expression:
        return 1
    elif "minus" in expression:
        return 1
    elif "times" in expression:
        return 1
    elif "divided by" in expression:
        return 1
    else:
        return "Error"
    
def evalBoolExpr(expression, state):
    if (len(expression.split()) == 1):
        if checkState(state, expression):
            r = state[expression]
            if is_number_tryexcept(r):
                return int(r)
            else:
                return r
        elif is_number_tryexcept(expression):
            return int(expression)
    elif (isOperExpr(expression)):
        r = evalOperExpr(expression, state)
        return r

    return False

def getLoopEnd(prog, index):
    while index < len(prog):
        line = prog[index]
        if "end loop" in line:
            return index
        index+=1
    print("Error: loop doesn't terminate")
    return -1

def getNextBlockIndex(program, index):
    while index < len(prog):
        line = program[index]
        if "elseif" in line:
            return index
        elif "else" in line:
            return index
        elif "end if" in line:
            return index 
        index+=1
    print("Error: conditional block doesn't end")
    return -1

def executeProgram(program):
    state = dict()
    functTab = dict()
    loopStart = -1
    loopEnd = -1
    conditionalLines = False
    conditionalFlag = False
    loopLines = False
    loopFlag = False

    i = 0
    while i < len(program):
        line = program[i]
        #print(str(i) + line)
        if "    " in line:
           line = line.strip()
        
        instruction, expression = line.split(" ", 1)
        
        if instruction == "end":
            if expression == "if":
                conditionalFlag = False
                conditionalLines = False
                i+=1
                continue
            elif expression == "loop":
                if (loopLines == False):
                    i+=1
                    continue
                i = loopStart
                continue
            
        if instruction == "home":
            functTab[instruction] = i
            i+=1
            continue

        if instruction == "int":
            var, val = expression.split("equals")
            var, val = var.strip(), val.strip()
            state[var] = val
            i+=1
            continue
        elif instruction == "str":
            var, val = expression.split("equals")
            var, val = var.strip(), val.strip()
            val = val.strip("'")
            state[var] = val
            i+=1
            continue
        elif instruction == "print":
            if expression.find(','):
                expression = expression.split(",")
            for x in expression:
                x = x.strip()
                if checkState(state, x):
                    print(state[x],end="")
                    continue
                elif x.find("'") == 0:
                    print(eval(x),end="")
                    continue
            print()
            i+=1
            continue
        elif instruction =="add":
            val, var = expression.split(" to ")
            if checkState(state, var):
                currVal = state[var]
                newVal = int(currVal) + int(val)
                state[var] = newVal
                i+=1
                continue
            else:
                print("Error: variable not found")
                return -1
        elif instruction == "if":
            conditionalLines = True
            if "is not equivalent to" in expression:
                temp = expression.split(" is not equivalent to ")
                expr1 = temp[0]
                expr2 = temp[1].rstrip(" then")
                res1 = evalBoolExpr(expr1, state)
                res2 = evalBoolExpr(expr2, state)
                if (res1 != res2):
                    conditionalFlag = True
                else:
                    conditionalFlag = False
                    i = getNextBlockIndex(lines, i+1)
                    continue
                i+=1
                continue
            elif "is equivalent to" in expression:
                temp = expression.split(" is equivalent to ")
                expr1 = temp[0]
                expr2 = temp[1].rstrip(" then")
                res1 = evalBoolExpr(expr1, state)
                res2 = evalBoolExpr(expr2, state)
                if (res1 == res2):
                    conditionalFlag = True
                else:
                    conditionalFlag = False
                    i = getNextBlockIndex(lines, i+1)
                    continue
                i+=1
                continue
            elif "True" in expression:
                conditionalFlag = True
                i+=1
                continue
            elif "False" in expression:
                conditionalFlag = False
                i = getNextBlockIndex(lines, i+1)
                continue
            else:
                print("Error: invalid statement")
                return -1
        elif (instruction == "elseif"):
            if conditionalFlag == True:
                nextIndex = getNextBlockIndex(lines, i+1)
                i = nextIndex
                continue
            if "is not equivalent to" in expression:
                temp = expression.split(" is not equivalent to ")
                expr1 = temp[0]
                expr2 = temp[1].rstrip(" then")
                res1 = evalBoolExpr(expr1, state)
                res2 = evalBoolExpr(expr2, state)
                if (res1 != res2):
                    conditionalFlag = True
                else:
                    conditionalFlag = False
                    i = getNextBlockIndex(lines, i+1)
                    continue
                i+=1
                continue
            elif "is equivalent to" in expression:
                temp = expression.split(" is equivalent to ")
                expr1 = temp[0]
                expr2 = temp[1].rstrip(" then")
                res1 = evalBoolExpr(expr1, state)
                res2 = evalBoolExpr(expr2, state)
                if (res1 == res2):
                    conditionalFlag = True
                else:
                    conditionalFlag = False
                    i = getNextBlockIndex(lines, i+1)
                    continue
                i+=1
                continue
        elif (instruction == "else"):
            if conditionalFlag == True:
                nextIndex = getNextBlockIndex(lines, i+1)
                i = nextIndex
                continue
            conditionalFlag == True
            i+=1
            continue

        elif (instruction == "loop"):
            if "from" not in expression:
                print("Error: statement invalid")
                return -1

            expression = expression.split()
            startRangeVal = expression[1]
            endRangeVal = expression[3]
            counterVar = expression[-1]

            if loopFlag == False:
                loopFlag = True
                loopLines = True
                loopStart = i
                loopEnd = getLoopEnd(lines, i+1)
                state[counterVar] = startRangeVal
            counterVal = state[counterVar]
            #print(counterVal)
            if (int(counterVal) < int(endRangeVal)):
                newCountVal = int(counterVal) + 1
                state[counterVar] = str(newCountVal)
                i+=1
                continue
            else:
                i = loopEnd
                loopFlag = False
                loopLines = False
                continue


            
        else:
            print("Error: Statement invalid, terminating program.")
            return -1

    return

programs = ["simpleprog1.genesis", "simpleprog2.genesis", "FizzBuzz.genesis"]
#programs = ["FizzBuzz.genesis"]
for prog in programs:
    f = open(prog, "r")
    lines = []
    line = f.readline()
    while line:
        #print(line)
        lines.append(line)
        line = f.readline()
    f.close()
    executeProgram(lines)