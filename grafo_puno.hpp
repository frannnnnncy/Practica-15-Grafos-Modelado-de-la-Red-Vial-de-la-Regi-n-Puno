// ── grafo_puno.hpp — Grafo en C++17 ──────────────────────────────────────
#pragma once
#include <vector>
#include <string>
#include <unordered_map>
#include <iostream>

using Arista = std::pair<int, int>; // (destino, peso)

class GrafoPuno {
    int n;
    std::vector<std::vector<Arista>> adj;
    int naristas = 0;
    const std::vector<std::string> ciudades = {
        "Puno", "Juliaca", "Ilave", "Desaguadero", "Yunguyo", "Juli",
        "Lampa", "Azangaro", "Huancane", "Moho", "Putina", "Ayaviri",
        "Macusani", "Sandia"};

public:
    explicit GrafoPuno(int n) : n(n), adj(n) {}

    void agregarArista(int u, int v, int peso) {
        adj[u].push_back({v, peso});
        adj[v].push_back({u, peso});
        naristas++;
    }

    const std::vector<Arista>& vecinos(int u) const { return adj[u]; }
    int grado(int u) const { return (int)adj[u].size(); }
    double densidad() const { return 2.0 * naristas / (n * (n - 1)); }
    std::string nombreCiudad(int u) const { return ciudades[u]; }
    int numVertices() const { return n; }
    int numAristas() const { return naristas; }

    bool existeArista(int u, int v) const {
        for (auto& [dest, _] : adj[u]) if (dest == v) return true;
        return false;
    }
};
