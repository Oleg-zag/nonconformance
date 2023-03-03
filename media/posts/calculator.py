from typing import List

OPERATIONS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}

def calculator(input_data: List[str]) -> int:
    '''72101085'''
    stack = []
    digit = 0
    flag = False
    for item in input_data:
        if item not in OPERATIONS.keys():
            item = int(item)
            stack.append(item)
            continue
        else:
            digit = OPERATIONS[item](stack[-2],stack[-1])
            flag = True
        stack = stack[:-2]
        stack.append(digit)
    if flag is False:
        return(stack[-1])
    return(digit)

if __name__ == '__main__':
    input_data = list(map(str, input().split()))
    print(calculator(input_data))
