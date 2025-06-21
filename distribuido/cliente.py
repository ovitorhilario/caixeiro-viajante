import socket
import pickle
import struct
from itertools import islice, permutations
from cidade.source import total_distance

def send_with_size(conn, data):
    size = struct.pack('!I', len(data))
    conn.sendall(size)
    conn.sendall(data)

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

def find_best_path_in_chunk_sequential(start_index, chunk_size, start_city, other_cities, cities_coords):
    best_path = None
    min_distance = float('inf')

    # Gera apenas as permutações entre start_index e start_index + chunk_size
    perm_gen = islice(permutations(other_cities), start_index, start_index + chunk_size)

    for perm in perm_gen:
        full_path = [start_city] + list(perm)
        distance = total_distance(full_path, cities_coords)

        if distance < min_distance:
            min_distance = distance
            best_path = full_path

    return best_path, min_distance

def tsp_worker_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Recebe o pacote inicial com todas as informações da tarefa
        data = recv_with_size(s)
        task_info = pickle.loads(data)

        start_city = task_info['start_city']
        cities_coords = task_info['cities_coords']
        other_cities = task_info['other_cities']
        start_index = task_info['start_index']
        chunk_size = task_info['chunk_size']

        print(f"Worker recebendo intervalo: start={start_index}, size={chunk_size}")

        # Processa o intervalo SEQUENCIALMENTE
        best_path, min_distance = find_best_path_in_chunk_sequential(
            start_index,
            chunk_size,
            start_city,
            other_cities,
            cities_coords
        )

        # Envia o resultado de volta ao servidor
        payload = pickle.dumps((best_path, min_distance))
        send_with_size(s, payload)
        print(f"Worker finalizou! Melhor distância local: {min_distance}")

if __name__ == "__main__":
    tsp_worker_client()