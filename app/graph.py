from py2neo import Graph

from app.config import GRAPH_PASSWORD, GRAPH_URL, GRAPH_USER

graph = Graph(GRAPH_URL, username=GRAPH_USER, password=GRAPH_PASSWORD)
