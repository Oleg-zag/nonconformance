from typing import Any, List


class Deque:
    'ID 71130931'
    def __init__(self, item_quantity: int, result: List[str]):
        self.__queue = [None] * item_quantity
        self.__max_len = item_quantity
        self.__head = 0
        self.__tail = 0
        self.__size = 0
        self.__back = 0
        self.__front = 0
        self.result = result

    def is_empty(self) -> int:
        return self.__size == 0

    def push_back(self, value: str, result: List[str]) -> Any:
        if self.__size < self.__max_len:
            self.__queue[self.__tail] = value
            self.__tail = (self.__tail + 1) % self.__max_len
            self.__size += 1
        elif self.__size >= self.__max_len:
            DequeIsOver(result)
    
    def push_front(self, value: str, result: List[str]) -> Any:
        if self.__size != self.__max_len:
            self.__queue[self.__head - 1] = value
            self.__head = (self.__head - 1) % self.__max_len
            self.__size += 1
        else:
            DequeIsOver(result)

    def pop_front(self, result: List[str]) -> Any:
        if self.is_empty():
            DequeIsEmpty(result)
            return None
        self.__front = self.__queue[self.__head]
        self.__queue[self.__head] = None
        self.__head = (self.__head + 1) % self.__max_len
        self.__size -= 1
        self.result.append(self.__front)

    def pop_back(self, result: List[str]) -> Any:
        if self.is_empty():
            DequeIsEmpty(result)
            return None
        self.__back = self.__queue[self.__tail-1]
        self.__queue[self.__tail - 1] = None
        self.__tail = (self.__tail - 1) % self.__max_len
        self.__size -= 1
        self.result.append(self.__back)


class DequeIsOver:
    '''Добавление в полную очередь.'''
    def __init__(self, result: List[str]):
        self.result = result
        self.result.append('error')


class DequeIsEmpty:
    '''Удаление из пустого списка'''
    def __init__(self, result: List[str]):
        self.result = result
        self.result.append('error')


if __name__ == '__main__':
    command_quantity = int (input())
    item_quantity = int (input())
    result = []
    deque = Deque(item_quantity, result)
    for _ in range(command_quantity):
        command = input().split()
        call_function = command[0]
        if len(command) > 1:
            arg_function = command[1]
            getattr(deque, call_function)(arg_function, result)
        else:
            getattr(deque, call_function)(result)  

    for item in result:
        print (item)