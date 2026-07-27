import time
import random
from collections import defaultdict, deque
from grafo_puno import GrafoPuno, componentes_conexas, RUTAS_PUNO

print("=== Benchmark Python: red vial de Puno (14 ciudades) ===")
t0 = time.perf_counter()
g = GrafoPuno(14)
for u, v, p in RUTAS_PUNO:
    g.agregar_arista(u, v, p)
ms_construccion = (time.perf_counter() - t0) * 1000
print(f'Tiempo de construccion del grafo (14 ciudades): {ms_construccion:.6f} ms')

t0 = time.perf_counter()
comp = componentes_conexas(g)
ms_comp = (time.perf_counter() - t0) * 1000
print(f'Componentes (sin bloqueos): {len(comp)} (calculado en {ms_comp:.6f} ms)')

t0 = time.perf_counter()
comp_lluvia = componentes_conexas(g, vertices_excluidos={12, 13})
ms_comp_lluvia = (time.perf_counter() - t0) * 1000
print(f'Componentes (Macusani/Sandia bloqueadas): {len(comp_lluvia)} (calculado en {ms_comp_lluvia:.6f} ms)')


def grafo_disperso(n, grado_promedio, rng):
    g = GrafoPuno(n)
    aristas_objetivo = int(n * grado_promedio / 2)
    for _ in range(aristas_objetivo):
        u, v = rng.randint(0, n - 1), rng.randint(0, n - 1)
        if u != v:
            g.agregar_arista(u, v, rng.randint(10, 200))
    return g


print("\n=== Benchmark a escala (grafos dispersos aleatorios, grado promedio ~2.3) ===")
rng = random.Random(42)
for n in [1000, 10000, 100000, 1000000]:
    t0 = time.perf_counter()
    g_grande = grafo_disperso(n, 2.3, rng)
    ms_const = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    comp_grande = componentes_conexas(g_grande)
    ms_comp = (time.perf_counter() - t0) * 1000

    print(f'n={n} | construccion={ms_const:.3f}ms | componentes={len(comp_grande)} en {ms_comp:.3f}ms')
