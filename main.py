from loaders.edge_list_loader import EdgeListLoader
from core.statistics import Statistics
from core.BFS import BFS
from core.DFS import DFS

loader = EdgeListLoader()
graph = loader.load("data/edges.txt")

stats = Statistics(graph)
bfs = BFS(graph)
dfs = DFS(graph)

print(stats.summary())

most_connected = stats.most_connected_user()
print("Most connected:", most_connected.id)

distances = bfs.distance_to_all(most_connected.id)
print(bfs.format_distances(distances))

components = dfs.connected_components()
print("Components:", [len(c) for c in components])