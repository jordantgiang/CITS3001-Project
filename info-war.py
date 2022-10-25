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
import sv_ttk
from PIL import Image, ImageTk


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
            "M1": {"cost": 1, "strength": 0.1, "message": "BLUE loves you"}, 
            "M2": {"cost": 2, "strength": 0.2, "message": "Trust in BLUE"},
            "M3": {"cost": 3, "strength": 0.3, "message": "BLUE is true"},
            "M4": {"cost": 4, "strength": 0.4, "message": "BLUE is better"},
            "M5": {"cost": 5, "strength": 0.5, "message": "Your future depends on your vote"}
        }
    
    # Decision making method for choosing a Blue agent action
    def chooseAction(self, greyAgents):
        # Randomly chooses between grey node and broadcast
        if (len(greyAgents) != 0 and random.random() < 0.1):
            return 1
        # Choosing random message
        print(f"Energy: {self.energy}")
        if (self.energy == 0):
            return -1
        while (True):
            msg = random.choice(list(self.messages.values()))
            if (msg["cost"] <= self.energy):
                return msg

class Red:
    # Constructor
    def __init__(self, followers):
        self.followers = followers
        self.messages = {
            "M1": {"loss": 0.005, "strength": 0.4, "message": "Blue is racist"}, 
            "M2": {"loss": 0.01, "strength": 0.5, "message": "Blue support child labour"},
            "M3": {"loss": 0.015, "strength": 0.6, "message": "Blue corrupts"},
            "M4": {"loss": 0.02, "strength": 0.7, "message": "Blue support human experiments"},
            "M5": {"loss": 0.025, "strength": 0.8, "message": "Blue uses birds to stalk people"}
        }

    def chooseAction(self):
        # Choosing random message
        return random.choice(list(self.messages.values()))

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
        if (self.spy):
            print("sneakily INFLUENCING")
        else:
            print("INFLUENCING")
        return


