import numpy as np
import random
import time
from datetime import datetime
from difflib import SequenceMatcher
import pytz
from colorama import Fore, Back, Style

tz_Istanbul = pytz.timezone('Europe/Istanbul')

def define_input_pool():
    targetNumber = random.choice(range(100, 1000))
    smallNumbers = [x for x in range(1,11)]
    largeNumbers = [25, 50, 75, 100]
    arithmeticOperators = ["+", "-", "*", "/"]
    selectNumbersForCalculation = []
    solutionExplanation = []
    solutionResult = []
    solutionDifference =[]
    totalDomain = {}

    selectSmallNumbers = list(np.random.choice(smallNumbers, 5, replace=False))
    selectLargeNumbers = random.choice(largeNumbers)
    selectSmallNumbers.append(selectLargeNumbers)
    selectNumbersList = tuple(sorted(selectSmallNumbers))
    print(f"{Fore.LIGHTBLUE_EX}The numbers given to solve are:{Style.RESET_ALL} {Fore.RED}{selectNumbersList}{Style.RESET_ALL}")
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}The number you have to find is:{Style.RESET_ALL} {Fore.RED}{targetNumber} {Style.RESET_ALL}")
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}You have 60 seconds to solve the problem{Style.RESET_ALL}")
    time.sleep(3)
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}Your time has started! Good luck!{Style.RESET_ALL}")
    print('\n')
    
    startTimeIstanbul = datetime.now(tz_Istanbul).strftime("%I:%M:%S %p")
    print(f"{Fore.RED}{startTimeIstanbul}{Style.RESET_ALL}")
    start_time = time.time()
    
    for r in range(150_000):
        selectNumbersListDuplicate = [x for x in selectNumbersList]
        while len(selectNumbersListDuplicate) - 1 > 0:
            selectArithmeticOperator = random.choice(arithmeticOperators)
            if len(selectNumbersListDuplicate) < 2:
                selectNumbersForCalculation.append(selectNumbersListDuplicate[0])
                selectNumbersForCalculation.append(random.choice(solutionResult))
            else:
                selectNumbersForCalculation = list(np.random.choice(selectNumbersListDuplicate, 2, replace=False))
            result, explanation, num1, num2 = arithmetic_operation(selectNumbersForCalculation, selectArithmeticOperator)
            if result is not None: 
                try:
                    selectNumbersListDuplicate.remove(selectNumbersForCalculation[0])
                    selectNumbersListDuplicate.remove(selectNumbersForCalculation[1])
                except:
                    pass
                selectNumbersListDuplicate.append(result)
                solutionExplanation.append(explanation)
                difference = abs(result-targetNumber)
                solutionDifference.append(difference)
                solutionResult.append(result)
                selectNumbersForCalculation = []
        exp, index = interim_solution(solutionExplanation, solutionDifference, solutionResult)
        totalDomain[exp] = solutionResult[index]
        solutionExplanation.clear()
        solutionResult.clear()
        solutionDifference.clear()
   
    keyList = list(totalDomain.keys())
    valList = list(totalDomain.values())
    minValueList = [abs(x-targetNumber) for x in valList]
    minValue = min(minValueList)  
    minValueIndex = minValueList.index(minValue)
    finalSolutionExplanation = keyList[minValueIndex]
    finalSolutionResult = valList[minValueIndex]
    distance = abs(targetNumber - finalSolutionResult)
    
    end_time = time.time()
    durationSeconds = end_time-start_time
    if durationSeconds < 60:
        waitSeconds = 60 - durationSeconds
        time.sleep(waitSeconds)
    print('\n')
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}Your time is up!{Style.RESET_ALL}")
    print('\n')
    endTimeIstanbul = datetime.now(tz_Istanbul).strftime("%I:%M:%S %p")
    print(f"{Fore.RED}{endTimeIstanbul}{Style.RESET_ALL}")
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}Here is the solution:{Style.RESET_ALL}")
    print('\n')
    print(f"{Fore.MAGENTA}{finalSolutionExplanation}{Style.RESET_ALL}")
    print('\n')
    print(f"{Fore.LIGHTBLUE_EX}The closest number is:{Style.RESET_ALL} {Fore.RED}{finalSolutionResult}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}different from the target number by {distance}{Style.RESET_ALL}")                                 
                
def interim_solution(solutionExplanation, solutionDifference, solutionResult):
    exp = ""
    optimalSolution = min(solutionDifference)
    index = solutionDifference.index(optimalSolution)
    for step in range(index + 1):
        string1 = str(solutionResult[step])
        string2 = solutionExplanation[step:]
        match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
        if match is None:
            solutionExplanation[step] = ""
        exp = f'{exp} \n {solutionExplanation[step]}'
    return exp, index
             
def arithmetic_operation(selectNumbersForCalculation, selectArithmeticOperator):
    num1 = selectNumbersForCalculation[0]
    num2 = selectNumbersForCalculation[1]       
    if selectArithmeticOperator == '+':
        result = int(num1 + num2)
        explanation = f'Sum {num1} and {num2} = {result}. '
    elif selectArithmeticOperator == '-' and num1 > num2:
        result = int(num1 - num2)
        explanation = f'Subtract {num2} from {num1} = {result}. '
    elif selectArithmeticOperator == '*':
        result = int(num1 * num2 )
        explanation = f'Multiply {num1} with {num2} = {result}. '
    elif selectArithmeticOperator == '/' and num2 !=0 and num1%num2 == 0:
        result = int(num1 / num2)
        explanation = f'Divide {num1} by {num2} = {result}. '
    else:
        result = None
        explanation = None
    return result, explanation, num1, num2
  
contest = define_input_pool()
contest
