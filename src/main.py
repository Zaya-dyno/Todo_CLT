from todo import Todo
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename="data/log",
                    filemode="w")

if __name__ == "__main__":
    todo = Todo()
    todo.run()
