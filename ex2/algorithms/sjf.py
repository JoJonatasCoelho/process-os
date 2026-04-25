from queue import PriorityQueue
from utils import executar_task

def run_sjf(tasks):
    fila = PriorityQueue()

    for t in tasks:
        fila.put((t.duration, t))

    while not fila.empty():
        _, task = fila.get()
        executar_task(task, "SJF")