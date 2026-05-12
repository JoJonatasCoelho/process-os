import time
from resources import compilador, banco_dados

def executar_task(task, algoritmo):
    banco_dados.acquire()
    compilador.acquire()

    print(f"[{algoritmo}] P{task.id} compilando ({task.duration:.2f}s)")

    time.sleep(task.duration)

    compilador.release()
    banco_dados.release()

    print(f"[{algoritmo}] P{task.id} terminou")