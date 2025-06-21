import time
import itertools

from cidade.source import total_distance

def tsp_sequential(cities_coords):
    """Resolve o TSP usando uma abordagem de força bruta sequencial."""
    start_time = time.perf_counter()

    city_names = list(cities_coords.keys())
    start_city = city_names[0]
    other_cities = city_names[1:]

    best_path = None
    min_distance = float('inf')

    # Gera todas as permutações das outras cidades
    for permutation in itertools.permutations(other_cities):
        current_path = (start_city,) + permutation
        current_distance = total_distance(current_path, cities_coords)

        if current_distance < min_distance:
            min_distance = current_distance
            best_path = current_path

    end_time = time.perf_counter()

    return best_path, min_distance, end_time - start_time