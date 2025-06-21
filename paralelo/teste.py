import itertools
import time
from multiprocessing import Pool, cpu_count
from cidade.source import total_distance

def find_best_path_chunk(chunk, start_city, cities_coords):
    """
    Função auxiliar (não utilizada nesse script) que encontraria o melhor caminho dentro de um grupo (chunk)
    de permutações. Pode ser usada em abordagens que dividem em blocos maiores.
    """
    local_best_path = None
    local_min_distance = float('inf')

    for permutation in chunk:
        current_path = (start_city,) + permutation
        current_distance = total_distance(current_path, cities_coords)

        if current_distance < local_min_distance:
            local_min_distance = current_distance
            local_best_path = current_path

    return local_best_path, local_min_distance

def evaluate_path(permutation_data):
    """
    Função executada por cada processo.
    Recebe uma permutação, monta o caminho completo e calcula sua distância total.
    """
    permutation, start_city, cities_coords = permutation_data
    current_path = (start_city,) + permutation
    current_distance = total_distance(current_path, cities_coords)
    return current_path, current_distance

# ---------- Função principal ----------
def tsp_parallel_streaming(cities_coords, num_processes=2):
    """
    Resolve o Problema do Caixeiro Viajante (TSP) usando processamento paralelo.
    Divide as permutações entre múltiplos processos usando pool de workers.
    """
    start_time = time.perf_counter()  # Marca o tempo inicial da execução

    city_names = list(cities_coords.keys())
    start_city = city_names[0]        # Cidade inicial fixa
    other_cities = city_names[1:]     # Cidades restantes para permutar

    best_path = None
    min_distance = float('inf')

    # Gera todas as permutações possíveis das cidades (exceto a inicial)
    perms = itertools.permutations(other_cities)

    # Gera os dados que cada processo irá processar (cada permutação vira uma tarefa)
    def data_generator():
        for perm in perms:
            yield (perm, start_city, cities_coords)

    # Cria um pool de processos e distribui as tarefas de forma contínua com imap
    with Pool(processes=num_processes) as pool:
        # O chunksize define quantas permutações são enviadas de uma vez para cada processo
        for current_path, current_distance in pool.imap(evaluate_path, data_generator(), chunksize=4000):
            if current_distance < min_distance:
                min_distance = current_distance
                best_path = current_path

    end_time = time.perf_counter()  # Marca o tempo final

    # Retorna o melhor caminho, a menor distância e o tempo total de execução
    return best_path, min_distance, end_time - start_time
