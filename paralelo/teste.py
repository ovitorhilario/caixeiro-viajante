import itertools
import time
from multiprocessing import Pool, cpu_count
from cidade.source import total_distance

def find_best_path_chunk(chunk, start_city, cities_coords):
    """Função que cada thread executará para encontrar o melhor caminho em um 'chunk' de permutações."""
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
    """Função para avaliar uma permutação individual (executada em paralelo)."""
    permutation, start_city, cities_coords = permutation_data
    current_path = (start_city,) + permutation
    current_distance = total_distance(current_path, cities_coords)
    return current_path, current_distance

# ---------- Função principal ----------
def tsp_parallel_streaming(cities_coords, num_processes=2):
    start_time = time.perf_counter()


    city_names = list(cities_coords.keys())
    start_city = city_names[0]
    other_cities = city_names[1:]

    best_path = None
    min_distance = float('inf')

    # Prepara o gerador de permutações (não carrega tudo na memória)
    perms = itertools.permutations(other_cities)

    # Empacota os dados que serão enviados para os workers
    def data_generator():
        for perm in perms:
            yield (perm, start_city, cities_coords)

    with Pool(processes=num_processes) as pool:
        for current_path, current_distance in pool.imap(evaluate_path, data_generator(), chunksize=4000):
            if current_distance < min_distance:
                min_distance = current_distance
                best_path = current_path

    end_time = time.perf_counter()

    return best_path, min_distance, end_time - start_time