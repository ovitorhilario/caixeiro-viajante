import time
import socket
import pickle
import struct
import threading
import math

from cidade.source import get_cities

# Envia dados com tamanho prefixado (necessário para comunicação via socket)
def send_with_size(conn, data):
    size = struct.pack('!I', len(data))  # Empacota o tamanho como um inteiro de 4 bytes
    conn.sendall(size)
    conn.sendall(data)

# Recebe dados com tamanho prefixado
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

# Função executada por cada thread do servidor, que gerencia a comunicação com um worker
def handle_worker(conn, start_index, chunk_size, start_city, cities_coords, other_cities, results, lock, worker_id):
    try:
        print(f"[Thread {worker_id}] Enviando dados básicos e intervalo...")

        # Dados a serem enviados ao worker para o processamento
        payload = pickle.dumps({
            'start_city': start_city,
            'cities_coords': cities_coords,
            'other_cities': other_cities,
            'start_index': start_index,
            'chunk_size': chunk_size
        })
        send_with_size(conn, payload)

        print(f"[Thread {worker_id}] Dados enviados. Aguardando resultado...")

        # Recebe o resultado do worker (melhor caminho e distância)
        data = recv_with_size(conn)
        result = pickle.loads(data)

        # Adiciona resultado com segurança (uso de trava para acesso concorrente)
        with lock:
            results.append(result)

        print(f"[Thread {worker_id}] Resultado recebido.")
    except Exception as e:
        print(f"[Thread {worker_id}] Erro: {e}")
    finally:
        conn.close()  # Garante o fechamento da conexão

# Função principal que gerencia o servidor distribuído para resolver o problema do Caixeiro Viajante
def tsp_distributed_server(cities_coords, num_workers, host='127.0.0.1', port=65432):
    city_names = list(cities_coords.keys())
    start_city = city_names[0]  # Define a cidade inicial
    other_cities = city_names[1:]  # As outras cidades a serem visitadas

    # Cálculo do total de permutações possíveis (exceto a cidade inicial)
    total_permutations = math.factorial(len(other_cities))
    chunk_size = total_permutations // num_workers  # Quantidade de permutações por worker

    results = []  # Lista onde os workers vão guardar seus melhores caminhos
    lock = threading.Lock()  # Trava para evitar concorrência simultânea
    threads = []
    connections = []

    # Inicia o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(num_workers)
        print(f"Servidor ouvindo em {host}:{port}")

        # Etapa 1: Espera todos os workers se conectarem
        for i in range(num_workers):
            print(f"Aguardando conexão do worker {i+1}...")
            conn, addr = s.accept()
            print(f"Worker {i+1} conectado de {addr}")
            connections.append(conn)

        start_time = time.perf_counter()

        print("\nTodos os workers conectados! Iniciando envio das tarefas...\n")

        # Etapa 2: Cria threads para enviar tarefas e aguardar os resultados
        for i, conn in enumerate(connections):
            start_index = i * chunk_size

            # O último worker recebe o que sobrar
            if i == num_workers - 1:
                this_chunk_size = total_permutations - start_index
            else:
                this_chunk_size = chunk_size

            # Cria e inicia a thread do worker
            thread = threading.Thread(
                target=handle_worker,
                args=(conn, start_index, this_chunk_size, start_city, cities_coords, other_cities, results, lock, i+1)
            )
            thread.start()
            threads.append(thread)

        # Espera todas as threads terminarem
        for thread in threads:
            thread.join()

    # Consolidação final: encontra o menor caminho entre os resultados recebidos
    best_path = None
    min_distance = float('inf')
    for path, dist in results:
        if dist < min_distance:
            min_distance = dist
            best_path = path

    end_time = time.perf_counter()

    # Exibe a melhor rota e tempo de execução total
    print(f"Melhor rota: {' -> '.join(best_path)}... -> {best_path[0]} com distância {min_distance}")
    print(f"Tempo total: {end_time - start_time:.2f} segundos")

    return best_path, min_distance, end_time - start_time

# Executa o servidor diretamente se o script for chamado
if __name__ == "__main__":
    cities_data = get_cities(12)  # Gera 12 cidades com coordenadas fictícias
    tsp_distributed_server(cities_data, num_workers=2, host='127.0.0.1', port=65432)
