# CITS3001 Project - Information War Game
# Author: Carmen Leong (22789943), Jordan Thompson-Giang (22729642)

# Import libraries
# --------------------------------------------------- 
import random
from types import NoneType
import networkx as nx
import matplotlib.pyplot as plt


# Global Constants
# --------------------------------------------------- 
# Inputs
GREY_NUM = 8 # Number of grey agent
GREEN_NUM = 90 # Number of green agent
CON_PROB = 0.03 # Probability of initial connection between any 2 green nodes
SPY_PROP = 0.2 # Proportion of agents who are spies from the red team
UNC_RANGE = (-0.5,0.5) # Initial uncertainty range for green nodes
INIT_VOTE = 0.7 # Percentage of green nodes with voting opinion

# Game settings
WIN_THRESHOLD = 0.6

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
        # Grey agent turn
        return

    def chooseAction(self):
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

    def chooseAction(self):
        return

class Green:
    def __init__(self, vote, uncertainty):
        self.vote = vote
        self.uncertainty = uncertainty
    
    def socialise(self):
        return

    
class Grey:
    def __init__(self, spy):
        self.spy = spy
    
    def influence(self):
        return


# Classes for game
# --------------------------------------------------- 
class Game:
    def __init__(self, greyNum, greenNum, connectProb, spyProp, uncRange, initVote):
        self.greyNum = greyNum
        self.greenNum = greenNum
        self.connectProb = connectProb
        self.spyProp = spyProp
        self.uncRange = uncRange
        self.initVote = initVote
        self.graph = None
        self.green_adj_list = []

    def createGraph(self):
        
        G = nx.Graph()
        colourMap = []
        voteList = {}
        
        # Create Green nodes/edges
        for i in range(self.greenNum):
            # Node's uncertainty and opinion
            vote = False
            if (i < self.greenNum * self.initVote):
                vote = True
                
            if (vote):
                voteList[i] = "T"
            else:
                voteList[i] = "F"
            
            unc = round(random.uniform(self.uncRange[0], self.uncRange[1]), 1)
            
            # Adding node by name and decision value
            G.add_node(i, obj = Green(vote, unc))
            colourMap.append("green")
        
        # Create Green connection list
        for i in list(G.nodes):
            for j in list(G.nodes):
                if (i < j):
                    if (random.random() <= self.connectProb):
                        G.add_edge(i, j)
            
        # Print graph
        pos = nx.circular_layout(G)
        nx.draw(G, pos=pos, with_labels=False, node_color=colourMap)
        nx.draw_networkx_labels(G, pos, labels=voteList)
        plt.show() 
        
        # Update Game attribute
        self.graph = G

    def checkWin(self):
        # Voting Proportion
        # Vote Majority - BLUE WIN
        # No Voting Majority - RED WIN
        
        certainVoters = 0
        certainNonVoters = 0
        for k in range(self.greenNum):
            node = self.graph.nodes[k]["obj"]
            if (node.uncertainty < 0):
                if (node.vote):
                    certainVoters += 1
                else:
                    certainNonVoters += 1
        
        if (certainVoters / self.greenNum > WIN_THRESHOLD):
            return 1
        elif (certainNonVoters / self.greenNum > WIN_THRESHOLD):
            return 2
        return 0
        
    def endGame(self):
        return
    
    def runGame(self, redAgent, blueAgent, greyAgents):
        win = self.checkWin()
        while (win == 0):
            # Red
            redAgent.chooseAction()
            
            # Blue
            blueAgent.chooseAction()
            
            # Grey
            
            # Green
            for edge in list(self.graph.edges):
                print(edge)
                node1 = self.graph.nodes[edge[0]]["obj"]
                node2 = self.graph.nodes[edge[1]]["obj"]
                
                
                
            break
                        
                        
                
            
            # Check win
            win = self.checkWin()
        self.endGame()

    def initGame(self):
        self.createGraph()
        red = Red(list(range(self.greenNum)))
        blue = Blue()
        greys = []
        for i in range(self.greyNum):
            spy = False
            if (i < self.greyNum * self.spyProp):
                spy = True
            greys.append(Grey(spy))
        self.runGame(red, blue, greys)
    
    

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

# initGameDefault("node-attributes","network-2.csv")
    
def main():
    G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,UNC_RANGE,INIT_VOTE)
    G1.initGame()


if __name__=="__main__":
    main()
