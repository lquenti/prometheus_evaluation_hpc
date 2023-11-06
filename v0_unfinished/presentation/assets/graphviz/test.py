import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (20,20)

# Define the number of nodes
N = 974+448

# Create an empty graph
G = nx.DiGraph()

# Add nodes to the graph
G.add_node("Influx")
for i in range(1, N+1):
    G.add_node(str(i))

# Add edges to the graph
for i in range(1, N+1):
    G.add_edge("Influx", str(i))

# Draw the graph
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="lightblue")
nx.draw_networkx_edges(G, pos, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
plt.axis("off")
#plt.show()
plt.savefig("test.png")

