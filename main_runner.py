from cidade.source import get_cities
from paralelo.teste import tsp_parallel_streaming
from sequencial.teste import tsp_sequential

def run_experiments():
    results_log = []  # Lista para armazenar os resultados dos testes
    num_cities_tests = [8, 10, 12]  # Número de cidades para os testes. Evita 14+ por demora na versão sequencial
    processes = 2  # Número de núcleos (processos paralelos) utilizados no teste paralelo

    # Loop de execução dos testes para cada quantidade de cidades
    for num in num_cities_tests:
        print(f"\n--- Testando com {num} cidades ---\n")
        cities_data = get_cities(num)  # Gera os dados das cidades

        # --- Execução Sequencial ---
        path_seq, dist_seq, time_seq = tsp_sequential(cities_data)
        print(f"[Sequencial] Melhor Rota: {' -> '.join(path_seq)}... -> {path_seq[0]}")
        print(f"[Sequencial] Distância: {dist_seq:.2f}")
        print(f"[Sequencial] Tempo de Execução: {time_seq:.4f} segundos")
        results_log.append({
            'version': 'sequential',
            'cities': num,
            'time': time_seq,
            'distance': dist_seq
        })

        # --- Execução Paralela com Threads (ou processos, dependendo da implementação) ---
        path_par, dist_par, time_par = tsp_parallel_streaming(cities_data, processes)
        print(f"[Paralelo Threads] Melhor Rota: {' -> '.join(path_par)}... -> {path_par[0]}")
        print(f"[Paralelo Threads] Distância: {dist_par:.2f}")
        print(f"[Paralelo Threads] Tempo de Execução: {time_par:.4f} segundos")
        results_log.append({
            'version': 'parallel_threads',
            'cities': num,
            'time': time_par,
            'distance': dist_par
        })

        # --- Execução Distribuída (Comentada) ---
        # Esta parte deve ser executada separadamente usando um servidor e múltiplos clientes.
        # Instruções:
        # 1. Rode o servidor: python distribuido_servidor.py
        # 2. Rode dois clientes (workers): python distribuido_cliente.py

    # --- Exibição dos Resultados em formato JSON ---
    print("\n--- Log de Resultados (JSON) ---")
    import json
    print(json.dumps(results_log, indent=2))  # Exibe os resultados formatados em JSON

    return results_log  # Retorna os dados dos testes (útil para salvar ou analisar posteriormente)

# Ponto de entrada principal do script
if __name__ == '__main__':
    run_experiments()
