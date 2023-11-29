from todo import Todo
from functools import partial

printf = partial(print,end='')

if __name__ == "__main__":
    todo = Todo()
    todo.run()
