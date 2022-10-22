# CITS3001 Project - Information War Game
# Author: Carmen Leong (22789943), Jordan Thompson-Giang (22729642)

# Import libraries
# --------------------------------------------------- 
import matplotlib.pyplot as plt
import math
import networkx as nx
import random
import time
import tkinter as tk
from tkinter import ttk

# Global Constants
# --------------------------------------------------- 
# Inputs
GREY_NUM = 8 # Number of grey agent
GREEN_NUM = 90 # Number of green agent
CON_PROB = 0.03 # Probability of initial connection between any 2 green nodes
SPY_PROP = 0.2 # Proportion of agents who are spies from the red team
UNC_RANGE = (-0.5, 0.3) # Initial uncertainty range for green nodes
INIT_VOTE = 0.7 # Percentage of green nodes with voting opinion

# Game settings
WIN_THRESHOLD = 0.6 # Proportion of population required with agreeing certain (uncertainty < 0) opinions for red/blue to win.
INFLUENCE_FACTOR = 1.2 # Uncertainty value's influence of the change of uncertainty in an interaction uncertainty calculation.
INTERACTION_COEFF = 0.1 # Scaling coefficient of an interaction uncertainty calculation.

# Classes for nodes
# --------------------------------------------------- 
class Blue:
    # Constructor
    def __init__(self):
        self.energy = 100
        self.messages = {
            "M1": {"cost": 1, "strength": 1, "message": None}, 
            "M2": {"cost": 2, "strength": 2, "message": None},
            "M3": {"cost": 3, "strength": 3, "message": None},
            "M4": {"cost": 4, "strength": 4, "message": None},
            "M5": {"cost": 5, "strength": 5, "message": None}
        }
    
    # Introduce a Grey node
    def introduceGrey(self):
        # Grey agent turn
        return

    # Decision making method for choosing a Blue agent action
    def chooseAction(self):
        return

class Red:
    # Constructor
    def __init__(self, followers):
        self.followers = followers
        self.messages = {
            "M1": {"cost": 1, "strength": 1, "message": None}, 
            "M2": {"cost": 2, "strength": 2, "message": None},
            "M3": {"cost": 3, "strength": 3, "message": None},
            "M4": {"cost": 4, "strength": 4, "message": None},
            "M5": {"cost": 5, "strength": 5, "message": None}
        }

    def chooseAction(self):
        return

class Green:
    # Constructor
    def __init__(self, vote, uncertainty):
        self.vote = vote
        self.uncertainty = uncertainty

    
class Grey:
    # Constructor
    def __init__(self, spy):
        self.spy = spy
    
    def influence(self):
        return