# Classes for game
# --------------------------------------------------- 
class Game:
    # Constructor
    def __init__(self, greyNum, greenNum, connectProb, spyProp, uncRange, initVote, redIsAi, blueIsAi):
        # Game parameter attributes
        self.greyNum = greyNum
        self.greenNum = greenNum
        self.connectProb = connectProb
        self.spyProp = spyProp
        self.uncRange = uncRange
        self.initVote = initVote
        self.redIsAi = redIsAi
        self.blueIsAi = blueIsAi
        self.turn = "RED"

        self.graph = nx.Graph()
        # List of
        self.nodes = [] # first node is Blue, second node is Red, the rest is green 
        self.greenAdj = []
        self.redAdj = []
        self.blueAdj = []

    # Get user input
    def startGame(self):
        print("------ Welcome to Information War Game ------")
        print("------ Game Settings ------")

        while True:
            redPlayer = input("AI/Human for Red Team (Enter AI/Human): ").lower()
            if redPlayer == "ai" or redPlayer =="human":
                self.redIsAi = False if redPlayer == "human" else True
                break
        while True:
            bluePlayer = input("AI/Human for Blue Team (Enter AI/Human): ").lower()
            if bluePlayer == "ai" or bluePlayer == "human":
                self.blueIsAi = False if bluePlayer == "human" else True
                break
        while True:
            default = input("Would you like to use the default game settings?: (Enter y/n) ").lower()
            if default == "y":
                return
            else:
                break
        while True:
            try:
                greenNum = int(input("Number of green agents (Enter an integer): "))
                self.greenNum = greenNum
                break
            except:
                continue
        while True:
            try:
                greyNum = int(input("Number of grey agents (Enter an integer): "))
                self.greyNum = greyNum
                break
            except:
                continue
        while True:
            try:
                connProb = float(input("Probability of connection between green agents (Enter a decimal value between 0 to 1): "))
                if connProb <= 1 and connProb >= 0:
                    self.connProb = connProb
                    break
                else:
                    continue
            except:
                continue
        while True:
            try:
                spyProp = float(input("Proportion of red spy among grey agents (Enter a decimal value between 0 to 1): "))
                if spyProp <= 1 and spyProp >= 0:
                    self.spyProp = spyProp
                    break
                else:
                    continue
            except:
                continue
        while True:
            try:
                uncRange = input("Initial uncertainty range for green nodes (Enter two decimal values between -1 to 1 separated by space): ").split()
                uncRange[0],uncRange[1] = float(uncRange[0]), float(uncRange[1])
                if uncRange[0] < uncRange[1]:
                    self.uncRange = (uncRange[0],uncRange[1])
                else:
                    self.uncRange = (uncRange[1],uncRange[0])
                break
            except:
                continue
        while True:
            try:
                initVote = float(input("Percentage of green nodes with voting opinion (Enter a decimal value between 0 to 1): "))
                if initVote <= 1 and initVote >= 0:
                    self.initVote = initVote
                    break
                else:
                    continue
            except:
                continue
        
        
        



    # Visualisation of the current game state graph
    def showGraph(self, adj, clr):
        plt.clf()
        self.graph.clear()
        colourMap = []
        voteList = {}
        
        self.graph.add_nodes_from(self.nodes)
        
        fixPos = {}
        nrows = math.ceil(math.sqrt(self.greenNum))
        greyCount = 0
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            # If blue node
            if type(node) == Blue:
                colourMap.append("blue")
                voteList[node] = "Blue"
                fixPos[node] = (-nrows//3, nrows)
            # If red node
            elif type(node) == Red:
                colourMap.append("red")
                voteList[node] = "Red"
                fixPos[node] = (nrows//3 + nrows, nrows)
            elif type(node) == Grey:
                greyCount += 1
                if node == adj[0][0]:
                    if node.spy:
                        colourMap.append("red")
                        voteList[node] = "Spy"
                    else:
                        colourMap.append("blue")
                        voteList[node] = "Influencer"
                else:
                    colourMap.append("grey")
                    voteList[node] = "?"
                fixPos[node] = (-nrows//3, nrows - greyCount)
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
        nx.draw(self.graph, pos = pos, with_labels=False, node_color=colourMap, edge_color=[clr]*len(self.graph.edges()), node_size=[30]*len(self.nodes))
        
        labelPos = {}
        for p in pos.keys():
            labelPos[p] = (pos[p][0] - nrows/50, pos[p][1] + nrows/45)
        
        nx.draw_networkx_labels(self.graph, pos=labelPos, labels=voteList, font_size=9)
        # plt.show()
        plt.pause(0.3)

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
        
        for i in range(self.greyNum):
            spy = False
            if (i < self.greyNum * self.spyProp):
                spy = True
            self.nodes.append(Grey(spy))

    def checkWin(self):
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
    def interact(self, agent1, agent2, message):
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
            if (type(agent1) == Blue):
                if (agent2.vote):   # Voter
                    self.calcUncertainty(agent2, message["strength"], False)
                else:               # Non-voter
                    self.calcUncertainty(agent2, message["strength"], True)
            else:
                if (agent2.vote):   # Voter
                    self.calcUncertainty(agent2, message["strength"], True)
                else:               # Non-voter
                    self.calcUncertainty(agent2, message["strength"], False)
    
    def socialise(self):
        for edge in self.greenAdj:
                self.interact(edge[0], edge[1], None)
        return
    
    # Broadcasting message to all Green nodes
    def broadcast(self, message, receivers, team, penalty):
        if (team == "blue"):
            # broadcast message to all receivers
            for node in receivers:
                self.interact(node[0], node[1], message)
            if (penalty):
                self.nodes[0].energy -= message["cost"]
        else: # red team
            # broadcast message to all receivers
            for node in receivers:
                self.interact(node[0], node[1], message)
            if (penalty):
                for node in receivers:
                    if (random.random() < message["loss"]):
                        self.redAdj.remove(node)
                # lose follower
        return
    
    def endGame(self):
        return
    
    def runGame(self):
        win = self.checkWin()
        isGrey = True
        while (win == 0):
            if (len(self.nodes) == self.greenNum + 2 and isGrey):
                print("NO GREY AGENTS LEFT")
                isGrey = False
            # Red
            redMsg = self.nodes[1].chooseAction()
            if (len(self.redAdj) == 0):
                print("NO MORE FOLLOWERS")
            else:
                self.broadcast(redMsg, self.redAdj, "red", True)
                self.showGraph(self.redAdj, (1,0,0,0.4))
            
            # Blue
            blueMsg = self.nodes[0].chooseAction(self.nodes[self.greenNum + 2:])
            if (blueMsg == 1):
                grey = random.choice(list(self.nodes[self.greenNum + 2:]))
                greyAdj = list(zip([grey]*self.greenNum, self.nodes[2:self.greenNum+2]))
                if (grey.spy):
                    self.broadcast(self.nodes[1].messages["M5"], greyAdj, "red", False)
                else:
                    self.broadcast(self.nodes[0].messages["M5"], greyAdj, "blue", False)
                self.showGraph(greyAdj, (108, 122, 137, 0.4) )
                self.nodes.remove(grey)
            elif (blueMsg == -1):
                print("NO MORE ENERGY")
            else:
                self.broadcast(blueMsg, self.blueAdj, "blue", True)
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

    def initGame(self, ):
        self.startGame()
        self.createPop()
        self.runGame()

def main():
    G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,UNC_RANGE,INIT_VOTE, False, False)
    # G1 = Game(None,None,None,None,None,None,None,None)
    G1.initGame()

if __name__=="__main__":
    main()
