from collections import deque
from utils import executar_task
import time

def run_rr(tasks, quantum=2):
    fila = deque([[t, t.duration] for t in tasks])

    while fila:
        task, restante = fila.popleft()

        exec_time = min(quantum, restante)

        print(f"[RR] P{task.id} executando {exec_time}s")

        time.sleep(exec_time)
        restante -= exec_time

        if restante > 0:
            fila.append([task, restante])
        else:
            executar_task(task, "RR")