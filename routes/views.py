from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import pandas as pd
from collections import deque
from haversine import haversine, haversine_vector, Unit

# ===========================================
# functions routes
# ===========================================
def encontrar_melhor_rota(grafo, inicio, destino):
    fila = deque([(inicio, [inicio], 0)])
    melhor_rota = None
    menor_custo = float('inf')
    while fila:
        vertice, rota_atual, custo_atual = fila.popleft()
        if vertice == destino:
            if custo_atual < menor_custo:
                melhor_rota = rota_atual
                menor_custo = custo_atual
        if vertice in grafo:
            for proximo, peso in grafo[vertice].items():
                if proximo not in rota_atual:
                    fila.append((proximo, rota_atual + [proximo], custo_atual + peso))
    return melhor_rota, menor_custo

def get_inicial_point(user_location, df_routes):
    points = {
        key: tuple(map(float, value.split(", "))) 
        for key, value in df_routes[["Cordenadas", "Nome"]].set_index("Nome").to_dict()["Cordenadas"].items()
    }
    for key, value in points.items():
        points[key] = haversine(user_location, value, unit=Unit.METERS)
    return min(points, key=points.get)

def get_possibilidades(df_routes):
    routes_temp = df_routes[["Cordenadas", "Nome", "Acesso"]].set_index("Nome").to_dict()
    routes_possibilidades = {}
    config_cord = lambda cord: tuple(map(float, cord.split(", ")))
    for acesso_cordenada, cordenadas in routes_temp["Cordenadas"].items():
        routes_possibilidades[acesso_cordenada] = {}
        for acesso_caminho in routes_temp["Acesso"][acesso_cordenada].split(", "):
            routes_possibilidades[acesso_cordenada][acesso_caminho] = haversine(
                config_cord(cordenadas), 
                config_cord(routes_temp["Cordenadas"][acesso_caminho]
            ), unit=Unit.METERS)
    return routes_possibilidades

# ===========================================
# views
# ===========================================
def map_creation(request):
    return render(request, "map/map_template.html")

def map_view(request):
    df_routes = pd.read_excel('./routes_file/teste.xlsx')
    routes = {"routes": list(df_routes.T.to_dict().values())}
    select_filter = list(df_routes[df_routes['Visivel'] == True]["Nome"].values)
    context = {
        "routes": routes,
        "select_filter": select_filter
    }
    return render(request, "map/map_view.html", context=context)

def get_route(request, latitude_user, longitude_user, destino):
    if latitude_user == '-1' and longitude_user == '-1':
        result = {"status": 400}
        
    else:
        try:
            df_routes = pd.read_excel('./routes_file/teste.xlsx')
            ponto_inicial = get_inicial_point((float(latitude_user), float(longitude_user)), df_routes)
            possibilidades = get_possibilidades(df_routes)
            melhor_caminho, distancia = encontrar_melhor_rota(possibilidades, ponto_inicial, destino)
            caminho_final = df_routes[df_routes["Nome"].isin(melhor_caminho)][["Nome", "Cordenadas"]].set_index("Nome").to_dict()["Cordenadas"]
            result = {"status": 200, "melhor_caminho":melhor_caminho, "routes": caminho_final, "distancia": distancia}
            
        except Exception as e:
            result = {"status": 400, "message": e}

    return JsonResponse(result)