// ── analisis_red_vial.cpp — Componentes conexas + benchmark real ───────
//
// Nota de extension: el objetivo especifico de la guia pide "medir el
// tiempo de construccion del grafo y de computo de componentes contra la
// version Python", pero el codigo de la Actividad 6 tal como aparece en
// la guia no incluye ninguna instrumentacion de tiempo (ni <chrono> se
// usa realmente para medir, solo se incluye el header). Este archivo
// agrega el cronometraje real que el objetivo exige.

#include "grafo_puno.hpp"
#include <queue>
#include <unordered_set>
#include <chrono>
#include <random>

using Clock = std::chrono::high_resolution_clock;

std::vector<std::vector<int>> componentesConexas(
    const GrafoPuno& g, const std::unordered_set<int>& excluidos = {}) {
    std::vector<std::vector<int>> componentes;
    std::unordered_set<int> visitados = excluidos;
    for (int inicio = 0; inicio < g.numVertices(); inicio++) {
        if (visitados.count(inicio)) continue;
        std::vector<int> comp;
        std::queue<int> cola; cola.push(inicio); visitados.insert(inicio);
        while (!cola.empty()) {
            int u = cola.front(); cola.pop(); comp.push_back(u);
            for (auto& [v, _] : g.vecinos(u))
                if (!visitados.count(v) && !excluidos.count(v)) {
                    visitados.insert(v); cola.push(v);
                }
        }
        componentes.push_back(comp);
    }
    return componentes;
}

int main() {
    // ---------------------------------------------------------------
    // Parte 1: red vial real de Puno (14 ciudades), tal como pide la guia
    // ---------------------------------------------------------------
    auto t0 = Clock::now();
    GrafoPuno g(14);
    std::vector<std::tuple<int,int,int>> rutas = {
        {0,1,44},{0,2,55},{0,5,80},{1,6,37},{1,7,70},{1,11,90},
        {2,3,50},{2,4,45},{3,4,25},{5,4,60},{7,8,95},{7,10,110},
        {7,11,75},{8,9,40},{11,12,140},{11,13,180}
    };
    for (auto& [u,v,p] : rutas) g.agregarArista(u,v,p);
    double msConstruccion = std::chrono::duration<double, std::milli>(Clock::now() - t0).count();

    std::cout << "V=" << g.numVertices() << " E=" << g.numAristas()
              << " densidad=" << g.densidad() << '\n';
    std::cout << "Tiempo de construccion del grafo (14 ciudades): " << msConstruccion << " ms\n";

    t0 = Clock::now();
    auto comp = componentesConexas(g);
    double msComponentes = std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
    std::cout << "Componentes (sin bloqueos): " << comp.size()
              << " (calculado en " << msComponentes << " ms)\n";

    t0 = Clock::now();
    auto compLluvia = componentesConexas(g, {12, 13});
    double msComponentesLluvia = std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
    std::cout << "Componentes (Macusani/Sandia bloqueadas): " << compLluvia.size()
              << " (calculado en " << msComponentesLluvia << " ms)\n";

    // ---------------------------------------------------------------
    // Parte 2 (extension): benchmark a escala para comparar de forma
    // significativa contra Python, ya que con solo 14 nodos cualquier
    // medicion esta dominada por el ruido del sistema operativo
    // (microsegundos), tal como se discute en el informe.
    // ---------------------------------------------------------------
    std::cout << "\n=== Benchmark a escala (grafos dispersos aleatorios, grado promedio ~2.3) ===\n";
    std::mt19937 rng(42);
    for (int n : {1000, 10000, 100000, 1000000}) {
        t0 = Clock::now();
        GrafoPuno gGrande(n);
        std::uniform_int_distribution<int> distV(0, n - 1);
        std::uniform_int_distribution<int> distPeso(10, 200);
        int aristasObjetivo = (int)(n * 2.3 / 2);
        for (int i = 0; i < aristasObjetivo; i++) {
            int u = distV(rng), v = distV(rng);
            if (u != v) gGrande.agregarArista(u, v, distPeso(rng));
        }
        double msConst = std::chrono::duration<double, std::milli>(Clock::now() - t0).count();

        t0 = Clock::now();
        auto compGrande = componentesConexas(gGrande);
        double msComp = std::chrono::duration<double, std::milli>(Clock::now() - t0).count();

        std::cout << "n=" << n << " | construccion=" << msConst << "ms"
                  << " | componentes=" << compGrande.size()
                  << " en " << msComp << "ms\n";
    }

    return 0;
}
