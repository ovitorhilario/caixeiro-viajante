import time
import itertools

from cidade.source import total_distance

def tsp_sequential(cities_coords):
    """Resolve o Problema do Caixeiro Viajante (TSP) usando força bruta sequencial."""
    start_time = time.perf_counter()  # Marca o tempo inicial

    city_names = list(cities_coords.keys())  # Lista com os nomes das cidades
    start_city = city_names[0]               # Define a cidade inicial como a primeira da lista
    other_cities = city_names[1:]            # As demais cidades serão permutadas

    best_path = None
    min_distance = float('inf')  # Inicia com uma distância infinita para comparação

    # Gera todas as permutações possíveis das cidades (exceto a inicial)
    for permutation in itertools.permutations(other_cities):
        current_path = (start_city,) + permutation  # Monta o caminho completo com cidade inicial
        current_distance = total_distance(current_path, cities_coords)  # Calcula a distância desse caminho

        # Se encontrar um caminho com menor distância, atualiza o melhor caminho
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = current_path

    end_time = time.perf_counter()  # Marca o tempo final da execução

    # Retorna o melhor caminho encontrado, a distância mínima e o tempo total gasto
    return best_path, min_distance, end_time - start_time
