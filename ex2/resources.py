import threading

# 1 compilador (exclusivo)
compilador = threading.Semaphore(1)

# 2 acessos simultâneos ao banco
banco_dados = threading.Semaphore(2)