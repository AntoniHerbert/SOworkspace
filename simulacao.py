
import random
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def generate_reference_sequence(num_pages, num_references, working_set_size, working_set_duration):
    sequence = []
    current_set = set(random.sample(range(num_pages), working_set_size))
    duration_counter = working_set_duration

    for _ in range(num_references):
        if duration_counter == 0:
            current_set = set(random.sample(range(num_pages), working_set_size))
            duration_counter = working_set_duration
        
        sequence.append(random.choice(list(current_set)))
        duration_counter -= 1

    return sequence

def fifo(reference_sequence, num_frames):
    frames = deque()
    page_faults = 0

    for page in reference_sequence:
        if page not in frames:
            page_faults += 1
            if len(frames) >= num_frames:
                frames.popleft()
            frames.append(page)

    return page_faults

def aging(reference_sequence, num_frames):
    frames = {}
    page_faults = 0
    ages = {}

    for page in reference_sequence:
        for frame in frames:
            ages[frame] >>= 1

        if page not in frames:
            page_faults += 1
            if len(frames) >= num_frames:
                oldest_page = min(ages, key=ages.get)
                del frames[oldest_page]
                del ages[oldest_page]
            frames[page] = True
            ages[page] = 1 << 7
        else:
            ages[page] |= (1 << 7)

    return page_faults

def simulate():
    num_pages = 50
    num_references = 10000
    working_set_sizes = [5, 10, 15]
    working_set_durations = [100, 200, 300]
    num_frames_options = [5, 10, 15, 20, 25]

    results = []
    sequences = {}
    fifo_results = {frames: [] for frames in num_frames_options}
    aging_results = {frames: [] for frames in num_frames_options}

    for i, (working_set_size, working_set_duration) in enumerate(zip(working_set_sizes, working_set_durations)):
        sequence = generate_reference_sequence(num_pages, num_references, working_set_size, working_set_duration)
        sequences[f"Processo_{i+1}"] = sequence

        for num_frames in num_frames_options:
            fifo_faults = fifo(sequence, num_frames)
            aging_faults = aging(sequence, num_frames)

            fifo_results[num_frames].append(fifo_faults / (num_references / 1000))
            aging_results[num_frames].append(aging_faults / (num_references / 1000))

            results.append({
                "processo": f"Processo_{i+1}",
                "molduras": num_frames,
                "fifo": fifo_faults / (num_references / 1000),
                "aging": aging_faults / (num_references / 1000),
            })

    with open("sequences.json", "w") as seq_file:
        json.dump(sequences, seq_file, indent=4)

    with open("results.json", "w") as res_file:
        json.dump(results, res_file, indent=4)

    # Gerar gráficos em subplots para todos os num_frames
    fig, axes = plt.subplots(len(num_frames_options), 1, figsize=(12, 6 * len(num_frames_options)))  # Aumentar a largura

    if len(num_frames_options) == 1:
        axes = [axes]  # Para garantir que axes sempre seja uma lista, mesmo com 1 subplot

    for i, num_frames in enumerate(num_frames_options):
        x = np.arange(len(working_set_sizes))  # Posições no eixo X
        width = 0.4  # Largura das barras

        axes[i].bar(x - width/2, fifo_results[num_frames], width, label=f"FIFO", alpha=0.7)
        axes[i].bar(x + width/2, aging_results[num_frames], width, label=f"Aging", alpha=0.7)

        axes[i].set_xlabel("Configuração do Conjunto de Trabalho")
        axes[i].set_ylabel("Faltas de Página por 1000 Referências")
        axes[i].set_title(f"Comparação FIFO vs Aging ({num_frames} molduras)")
        axes[i].set_xticks(x)
        axes[i].set_xticklabels([f"Set {i+1}" for i in range(len(working_set_sizes))])
        axes[i].legend()
        axes[i].grid(axis='y', linestyle='--', alpha=0.7)

        # Rotacionar os rótulos no eixo X para evitar sobreposição
        plt.setp(axes[i].get_xticklabels(), rotation=45, ha="right")

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    plt.show()

if __name__ == "__main__":
    simulate()

