import networkx as nx
import matplotlib.pyplot as plt


def generate_random_graph(n, m):
    G = nx.dense_gnm_random_graph(n, m)

    val_map = {0: 1.0}
    values = [val_map.get(node, 1) for node in G.nodes()]

    black_edges = [edge for edge in G.edges()]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)

    katz = katz_centrality(G, 0.1, 1.0)

    plt.show()

    return katz

def get_list_of_edges(edges):
    list_of_edges = []
    print("Type pairs of nodes in uppercase between the edges and separating the nodes with a comma")
    full_connections = 0
    while full_connections < edges:
        new_connection = input()
        try:
            new_connection = new_connection.replace(" ", "")
            if new_connection[0].isalpha() and new_connection[0].isupper():
                if new_connection[2].isalpha() and new_connection[2].isupper():
                    list_of_edges.append(tuple(new_connection.split(",")))
                    full_connections += 1
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("Incorrect names of nodes")
    return list_of_edges


def generate_graph(n, m):
    G = nx.DiGraph()

    list_of_edges = get_list_of_edges(m)

    try:
        G.add_edges_from(list_of_edges)
    except ValueError:
        print("Incorrect names for nodes")

    while len(G.nodes()) != n:
        print(G.nodes())

        if len(G.nodes()) < n:
            l = sorted(nx.nodes(G))
            num_char = ord(l[-1])
            node_to_add = chr(num_char+1)
            G.add_node(node_to_add)
        else:
            print("Too much nodes, please back to form")
            list_of_edges = get_list_of_edges(m)
            try:
                G.add_edges_from(list_of_edges)
            except ValueError:
                print("Incorrect names for nodes")

    val_map = {list_of_edges[0][0]: 1.0}

    values = [val_map.get(node, 1) for node in G.nodes()]

    black_edges = [edge for edge in G.edges()]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)

    katz = katz_centrality(G, 0.1, 1.0)

    plt.show()
    return katz


def katz_centrality(G, alpha, beta=1.0, max_iter=1000, tol=1.0e-6, weight=None, normalized=True ):
    if len(G) == 0:
        return {}

    nodes = G.number_of_nodes()
    dict_of_nodes = dict([(n, 0) for n in G])

    try:
        beta_dictionary = dict.fromkeys(G, float(beta))
    except (TypeError, ValueError, AttributeError):
        beta_dictionary = beta
        if set(beta) != set(G):
            raise nx.NetworkXError('beta dictionary must have a value for every node')

    for i in range(max_iter):
        dict_of_nodes_helper = dict_of_nodes
        dict_of_nodes = dict.fromkeys(dict_of_nodes_helper, 0)
        for n in dict_of_nodes:
            for nbr in G[n]:
                dict_of_nodes[nbr] += dict_of_nodes_helper[n] * G[n][nbr].get(weight, 1)
        for n in dict_of_nodes:
            dict_of_nodes[n] = alpha * dict_of_nodes[n] + beta_dictionary[n]
        err = sum([abs(dict_of_nodes[n] - dict_of_nodes_helper[n]) for n in dict_of_nodes])
        if err < nodes * tol:
            if normalized:
                min_item = min(dict_of_nodes.values())

                max_item = max(dict_of_nodes.values())
                for k, v in dict_of_nodes.items():
                    if dict_of_nodes[k] == min_item:
                        dict_of_nodes[k] = 0.0
                        continue
                    dict_of_nodes[k] = v / max_item

            return dict_of_nodes
    raise nx.PowerIterationFailedConvergence(max_iter)

if __name__ == "__main__":

    print("Hello!\nHow graph you want to have:")
    print("1) Random")
    print("2) Your graph")
    choice = int(input("Answer: "))
    n = int(input("How much nodes you want to have in your graph?"))
    m = int(input("How much edges you want to have in your graph?"))
    katz = 0

    if choice == 1:
        katz = generate_random_graph(n, m)
    if choice == 2:
        katz = generate_graph(n, m)

    print(katz)
