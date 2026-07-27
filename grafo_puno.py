# ── Actividad 1: GrafoPuno — lista de adyacencia ────────────────────────
from collections import defaultdict, deque


class GrafoPuno:
    CIUDADES = {0: 'Puno', 1: 'Juliaca', 2: 'Ilave', 3: 'Desaguadero', 4: 'Yunguyo',
                5: 'Juli', 6: 'Lampa', 7: 'Azangaro', 8: 'Huancane', 9: 'Moho',
                10: 'Putina', 11: 'Ayaviri', 12: 'Macusani', 13: 'Sandia'}
    RIESGO = {0: 'bajo', 1: 'bajo', 2: 'bajo', 3: 'bajo', 4: 'medio', 5: 'bajo',
              6: 'medio', 7: 'medio', 8: 'alto', 9: 'alto', 10: 'alto',
              11: 'medio', 12: 'alto', 13: 'alto'}

    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)
        self.naristas = 0

    def agregar_arista(self, u, v, peso):
        self.adj[u].append((v, peso))
        self.adj[v].append((u, peso))  # no dirigido: ambos sentidos
        self.naristas += 1

    def grado(self, u):
        return len(self.adj[u])

    def densidad(self):
        return 2 * self.naristas / (self.n * (self.n - 1))


# Red vial principal — distancias aproximadas en km (MTC, 2024)
RUTAS_PUNO = [
    (0, 1, 44), (0, 2, 55), (0, 5, 80), (1, 6, 37), (1, 7, 70), (1, 11, 90),
    (2, 3, 50), (2, 4, 45), (3, 4, 25), (5, 4, 60), (7, 8, 95), (7, 10, 110),
    (7, 11, 75), (8, 9, 40), (11, 12, 140), (11, 13, 180),
]


def construir_grafo_puno():
    g = GrafoPuno(14)
    for u, v, p in RUTAS_PUNO:
        g.agregar_arista(u, v, p)
    return g


# ── Actividad 3: Grafo DIRIGIDO — restricciones festividad ──────────────
class GrafoDirigidoPuno:
    """
    Representa las calles del centro de Puno con restricciones de
    sentido unico durante la Festividad de la Virgen de la Candelaria
    (febrero), declarada Patrimonio Cultural Inmaterial de la Humanidad
    por la UNESCO en 2014 -- la misma festividad de la que se origina
    la danza de la Diablada Punena.
    """

    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)

    def agregar_arista_dirigida(self, u, v, peso):
        self.adj[u].append((v, peso))  # SOLO un sentido: u -> v

    def es_alcanzable(self, origen, destino):
        """Verifica si destino es alcanzable desde origen (DFS simple)."""
        visitados = set()

        def dfs(u):
            if u == destino:
                return True
            visitados.add(u)
            return any(dfs(v) for v, _ in self.adj[u] if v not in visitados)

        return dfs(origen)


# Calles del centro historico -- 6 intersecciones (simplificado)
# 0=Plaza de Armas 1=Jr.Lima 2=Av.El Sol 3=Jr.Moquegua 4=Jr.Tacna 5=Malecon
RESTRICCIONES_CANDELARIA = [
    (0, 1, 'solo bajada hacia el malecon'),
    (1, 5, 'flujo unico hacia el lago durante el corso'),
    (2, 0, 'acceso unico a la plaza desde Av. El Sol'),
    (3, 2, 'desvio obligatorio'),
    (4, 3, 'sentido unico zona comercial'),
]


def construir_grafo_dirigido():
    gd = GrafoDirigidoPuno(6)
    for u, v, _ in RESTRICCIONES_CANDELARIA:
        gd.agregar_arista_dirigida(u, v, 1)
    return gd


# ── Actividad 4: Componentes conexas bajo bloqueo por lluvias ───────────
def componentes_conexas(g, vertices_excluidos=None):
    excluidos = vertices_excluidos or set()
    visitados = set(excluidos)
    componentes = []
    for inicio in range(g.n):
        if inicio in visitados:
            continue
        componente = []
        cola = deque([inicio])
        visitados.add(inicio)
        while cola:
            u = cola.popleft()
            componente.append(u)
            for v, _ in g.adj[u]:
                if v not in visitados and v not in excluidos:
                    visitados.add(v)
                    cola.append(v)
        componentes.append(componente)
    return componentes
