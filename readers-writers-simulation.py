import threading
import time
import random

class SharedResource:
    def __init__(self):
        self.data = 0
        self.readers = 0
        self.mutex = threading.Lock()
        self.resource = threading.Lock()
        self.waiting_writers = 0
        self.reader_wait_times = []
        self.writer_wait_times = []
        self.reader_access_count = 0
        self.writer_access_count = 0


class Solution1:
    def __init__(self):
        self.shared = SharedResource()

    def reader(self, reader_id):
        while True:
            start_time = time.time()
            with self.shared.mutex:
                self.shared.readers += 1
                if self.shared.readers == 1:
                    self.shared.resource.acquire()
            
            wait_time = time.time() - start_time
            self.shared.reader_wait_times.append(wait_time)

            print(f"Leitor {reader_id} lendo valor: {self.shared.data}")
            self.shared.reader_access_count += 1
            time.sleep(random.uniform(0.1, 0.5))    

            with self.shared.mutex:
                self.shared.readers -= 1
                if self.shared.readers == 0:
                    self.shared.resource.release()

            time.sleep(random.uniform(0.1, 0.5))  

    def writer(self, writer_id):
        while True:
            start_time = time.time()
            with self.shared.resource:
                wait_time = time.time() - start_time
                self.shared.writer_wait_times.append(wait_time)
                # Escrita
                self.shared.data += 1
                print(f"Escritor {writer_id} escreveu valor: {self.shared.data}")
                self.shared.writer_access_count += 1
                time.sleep(random.uniform(0.1, 0.5))    

            time.sleep(random.uniform(0.1, 0.5))    


class Solution2:
    def __init__(self):
        self.shared = SharedResource()

    def reader(self, reader_id):
        while True:
            start_time = time.time()
            with self.shared.mutex:
                while self.shared.waiting_writers > 0:
                    self.shared.mutex.release()
                    time.sleep(random.uniform(0.1, 0.5))
                    self.shared.mutex.acquire()

                self.shared.readers += 1
                if self.shared.readers == 1:
                    self.shared.resource.acquire()
            
            wait_time = time.time() - start_time
            self.shared.reader_wait_times.append(wait_time)

            print(f"Leitor {reader_id} lendo valor: {self.shared.data}")
            self.shared.reader_access_count += 1
            time.sleep(random.uniform(0.1, 0.5))    

            with self.shared.mutex:
                self.shared.readers -= 1
                if self.shared.readers == 0:
                    self.shared.resource.release()

            time.sleep(random.uniform(0.1, 0.5))    

    def writer(self, writer_id):
        while True:
            start_time = time.time()
            with self.shared.mutex:
                self.shared.waiting_writers += 1

            with self.shared.resource:
                with self.shared.mutex:
                    self.shared.waiting_writers -= 1
                wait_time = time.time() - start_time
                self.shared.writer_wait_times.append(wait_time)

                self.shared.data += 1
                print(f"Writer {writer_id} escreveu valor: {self.shared.data}")
                self.shared.writer_access_count += 1
                time.sleep(random.uniform(0.1, 0.5))    

            time.sleep(random.uniform(0.1, 0.5))    


def run_simulation(solution_class, num_readers, num_writers, duration):
    solution = solution_class()
    threads = []

    for i in range(num_readers):
        t = threading.Thread(target=solution.reader, args=(i,))
        threads.append(t)
        t.daemon = True
        t.start()

    for i in range(num_writers):
        t = threading.Thread(target=solution.writer, args=(i,))
        threads.append(t)
        t.daemon = True
        t.start()

    time.sleep(duration)  
    return solution.shared

print("Executando Solução 1 (escritores podem ter starve)")
shared_resource_1 = run_simulation(Solution1, 3, 2, 10)
print(f"\nValor final da solução 1: {shared_resource_1.data}")
print(f"Tempo médio de espera dos leitores: {sum(shared_resource_1.reader_wait_times)/len(shared_resource_1.reader_wait_times) if shared_resource_1.reader_wait_times else 0}")
print(f"Tempo médio de espera dos escritores: {sum(shared_resource_1.writer_wait_times)/len(shared_resource_1.writer_wait_times) if shared_resource_1.writer_wait_times else 0}")
print(f"Número de acessos dos leitores: {shared_resource_1.reader_access_count}")
print(f"Número de acessos dos escritores: {shared_resource_1.writer_access_count}\n")

print("Executando Solução 2 (escritores não tem starve)")
shared_resource_2 = run_simulation(Solution2, 3, 2, 10)
print(f"\nValor final da solução 2: {shared_resource_2.data}")
print(f"Tempo médio de espera dos leitores: {sum(shared_resource_2.reader_wait_times)/len(shared_resource_2.reader_wait_times) if shared_resource_2.reader_wait_times else 0}")
print(f"Tempo médio de espera dos escritores: {sum(shared_resource_2.writer_wait_times)/len(shared_resource_2.writer_wait_times) if shared_resource_2.writer_wait_times else 0}")
print(f"Número de acessos dos leitores: {shared_resource_2.reader_access_count}")
print(f"Número de acessos dos escritores: {shared_resource_2.writer_access_count}")