# Classes for game
# --------------------------------------------------- 
class Game:
    # Constructor
    def __init__(self, greyNum, greenNum, connectProb, spyProp, uncRange, initVote):
        # Game parameter attributes
        self.greyNum = greyNum
        self.greenNum = greenNum
        self.connectProb = connectProb
        self.spyProp = spyProp
        self.uncRange = uncRange
        self.initVote = initVote
        
        self.graph = nx.Graph()
        # List of
        self.nodes = []
        self.greenAdj = []
        self.redAdj = []
        self.blueAdj = []

    # Visualisation of the current game state graph
    def showGraph(self, adj, clr):
        plt.clf()
        self.graph.clear()
        colourMap = []
        voteList = {}
        
        self.graph.add_nodes_from(self.nodes)
        
        fixPos = {}
        nrows = math.ceil(math.sqrt(self.greenNum))
        
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            # If blue node
            if node.__class__.__name__ == "Blue":
                colourMap.append("blue")
                voteList[node] = "Blue"
                fixPos[node] = (-nrows//3, (nrows // 2) - 1)
            # If red node
            elif node.__class__.__name__ == "Red":
                colourMap.append("red")
                voteList[node] = "Red"
                fixPos[node] = (nrows//3 + nrows, (nrows // 2) - 1)
            else:
                fixPos[node] = ((i-2) % nrows, (i-2) // nrows)
                if node.vote:
                    colourMap.append( (0, 0.5, 1) )
                    voteList[node] = f"V, {round(node.uncertainty, 1)}"
                else:
                    colourMap.append( (1, 0.5, 0) )
                    voteList[node] = f"NV, {round(node.uncertainty, 1)}"
                
        self.graph.add_edges_from(adj)
        
        pos = nx.spring_layout(self.graph, pos=fixPos, fixed=self.nodes)
        # nx.draw_networkx_nodes(self.graph, pos=pos, node_color=colourMap, node_size=[30]*len(self.nodes))
        # nx.draw_networkx_edges(self.graph, pos=pos, edge_color=[clr]*len(self.graph.edges()))
        nx.draw(self.graph, pos = pos, with_labels=False, node_color=colourMap, edge_color=[clr]*len(self.graph.edges()), node_size=[30]*len(self.nodes))
        
        labelPos = {}
        for p in pos.keys():
            labelPos[p] = (pos[p][0] - nrows/50, pos[p][1] + nrows/45)
        
        nx.draw_networkx_labels(self.graph, pos=labelPos, labels=voteList, font_size=8)
        # plt.show()
        plt.pause(1)

    # Creates an initial game state graph 
    def createPop(self):
        
        self.nodes = [Blue(), Red(range(2, 2+self.greenNum))]
        
        for i in range(self.greenNum):
            
            # Node's uncertainty and opinion
            vote = False
            if (i < self.greenNum * self.initVote):
                vote = True
            
            uncertainty = round(random.uniform(self.uncRange[0], self.uncRange[1]), 1)
            
            self.nodes.append(Green(vote, uncertainty))
            
            self.blueAdj.append( (self.nodes[0], self.nodes[i+2]) )
            self.redAdj.append( (self.nodes[1], self.nodes[i+2]) )
        
        # Generate initial random edges
        for i in range(2, 2+self.greenNum):
            for j in range(i+1, 2+self.greenNum):
                if (random.random() < self.connectProb):
                    self.greenAdj.append( (self.nodes[i], self.nodes[j]) )

    def checkWin(self):
        # Voting Proportion
        # Vote Majority - BLUE WIN
        # No Voting Majority - RED WIN
        
        certainVoters = 0
        certainNonVoters = 0
        for k in range(self.greenNum):
            node = self.nodes[k+2]
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
    
    def calcUncertainty(self, agent, diff, increase):
        if increase:
            agent.uncertainty += (agent.uncertainty+INFLUENCE_FACTOR)*diff*INTERACTION_COEFF
        else:
            agent.uncertainty -= (agent.uncertainty+INFLUENCE_FACTOR)*diff*INTERACTION_COEFF

        if (agent.uncertainty > 1):
            overflow = agent.uncertainty - 1
            agent.vote = not agent.vote
            agent.uncertainty = 1 - overflow
        
        if (agent.uncertainty < -1):
            agent.uncertainty = -1

    # In the case of a red/blue to green interaction, @param agent1 is passed as red/blue
    def interact(self, agent1, agent2):
        # Interaction between 2 green nodes
        if (type(agent1) == Green and type(agent2) == Green):
            # print(f"Old:\n\t1. Vote = {agent1.vote}, Unc = {agent1.uncertainty}\n\t2. Vote = {agent2.vote}, Unc = {agent2.uncertainty}")
            # Agreeing opinions
            if (agent1.vote == agent2.vote):
                uncDiff = (agent1.uncertainty - agent2.uncertainty)
                if abs(agent1.uncertainty) < abs(agent2.uncertainty):
                    self.calcUncertainty(agent1, uncDiff, True)
                    self.calcUncertainty(agent2, uncDiff, False)
                else:
                    self.calcUncertainty(agent1, uncDiff, False)
                    self.calcUncertainty(agent2, uncDiff, True)
            # Differing opinions
            else:
                uncDiff = (1 - agent1.uncertainty) + (1 - agent2.uncertainty)
                self.calcUncertainty(agent2, uncDiff, True)
                
            # print(f"New:\n\t1. Vote = {agent1.vote}, Unc = {agent1.uncertainty}\n\t2. Vote = {agent2.vote}, Unc = {agent2.uncertainty}")
        else:
            # change green uncertainty/opinion only
            # if (blue):
            # else:
            pass
    
    def socialise(self):
        for edge in self.greenAdj:
                self.interact(edge[0], edge[1])
        return
    
    # Broadcasting message to all Green nodes
    def broadcast(self, message, receivers):
        return
    
    def endGame(self):
        return
    
    def runGame(self, greyAgents):
        win = self.checkWin()
        while (win == 0):
            # Red
            self.nodes[1].chooseAction()
            
            self.showGraph(self.redAdj, (1,0,0,0.4))
            # Blue
            self.nodes[0].chooseAction()
            self.showGraph(self.blueAdj, (0,0,1,0.4))
            
            # Grey
            
            # Green
            self.socialise()
            self.showGraph(self.greenAdj, (0,1,0,0.4))
                
            
            # Check win
            win = self.checkWin()
            
        if win==1:
            print("BLUE WINS")
        elif win==2:
            print("RED WINS")
        self.endGame()

    def initGame(self):
        self.createPop()
        greys = []
        for i in range(self.greyNum):
            spy = False
            if (i < self.greyNum * self.spyProp):
                spy = True
            greys.append(Grey(spy))
        self.runGame(greys)

# GUI
# -------------------------------------------------------------


    def showWindow(self):

        def button_clicked(option):
            print('Button clicked:',option)
        
        root = tk.Tk()
        root.title('Information War Game')
        root.geometry('600x400+50+50')
        root.iconbitmap('./logo.ico')

        # place a label on the root window
        message = ttk.Label(root, text="Information War Game", font=("Rockwell", 14))
        message.pack()

        # place a button on the root window
        ttk.Button(root, text='Click Me', command=button_clicked('Hello')).pack()

        # keep the window displaying
        root.mainloop()

    

# Functions
# --------------------------------------------------- 
# def initGame(greenSettings, greySettings, uncertaintyInt, votePercentage)

# def initGameDefault(idFile, edgeFile):
#     # Read file
#     nodes = [] # Example: [(4, {"color": "red"}),(5, {"color": "blue"}),(6, {"color": "green", "certainty":0.5})]
#     edges = [] # Example: [(1, 2), (1, 3)]
    
#     colourMap = []
#     # Nodes file
#     with open(idFile) as idF:
#         lines = idF.readlines()
#         for line in lines[1:]:
#             line = line.strip("\n").split(",")
#             if (line[1] == "green"):
#                 nodes.append( (line[0], {"colour": line[1], "certainty": round(random.uniform(-1, 1), 2)}))
#             else:
#                 nodes.append( (line[0], {"colour": line[1]}) )
#             colourMap.append(line[1].split("-")[0])
            
#     # Edges file
#     with open(edgeFile) as edgeF:
#         lines = edgeF.readlines()
#         for line in lines[1:]:
#             line = line.strip("\n").split(",")
#             edges.append( (line[0], line[1]) )
    
#     G = nx.Graph()
#     G.add_nodes_from(nodes)
#     G.add_edges_from(edges)
    
    # Draw graph
    # nx.draw(G, with_labels=True, node_color=colourMap)
    # plt.show() 

# initGameDefault("node-attributes","network-2.csv")
    
def main():
    G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,UNC_RANGE,INIT_VOTE)
    # G1.initGame()
    G1.showWindow()
    # a1 = Green(True, -0.7)
    # a2 = Green(True, 0.2)
    # G1.interact(a1, a2)


if __name__=="__main__":
    main()
