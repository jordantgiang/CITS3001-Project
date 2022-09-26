# CITS3001 Project - Information War Game
# Author: Carmen Leong (22789943), Jordan Thompson-Giang (22729642)

# Import libraries
# --------------------------------------------------- 
import random
import networkx as nx
import matplotlib.pyplot as plt


# Classes
# --------------------------------------------------- 
class Blue:
    def __init__(self, name, age):
        self.name = name
        self.age = age
class Red:
    def __init__(self, name, age):
        self.name = name
        self.age = age
class Green:
    def __init__(self, voteCertainty):
        self.voteCertainty = voteCertainty
class Grey:
    def __init__(self, spy):
        self.spy = spy

# Functions
# --------------------------------------------------- 
# def initGame(greenSettings, greySettings, uncertaintyInt, votePercentage)

def initGameDefault(idFile, edgeFile):
    # Read file
    nodes = [] # Example: [(4, {"color": "red"}),(5, {"color": "blue"}),(6, {"color": "green", "certainty":0.5})]
    edges = [] # Example: [(1, 2), (1, 3)]
    
    colourMap = []
    # Nodes file
    with open(idFile) as idF:
        lines = idF.readlines()
        for line in lines[1:]:
            line = line.strip("\n").split(",")
            if (line[1] == "green"):
                nodes.append( (line[0], {"colour": line[1], "certainty": round(random.uniform(-1, 1), 2)}))
            else:
                nodes.append( (line[0], {"colour": line[1]}) )
            colourMap.append(line[1].split("-")[0])
            
    # Edges file
    with open(edgeFile) as edgeF:
        lines = edgeF.readlines()
        for line in lines[1:]:
            line = line.strip("\n").split(",")
            edges.append( (line[0], line[1]) )

    print(nodes)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    # Draw graph
    nx.draw(G, with_labels=True, node_color=colourMap)
    plt.show() 

initGameDefault("node-attributes","network-2.csv")
    
