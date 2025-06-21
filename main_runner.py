from cidade.source import get_cities
from paralelo.teste import tsp_parallel_streaming
from sequencial.teste import tsp_sequential

def run_experiments():
    results_log = []
    num_cities_tests = [8, 10, 12]  # 14 cidades pode levar muito tempo para a versão sequencial

    for num in num_cities_tests:
        print(f"\n--- Testando com {num} cidades ---\n")
        cities_data = get_cities(num)

        # --- Sequencial ---
        path_seq, dist_seq, time_seq = tsp_sequential(cities_data)
        print(f"[Sequencial] Melhor Rota: {' -> '.join(path_seq)}... -> {path_seq[0]}")
        print(f"[Sequencial] Distância: {dist_seq:.2f}")
        print(f"[Sequencial] Tempo de Execução: {time_seq:.4f} segundos")
        results_log.append({'version': 'sequential', 'cities': num, 'time': time_seq, 'distance': dist_seq})

        # --- Paralelo com Threads ---
        path_par, dist_par, time_par = tsp_parallel_streaming(cities_data,)
        print(f"\n[Paralelo Threads] Melhor Rota: {' -> '.join(path_par)}... -> {path_par[0]}")
        print(f"[Paralelo Threads] Distância: {dist_par:.2f}")
        print(f"[Paralelo Threads] Tempo de Execução: {time_par:.4f} segundos")
        results_log.append({'version': 'parallel_threads', 'cities': num, 'time': time_par, 'distance': dist_par})

        # --- Simulação Distribuída ---
        # Nota: Para executar, rode o servidor em um terminal e 4 clientes em outros 4 terminais.
        # O código abaixo simula a chamada, mas a execução real deve ser feita separadamente.
        print("\n[Distribuído Sockets] A execução deve ser feita manualmente.")
        print("1. Rode o servidor: python servidor.py")
        print("2. Rode 4 workers: python cliente.py")
        # Exemplo de resultado para a versão distribuída seria adicionado aqui
        # Ex: results_log.append({'version': 'distributed_sockets', 'cities': num, 'time': time_dist, 'distance': dist_dist})

    # --- Exportar Resultados ---
    print("\n--- Log de Resultados (JSON) ---")
    import json
    print(json.dumps(results_log, indent=2))
    return results_log

if __name__ == '__main__':
    run_experiments()