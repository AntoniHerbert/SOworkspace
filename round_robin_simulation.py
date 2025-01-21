import numpy as np
import matplotlib.pyplot as plt


def round_robin(processes, burst_times, quantum, context_switch=1):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    remaining_times = burst_times[:]
    sequence = []

    time = 0
    while any(remaining > 0 for remaining in remaining_times):
        for i in range(n):
            if remaining_times[i] > 0:
                sequence.append(processes[i])
                exec_time = min(quantum, remaining_times[i])
                time += exec_time
                remaining_times[i] -= exec_time

                # adiciona tempo de troca de contexto se o processo não tiver sido concluído
                if remaining_times[i] > 0:
                    time += context_switch

                # atualiza tempo de espera para outros contextos
                for j in range(n):
                    if j != i and remaining_times[j] > 0:
                        waiting_times[j] += exec_time + (context_switch if remaining_times[i] > 0 else 0)

    # calcula tempos de retorno
    for i in range(n):
        turnaround_times[i] = waiting_times[i] + burst_times[i]

    return waiting_times, turnaround_times, sequence

def simulate_round_robin(num_processes, burst_time_range, quantum_values):
    processes = [f"P{i+1}" for i in range(num_processes)]
    burst_times = np.random.randint(burst_time_range[0], burst_time_range[1] + 1, size=num_processes).tolist()

    results = {}

    for quantum in quantum_values:
        waiting_times, turnaround_times, sequence = round_robin(processes, burst_times, quantum)

        avg_waiting_time = np.mean(waiting_times)
        std_waiting_time = np.std(waiting_times)

        avg_turnaround_time = np.mean(turnaround_times)
        std_turnaround_time = np.std(turnaround_times)

        throughput = num_processes / (sum(turnaround_times) / num_processes)

        results[quantum] = {
            "sequence": sequence,
            "avg_waiting_time": avg_waiting_time,
            "std_waiting_time": std_waiting_time,
            "avg_turnaround_time": avg_turnaround_time,
            "std_turnaround_time": std_turnaround_time,
            "throughput": throughput,
        }

    return processes, burst_times, results

def plot_results(quantum_values, results):
    avg_waiting_times = [results[q]["avg_waiting_time"] for q in quantum_values]
    avg_turnaround_times = [results[q]["avg_turnaround_time"] for q in quantum_values]
    throughputs = [results[q]["throughput"] for q in quantum_values]

    plt.figure(figsize=(12, 6))

    # Subplot 1: Tempo Médio de Espera
    plt.subplot(1, 3, 1)
    plt.plot(quantum_values, avg_waiting_times, marker='o', label="Tempo Médio de Espera")
    plt.xlabel("Quantum")
    plt.ylabel("Tempo Médio de Espera")
    plt.title("Tempo Médio de Espera vs Quantum")
    plt.grid()

    # Subplot 2: Tempo Médio de Retorno
    plt.subplot(1, 3, 2)
    plt.plot(quantum_values, avg_turnaround_times, marker='o', color='g', label="Tempo Médio de Retorno")
    plt.xlabel("Quantum")
    plt.ylabel("Tempo Médio de Retorno")
    plt.title("Tempo Médio de Retorno vs Quantum")
    plt.grid()

    # Subplot 3: Vazão
    plt.subplot(1, 3, 3)
    plt.plot(quantum_values, throughputs, marker='o', color='r', label="Vazão")
    plt.xlabel("Quantum")
    plt.ylabel("Vazão")
    plt.title("Vazão vs Quantum")
    plt.grid()

    plt.tight_layout()
    plt.show()


def main():
    num_processes = 5
    burst_time_range = (100, 200)  # Burst times entre 5 and 20
    quantum_values = list(range(50, 301, 1)) #valores de quantum para testar

    processes, burst_times, results = simulate_round_robin(num_processes, burst_time_range, quantum_values)

    print("Processos:", processes)
    print("Burst Times:", burst_times)

    for quantum, metrics in results.items():
        print(f"\nQuantum: {quantum}")
        print("Sequencia de execução:", " -> ".join(metrics["sequence"]))
        print(f"Tempo médio de espera: {metrics['avg_waiting_time']:.2f} +/- {metrics['std_waiting_time']:.2f}")
        print(f"Tempo médio de retorno: {metrics['avg_turnaround_time']:.2f} +/- {metrics['std_turnaround_time']:.2f}")
        print(f"Vazão: {metrics['throughput']:.2f} processos/unidade de tempo")

    plot_results(quantum_values, results)


if __name__ == "__main__":
    main()
