import math
import itertools

# Coordenadas das cidades (latitude, longitude aproximadas)
# As cidades são armazenadas em um dicionário, com identificadores de 'A' até 'O'
CITIES = {
    'A': (40.7128, -74.0060), 'B': (34.0522, -118.2437), 'C': (41.8781, -87.6298),
    'D': (29.7604, -95.3698), 'E': (39.9526, -75.1652), 'F': (33.4484, -112.0740),
    'G': (47.6062, -122.3321), 'H': (39.7392, -104.9903), 'I': (36.1699, -115.1398),
    'J': (25.7617, -80.1918), 'K': (30.2672, -97.7431), 'L': (32.7767, -96.7970),
    'M': (38.9072, -77.0369), 'N': (48.8566, 12.3522),  'O': (35.6895, 139.6917)
}

def get_cities(num_cities):
    """
    Retorna um subconjunto com as 'num_cities' primeiras cidades da lista.
    Útil para testar o algoritmo com diferentes tamanhos de entrada.
    """
    return dict(itertools.islice(CITIES.items(), num_cities))

def calculate_distance(city1_coords, city2_coords):
    """
    Calcula a distância euclidiana entre duas cidades com base nas coordenadas geográficas.
    Fórmula: raiz quadrada da soma dos quadrados das diferenças de latitude e longitude.
    """
    return math.sqrt((city1_coords[0] - city2_coords[0])**2 + (city1_coords[1] - city2_coords[1])**2)

def total_distance(path, cities_coords):
    """
    Calcula a distância total de um caminho (rota) que passa por todas as cidades e retorna à cidade inicial.
    """
    dist = 0
    for i in range(len(path) - 1):
        dist += calculate_distance(cities_coords[path[i]], cities_coords[path[i+1]])
    # Fecha o ciclo: volta da última cidade para a cidade inicial
    dist += calculate_distance(cities_coords[path[-1]], cities_coords[path[0]])
    return dist
