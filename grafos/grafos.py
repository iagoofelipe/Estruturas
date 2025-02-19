"""
###########################################################

Ativiade Ativa - Teoria dos Grafos e Análise de Algoritmos

###########################################################
"""

import matplotlib.pyplot as plt
import networkx as nx
import heapq
from typing import Iterable

LINE = '-' * 90

class CaminhoMinimo:
    def __init__(self, grafo:nx.Graph):
        self.grafo = grafo

    def gerarCaminho(self, origem:str) -> None:
        """ gera o caminho mínimo de um grafo utilizando o Algoritmo de Bellman-Ford """
        distancias = {}
        predecessores = {}
        caminhos = {}
        vertices = self.grafo.nodes

        if origem not in vertices:
            raise ValueError('esta origem não pertence aos vértices deste grafo')

        # armazenando distâncias com valores infinitos, exceto para a origem
        for vertice in vertices:
            distancias[vertice] = float('inf') if (vertice != origem) else 0
            predecessores[vertice] = None
            caminhos[vertice] = []

        # realizando relaxamento |V| - 1 vezes
        for _ in range(len(vertices) - 1):
            for vertice in vertices:
                for vizinho, prop in self.grafo[vertice].items():
                    peso = prop['weight']
                    distancia = distancias[vertice] + peso

                    if distancia < distancias[vizinho]:
                        distancias[vizinho] = distancia
                        predecessores[vizinho] = vertice
                
        # verificando se há ciclo negativo
        for vertice in self.grafo:
            for vizinho, prop in self.grafo[vertice].items():
                peso = prop['weight']
                if distancias[vertice] + peso < distancias[vizinho]:
                    raise ValueError("Ciclo negativo detectado")
                
        # gerando caminho completo a partir de cada predecessor
        caminhos_arestas = {}
        for atual, caminho in caminhos.items():
            aux1, aux2, proximo = atual, None, None
            caminhos_arestas[atual] = []

            while aux1 != origem:
                caminho.append(aux1)
                aux2 = aux1
                aux1 = predecessores[aux1]
                proximo = aux1
                caminhos_arestas[atual].append((aux2, proximo, self.grafo.get_edge_data(aux2, proximo)))

            caminho.append(origem)
            caminho.reverse()
            caminhos_arestas[atual].reverse()

        self.caminhos = caminhos
        self.distancias = distancias
        self.caminhos_arestas = caminhos_arestas

    def getDestino(self, destino:str) -> dict:
        """ retorna o caminho entre a última execução de gerarCaminho e o destino """

        return {
            'caminho': self.caminhos[destino],
            'distancia': self.distancias[destino],
            'grafo': nx.Graph(self.caminhos_arestas[destino]),
        }

class Grafo:
    def __init__(self, vertices):
        """ gera o grafo e prepara para a exibição visual """

        # gerando grafo e adicionando seus valores
        self.grafo = nx.Graph()
        self.grafo.add_weighted_edges_from(vertices)
        
        # obtendo dados para desenhar o grafo
        self.pos = nx.spring_layout(self.grafo, seed=7)
        self.labels = nx.get_edge_attributes(self.grafo, "weight")

    def caminhoEconomico(self, origem=None) -> nx.Graph:
        """ retorna a árvore geradora mínima do grafo, utilizando o algoritmo de Prim """
        vertices = set(self.grafo.nodes)
        visitados = set()
        agm = []

        # escolhe um vértice inicial, o qual pode ser escolhido arbitrariamente
        if origem is None:
            inicial = vertices.pop()
        else:
            vertices.remove(origem)
            inicial = origem

        visitados.add(inicial)

        # inicializa a fila de prioridade utilizando heapq, o qual mantém a ordem crescente de elementos
        fila = []
        for vizinho, prop in self.grafo[inicial].items():
            heapq.heappush(fila, (prop['weight'], inicial, vizinho))

        while fila:
            peso, u, v = heapq.heappop(fila)
            if v not in visitados:
                agm.append((u, v, {'weight': peso}))
                visitados.add(v)
                for vizinho, prop_v in self.grafo[v].items():
                    if vizinho not in visitados:
                        heapq.heappush(fila, (prop_v['weight'], v, vizinho))

        return nx.Graph(agm)

    def exibirGrafo(self, subgrafo:nx.Graph=None):
        """ cria uma janela para exibir o grafo e destaca o subgrafo informado, caso seja fornecido """

        # caso um subgrafo seja definido
        if subgrafo:
            ref = subgrafo.edges.data()
            edges_caminho = []
            edges_fora_caminho = []

            # separando arestas do caminho para destaque visual
            for u, v, d in self.grafo.edges.data():
                aresta = (u, v, d)

                if (u, v, d) in ref or (v, u, d) in ref:
                    edges_caminho.append(aresta)
                else:
                    edges_fora_caminho.append(aresta)

            nx.draw_networkx_edges(self.grafo, self.pos, edges_fora_caminho, edge_color="lightgray")
            nx.draw_networkx_edges(self.grafo, self.pos, edges_caminho, edge_color="blue", style="dashed")
        
        else:
            nx.draw_networkx_edges(self.grafo, self.pos, edge_color="lightgray")

        # desenhando grafo
        nx.draw_networkx_nodes(self.grafo, self.pos, node_color="lightgray", node_size=1500)
        nx.draw_networkx_labels(self.grafo, self.pos, font_family="sans-serif")
        nx.draw_networkx_edge_labels(self.grafo, self.pos, self.labels)
        

        # configurando e exibindo com matplotlib
        plt.title("Atividade Ativa - Teoria dos Grafos e Análise de Algoritmos")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

