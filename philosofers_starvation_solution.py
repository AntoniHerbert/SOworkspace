import threading
import time
import random

# Número de filósofos e palitos
NUM_PHILOSOPHERS = 5
NUM_MEALS = 1000

# Semáforo para cada palito
chopsticks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

# Função do filósofo
def philosopher(phil_id, meals_to_eat):
    left = phil_id
    right = (phil_id + 1) % NUM_PHILOSOPHERS

    for _ in range(meals_to_eat):
        print(f"Filósofo {phil_id} está pensando.")
        time.sleep(random.uniform(0.5, 2))  # Pensar por um tempo aleatório

        # Pegar os palitos (evitar deadlock com ordem hierárquica)
        if phil_id % 2 == 0:
            chopsticks[left].acquire()
            chopsticks[right].acquire()
        else:
            chopsticks[right].acquire()
            chopsticks[left].acquire()

        # Comer
        print(f"Filósofo {phil_id} está comendo.")
        time.sleep(random.uniform(1, 3))  # Comer por um tempo aleatório

        # Soltar os palitos
        chopsticks[left].release()
        chopsticks[right].release()
        print(f"Filósofo {phil_id} terminou de comer e devolveu os palitos.")

# Inicialização e execução das threads
if __name__ == "__main__":
    philosophers = []
    meals_per_philosopher = NUM_MEALS

    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i, meals_per_philosopher))
        philosophers.append(t)
        t.start()

    for t in philosophers:
        t.join()

    print("Todos os filósofos terminaram de comer.")
