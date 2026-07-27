import sys
import numpy as np
import random
from collections import defaultdict
from grafo_puno import GrafoPuno, construir_grafo_puno, componentes_conexas

print("=== Extension: ¿por que la matriz salio MAS PEQUENA que la lista en la Actividad 2? ===\n")
print("Con solo 14 nodos, el overhead por objeto de Python (cada tupla, cada lista)")
print("pesa mas que la ventaja asintotica O(V+E) vs O(V^2). Se prueba el mismo grafo")
print("disperso (misma densidad relativa) a mayor escala para encontrar el punto de cruce.\n")


def grafo_disperso_aleatorio(n, grado_promedio=2.3, semilla=42):
    """Genera un grafo aleatorio disperso con densidad similar a la red de Puno."""
    random.seed(semilla)
    g = GrafoPuno(n)
    aristas_objetivo = int(n * grado_promedio / 2)
    intentos = 0
    while g.naristas < aristas_objetivo and intentos < aristas_objetivo * 20:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        intentos += 1
        if u != v and not any(vv == v for vv, _ in g.adj[u]):
            g.agregar_arista(u, v, random.randint(10, 200))
    return g


def medir_memoria(g):
    tam_lista = sys.getsizeof(g.adj) + sum(sys.getsizeof(v) for v in g.adj.values())
    M = np.full((g.n, g.n), np.inf, dtype=np.float64)
    tam_matriz = M.nbytes
    return tam_lista, tam_matriz


print(f'{"N":>8} {"Lista (bytes)":>15} {"Matriz (bytes)":>15} {"Razon M/L":>12} {"Gana":>8}')
for n in [14, 50, 100, 500, 1000, 5000]:
    g = grafo_disperso_aleatorio(n)
    tam_lista, tam_matriz = medir_memoria(g)
    razon = tam_matriz / tam_lista
    gana = "Matriz" if razon < 1 else "Lista"
    print(f'{n:>8} {tam_lista:>15,} {tam_matriz:>15,} {razon:>11.2f}x {gana:>8}')

print("\n=== Pregunta de Reflexion 3: bloquear SOLO Macusani (12), sin tocar Sandia (13) ===\n")
g = construir_grafo_puno()
print('Vecinos de Macusani (12):', [(g.CIUDADES[v], p) for v, p in g.adj[12]])
print('Vecinos de Sandia (13):  ', [(g.CIUDADES[v], p) for v, p in g.adj[13]])

comp_solo_macusani = componentes_conexas(g, vertices_excluidos={12})
print(f'\nBloqueando SOLO Macusani(12): {len(comp_solo_macusani)} componentes conexas')
for c in comp_solo_macusani:
    print(f'  {[g.CIUDADES[v] for v in c]}')

sandia_aislada = all(len(c) == 1 and g.CIUDADES[c[0]] == 'Sandia' or 'Sandia' not in [g.CIUDADES[x] for x in c]
                      for c in comp_solo_macusani)
sandia_en_componente_grande = any('Sandia' in [g.CIUDADES[x] for x in c] and len(c) > 1 for c in comp_solo_macusani)
print(f'\n¿Sandia quedo aislada al bloquear SOLO Macusani? '
      f'{"NO, sigue conectada" if sandia_en_componente_grande else "SI, quedo aislada"}')