def getOpcao(opcoes:Iterable, texto:str='Opção desejada') -> str:
    """ coleta a resposta do usuário, retorna apenas quando a opção fornecida estiver entre o conjunto de opções """
    opcao = input(texto+': ')

    while opcao not in opcoes:
        opcao = input(f'Opção inválida!\n{texto}: ')
    
    return opcao

def menu(grafo:Grafo):
    """ exibindo opções para o usuário utilizar o grafo """

    caminho_minimo = CaminhoMinimo(grafo.grafo)
    vertices = grafo.grafo.nodes

    while True:
        print(
            LINE,
            'Opções disponíveis',
            '',
            '\t1. Caminho mínimo entre dois vértices',
            '\t2. Caminho mais econômico',
            '\t3. Exibir vértices',
            '\t4. Exibir grafo',
            '\t0. Sair',
            '',
            sep='\n'
        )

        opcao = getOpcao(map(lambda x: str(x), range(5)))

        print(LINE)
        if opcao == '0':
            break
        elif opcao in ('1', '2', '3'):
            print('Vértices disponíveis', vertices)

        match opcao:
            case '1':
                origem = getOpcao(vertices, 'Origem')
                destino = getOpcao(vertices, 'Destino')

                # calculando caminho
                caminho_minimo.gerarCaminho(origem)
                resultado = caminho_minimo.getDestino(destino)

                print(
                    f'\nCaminho mínimo entre {origem} e {destino}:',
                    f'\tDistância: {resultado["distancia"]}',
                    f'\tTrajeto: {" > ".join(resultado["caminho"])}',
                    sep='\n'
                )
                grafo.exibirGrafo(resultado['grafo'])
            
            case '2':
                origem = getOpcao(list(vertices)+[''], 'Origem (em branco para origem aleatória)')
                caminho_economico = grafo.caminhoEconomico(origem if origem else None)
                distancia_total = 0

                print('\nArestas percoridas:')
                for u, v, d in caminho_economico.edges.data():
                    peso = d['weight']
                    distancia_total += peso
                    print(f'\tDistância {peso}, {u} > {v}')

                print('\tDistância total:', distancia_total)
                
                grafo.exibirGrafo(caminho_economico)

            case '4':
                grafo.exibirGrafo()


if __name__ == '__main__':

    # Preparando valores de vértices e arestas
    vertices = [
        ("Esplanada", "Asa Sul", 5),
        ("Esplanada", "Lago Sul", 11),
        ("Esplanada", "Vila Planalto", 10),
        ("Esplanada", "Lago Norte", 8),
        ("Esplanada", "Asa Norte", 6),
        ("Asa Sul", "Lago Sul", 5),
        ("Lago Sul", "Vila Planalto", 14),
        ("Vila Planalto", "Lago Norte", 7),
        ("Lago Norte", "Asa Norte", 12),
        ("Asa Norte", "Asa Sul", 12),
    ]
    grafo = Grafo(vertices)
    menu(grafo)