from todo import Todo
import logging
from curses import wrapper
import signal
logging.basicConfig(level=logging.DEBUG,
                    filename="data/log",
                    filemode="w")

def main(scr):
    todo = Todo(scr)
    todo.run()

if __name__ == "__main__":
    wrapper(main)

