from queue import PriorityQueue
from utils import executar_task

def run_edf(tasks):
    fila = PriorityQueue()

    for t in tasks:
        fila.put((t.deadline, t))

    while not fila.empty():
        _, task = fila.get()
        executar_task(task, "EDF")