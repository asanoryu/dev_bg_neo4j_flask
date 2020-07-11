from envparse import env


GRAPH_URL = env.str("GRAPH_URL", default="http://localhost:7474")
GRAPH_USER = env.str("GRAPH_USER", default="neo4j")
GRAPH_PASSWORD = env.str("GRAPH_PASSWORD", default="123456")
