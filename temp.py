import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
G.add_edge(2, 1)
G.add_edge(2, 1)
G.add_edge(2, 13)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=True)
# plt.savefig('picture.png')
plt.show()
