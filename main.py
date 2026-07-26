from loaders.loader_factory import LoaderFactory
from core.statistics import Statistics

# برای دیتاست edge-list (مثل همونی که فرستادی):
graph = LoaderFactory.load("data/edges.txt")

# برای دیتاست JSON (دو فایل جدا users/relationships):
graph = LoaderFactory.load("data/users.json", "data/relationships.json")

stats = Statistics(graph)
print(stats.summary())
