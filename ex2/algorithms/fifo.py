from queue import Queue
from utils import executar_task

def run_fifo(tasks):
    fila = Queue()

    for t in tasks:
        fila.put(t)

    while not fila.empty():
        task = fila.get()
        executar_task(task, "FIFO")