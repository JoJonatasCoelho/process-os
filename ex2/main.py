import random
from task import Task

from algorithms.fifo import run_fifo
from algorithms.sjf import run_sjf
from algorithms.round_robin import run_rr
from algorithms.edf import run_edf
from algorithms.priority import run_priority

def gerar_tasks():
    tasks = []

    for i in range(5):
        duration = random.uniform(1, 5)
        deadline = random.randint(5, 20)
        priority = random.randint(1, 5)

        tasks.append(Task(i, duration, deadline, priority))

    return tasks


if __name__ == "__main__":
    tasks = gerar_tasks()

    print("\n--- FIFO ---")
    run_fifo(tasks)

    print("\n--- SJF ---")
    run_sjf(tasks)

    print("\n--- ROUND ROBIN ---")
    run_rr(tasks)

    print("\n--- EDF ---")
    run_edf(tasks)

    print("\n--- PRIORITY ---")
    run_priority(tasks)