# CITS3001 Project - Information War Game
# Author: Carmen Leong (22789943), Jordan Thompson-Giang (22729642)

# Import libraries
# --------------------------------------------------- 
import random
import networkx as nx
import matplotlib.pyplot as plt


# Global Constants
# --------------------------------------------------- 
GREY_NUM = 8 # Number of grey agent
GREEN_NUM = 90 # Number of green agent
CON_PROB = 0.2 # Probability of initial connection between any 2 green nodes
SPY_PROP = 0.2 # Proportion of agents who are spies from the red team
UNCERTAINTY_RANGE = (-0.5,0.5) # Initial uncertainty range for green nodes
VOTER_PERC = 0.7 # Percentage of green nodes with voting opinion 


# Classes for nodes
# --------------------------------------------------- 
class Blue:
    def __init__(self):
        self.energy = 100
        self.messages = {
            "M1": {"cost": 1, "strength": 1, "message": None}, 
            "M2": {"cost": 2, "strength": 2, "message": None},
            "M3": {"cost": 3, "strength": 3, "message": None},
            "M4": {"cost": 4, "strength": 4, "message": None},
            "M5": {"cost": 5, "strength": 5, "message": None}
        }
    
    def broadcast(self):
        return
    
    def introduceGrey(self):
        return

    def takeTurn(self):
        return

class Red:
    def __init__(self, followers):
        self.followers = followers
        self.messages = {
            "M1": {"cost": 1, "strength": 1, "message": None}, 
            "M2": {"cost": 2, "strength": 2, "message": None},
            "M3": {"cost": 3, "strength": 3, "message": None},
            "M4": {"cost": 4, "strength": 4, "message": None},
            "M5": {"cost": 5, "strength": 5, "message": None}
        }
    
    def broadcast(self):
        return

    def takeTurn(self):
        return

class Green:
    def __init__(self, voteCertainty):
        self.voteCertainty = voteCertainty
    
    def socialise(self):
        return
    
    def takeTurn(self):
        return

    
class Grey:
    def __init__(self, spy):
        self.spy = spy
    
    def influence(self):
        return

    def takeTurn(self):
        return


# Classes for game
# --------------------------------------------------- 
class Game:
    def __init__(self, grey_num, green_num, con_prob, spy_prob, uncertainity_range, voter_perc):
        self.grey_num = grey_num
        self.green_num = green_num
        self.con_prob = con_prob
        self.spy_prob = spy_prob
        self.uncertainity_range = uncertainity_range
        self.voter_perc = voter_perc
        self.green_adj_list = []

    def createGraph(self):
        for i in range(self.green_num):
            

        self.green_adj_list = 
        return

    def checkWin(self):
        return
    
    def runGame(self):
        return

    def initGame(self):
        self.createGraph()
        self.runGame()
    
    

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
    
def main():
    G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,UNCERTAINTY_RANGE,VOTER_PERC)
    G1.initGame()


if __name__=="__main__":
    main()
