import socket
import pickle
import struct
from itertools import islice, permutations
from cidade.source import total_distance

# Função para enviar dados com tamanho prefixado
def send_with_size(conn, data):
    size = struct.pack('!I', len(data))  # Empacota o tamanho do dado (4 bytes)
    conn.sendall(size)
    conn.sendall(data)

# Função para receber dados com tamanho prefixado
def recv_with_size(conn):
    size_data = conn.recv(4)
    if not size_data:
        return None
    size = struct.unpack('!I', size_data)[0]

    data = b''
    while len(data) < size:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    return data

# Função que encontra o melhor caminho (menor distância) dentro de um intervalo de permutações
def find_best_path_in_chunk_sequential(start_index, chunk_size, start_city, other_cities, cities_coords):
    best_path = None
    min_distance = float('inf')

    # Gera apenas um "pedaço" das permutações totais, a partir do índice fornecido
    perm_gen = islice(permutations(other_cities), start_index, start_index + chunk_size)

    for perm in perm_gen:
        full_path = [start_city] + list(perm)
        distance = total_distance(full_path, cities_coords)

        if distance < min_distance:
            min_distance = distance
            best_path = full_path

    return best_path, min_distance

# Cliente que atua como worker para resolver parte do problema do Caixeiro Viajante
def tsp_worker_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # Conecta ao servidor

        # Recebe os dados da tarefa do servidor
        data = recv_with_size(s)
        task_info = pickle.loads(data)

        # Extrai as informações da tarefa
        start_city = task_info['start_city']
        cities_coords = task_info['cities_coords']
        other_cities = task_info['other_cities']
        start_index = task_info['start_index']
        chunk_size = task_info['chunk_size']

        print(f"Worker recebendo intervalo: start={start_index}, size={chunk_size}")

        # Executa o processamento local (sequencial) no intervalo recebido
        best_path, min_distance = find_best_path_in_chunk_sequential(
            start_index,
            chunk_size,
            start_city,
            other_cities,
            cities_coords
        )

        # Envia o melhor resultado encontrado de volta ao servidor
        payload = pickle.dumps((best_path, min_distance))
        send_with_size(s, payload)
        print(f"Worker finalizou! Melhor distância local: {min_distance}")

# Executa o cliente worker quando o script é chamado diretamente
if __name__ == "__main__":
    tsp_worker_client()
