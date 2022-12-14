# CITS3001 Project - Information War Game
# Author: Carmen Leong (22789943), Jordan Thompson-Giang (22729642)

# Imported libraries
# --------------------------------------------------- 
import matplotlib.pyplot as plt
import numpy as np
import math
import networkx as nx
import time
import random
import warnings


# Global Constants
# --------------------------------------------------- 
# User Inputted Parameters
GREY_NUM    = 6               # Number of grey agent
GREEN_NUM   = 60              # Number of green agent
CON_PROB    = 0.01            # Probability of connection between any 2 green nodes
SPY_PROP    = 0.35            # Proportion of Grey agents who are spies from the red team
UNC_RANGE   = (-0.5, 0.5)     # Initial uncertainty range for green nodes
INIT_VOTE   = 0.5             # Percentage of green nodes with voting opinion

# Game settings
WIN_THRESHOLD       = 0.6   # Proportion of population required with agreeing certain (uncertainty < 0) opinions for red/blue to win.
CHANGE_MAGNITUDE    = 0.5   # Scaling coefficient green-to-green uncertainty change's magnitude
CERTAINTY_SCALE     = 2     # Scaling coefficient green-to-green uncertainty influence to change
CERTAINTY_INFLUENCE = 1.5   # Scaling coefficient for broadcasting uncertainty change's magnitude
BC_INFLUENCE        = 0.05  # Scaling coefficient node uncertainty's influence over change for broadcast

# Classes for nodes
# --------------------------------------------------- 
class Blue:
    # Constructor
    def __init__(self):
        self.energy = 100
        self.messages = {
            "M1": {"cost": 1, "strength": 0.5, "message": "RED promises unrealistic policies"},
            "M2": {"cost": 2, "strength": 1.0, "message": "RED likely to be discredited"},
            "M3": {"cost": 3, "strength": 1.5, "message": "RED rumoured to be spreading misinformation"},
            "M4": {"cost": 4, "strength": 2.0, "message": "RED under investigation by federal police"},
            "M5": {"cost": 5, "strength": 2.5, "message": "RED suspected to have terrorist ties"}
        }
    
    # Method that prompts user for Blue team action
    def userAction(self, greyAgents):
        greyNum = len(greyAgents)
        # No possible actions
        if greyNum <= 0 and self.energy <= 0:
            return -1
        if greyNum > 0:
            while True:
                try:
                    g = input(f"Would you like to introduce a Grey agent? (Enter y/n): ")
                    if g == "y":
                        print()
                        return 1
                    elif g == "n":
                        break
                    continue
                except KeyboardInterrupt:
                    exit()
                except:
                    continue
            print()
        if self.energy > 0:
            print(f"---- Message Options for Blue {'-'*70}")
            print(f"{'Message':48}{'Strength':15}{'Energy Cost'}")
            print(f"1. {self.messages['M1']['message']:45}{self.messages['M1']['strength']:<15}{self.messages['M1']['cost']}")
            print(f"2. {self.messages['M2']['message']:45}{self.messages['M2']['strength']:<15}{self.messages['M2']['cost']}")
            print(f"3. {self.messages['M3']['message']:45}{self.messages['M3']['strength']:<15}{self.messages['M3']['cost']}")
            print(f"4. {self.messages['M4']['message']:45}{self.messages['M4']['strength']:<15}{self.messages['M4']['cost']}")
            print(f"5. {self.messages['M5']['message']:45}{self.messages['M5']['strength']:<15}{self.messages['M5']['cost']}")
            print(f"{'-'*100}")
            while True:
                try:
                    m = int(input("\nWhich message would you like to select? (Enter an integer between 1-5): "))
                    if m > 0 and m <=5:
                        if m > self.energy:
                            print("Not enough energy")
                            continue
                        print()
                        return self.messages[f"M{m}"]
                except KeyboardInterrupt:
                    exit()
                except:
                    continue
        else:
            return -1

    def M1AIAction(self,greyAgents,game):
        # Randomly chooses between grey node and broadcast
        if (len(greyAgents) != 0 and self.energy == 0):
            return 1

        if (self.energy == 0):
            return -1
        else:
            return self.messages["M1"]

    def M5AIAction(self,greyAgents,game):
        # Randomly chooses between grey node and broadcast
        if (len(greyAgents) != 0 and self.energy == 0):
            return 1

        if (self.energy == 0):
            return -1
        elif self.energy >= 5:
            return self.messages["M5"]
        else:
            return self.messages[f"M{self.energy}"]

    def randomAIAction(self,greyAgents):
        # Randomly chooses between grey node and broadcast
        if (len(greyAgents) != 0 and random.random() < 0.1):
            return 1

        if (self.energy == 0):
            return -1
        while (True):
            msg = random.choice(list(self.messages.values()))
            if (msg["cost"] <= self.energy):
                return msg

    # Blue agent that chooses an action based on a set policy
    def AIAction(self, greyAgents, game):
        if (self.energy == 0):
            if len(greyAgents) > 0:
                return 1
            else:
                return -1
        if (self.energy <= 10) and (len(greyAgents) > 0) and (random.random() < 0.5):
                return 1
        Vperc, NVperc = game.calcVoters()
        if Vperc <= 70 and self.energy >= 5:
            if self.energy >= 30:
                return self.messages["M5"]
            elif self.energy >= 20:
                return self.messages["M4"]
            else:
                return self.messages["M3"]
        elif Vperc <= 75 and self.energy >= 4:
            if self.energy >= 25:
                return self.messages["M4"]
            elif self.energy >= 15:
                return self.messages["M3"]
            else:
                return self.messages["M2"]
        elif Vperc <= 80 and self.energy >= 3:
            if self.energy >= 20:
                return self.messages["M3"]
            elif self.energy >= 10:
                return self.messages["M2"]
            else:
                return self.messages["M1"]
        if Vperc <= 85 and self.energy >= 2:
            if self.energy >= 10:
                return self.messages["M2"]
            else:
                return self.messages["M1"]
        else:
            return self.messages["M1"]

    # Method for Blue choosing an action
    def chooseAction(self, greyAgents, game):
        if game.blueIsAi:
            return self.AIAction(greyAgents, game)
        else:
            return self.userAction(greyAgents)

class Red:
    # Constructor
    def __init__(self):
        self.messages = {
            "M1": {"loss": 0.02, "strength": 1.0, "message": "Blue is racist"},
            "M2": {"loss": 0.03, "strength": 1.5, "message": "Blue supports child labour"},
            "M3": {"loss": 0.04, "strength": 2.0, "message": "Blue is corrupted"},
            "M4": {"loss": 0.05, "strength": 2.5, "message": "Blue supports human experimentation"},
            "M5": {"loss": 0.06, "strength": 3.0, "message": "Blue uses robots birds to spy on population"}
        }

    # Method that prompts user for Red team action
    def userAction(self, game):
        if len(game.redAdj) > 0:
            print(f"---- Message Options for Red {'-'*71}")
            print(f"{'Message':48}{'Strength':15}{'Probability of follower lost'}")
            print(f"1. {self.messages['M1']['message']:45}{self.messages['M1']['strength']:<15}{self.messages['M1']['loss']}")
            print(f"2. {self.messages['M2']['message']:45}{self.messages['M2']['strength']:<15}{self.messages['M2']['loss']}")
            print(f"3. {self.messages['M3']['message']:45}{self.messages['M3']['strength']:<15}{self.messages['M3']['loss']}")
            print(f"4. {self.messages['M4']['message']:45}{self.messages['M4']['strength']:<15}{self.messages['M4']['loss']}")
            print(f"5. {self.messages['M5']['message']:45}{self.messages['M5']['strength']:<15}{self.messages['M5']['loss']}")
            print(f"{'-'*100}")
            while True:
                try:
                    m = int(input("\nWhich message would you like to select? (Enter an integer between 1-5): "))
                    if m >= 0 and m <=5:
                        print()
                        return self.messages[f"M{m}"]
                except KeyboardInterrupt:
                        exit()
                except:
                    continue

    def M1AIAction(self):
        return self.messages["M5"]

    def M5AIAction(self):
        return self.messages["M5"]

    def randomAIAction(self):
        return random.choice(list(self.messages.values()))

    # Red agent that chooses an action based on a set policy
    def AIAction(self, game):
        Vperc, NVperc = game.calcVoters()
        followers = len(game.redAdj)/ game.greenNum
        if NVperc <= 70:
            if followers >= 0.5:
                return self.messages["M5"]
            else:
                return self.messages["M4"]
        elif NVperc <= 75:
            if followers >= 0.5:
                return self.messages["M4"]
            else:
                return self.messages["M3"]
        elif NVperc <= 80:
            if followers >= 0.5:
                return self.messages["M3"]
            else:
                return self.messages["M2"]
        if NVperc <= 85:
            if followers >= 0.5:
                return self.messages["M2"]
            else:
                return self.messages["M1"]
        else:
            return self.messages["M1"]

    # Method for Blue choosing an action
    def chooseAction(self, game):
        if game.redIsAi:
            return self.AIAction(game)
        else:
            return self.userAction(game)

class Green:
    # Constructor
    def __init__(self, vote, uncertainty):
        self.vote = vote
        self.uncertainty = uncertainty
class Grey:
    # Constructor
    def __init__(self, spy):
        self.spy = spy
        self.messages = {
            "BLUE": {"strength": 2.5, "message": "We encourage everyone to vote"},
            "RED": {"strength": 6.0, "message": "Voting doesn't make a difference!"}
        }


# Classes for game
# --------------------------------------------------- 
class Game:
    # Constructor
    def __init__(self, greyNum, greenNum, connectProb, spyProp, uncRange, initVote, redIsAi, blueIsAi):
        # User Inputted Parameters
        self.greyNum = greyNum
        self.greenNum = greenNum
        self.connectProb = connectProb
        self.spyProp = spyProp
        self.uncRange = uncRange
        self.initVote = initVote
        
        # AI/Human settings for the game
        self.redIsAi = redIsAi
        self.blueIsAi = blueIsAi

        # Game objects
        self.graph = nx.Graph()     # The graphical visualisation network object
        self.nodes = []             # Holds all of the agents in the game [Blue, Red, Greens, Greys]
        self.greenAdj = []          # Adjacency list for the Green network
        self.redAdj = []            # Adjacency list for the Red Agent
        self.blueAdj = []           # Adjacency list for the Blue Agent

    # Method that prompts user for game set-up settings
    def startGame(self):
        print(f"\n==== WELCOME TO INFORMATION WAR GAME {'='*63}")
        print(f"---- Game Settings {'-'*81}\n")

        while True:
            try:
                redPlayer = input(f"{'      Red Team (Enter AI/Human):  '} ").lower()
                if redPlayer == "ai" or redPlayer =="human":
                    self.redIsAi = False if redPlayer == "human" else True
                    break
            except KeyboardInterrupt:
                exit()
        while True:
            bluePlayer = input(f"{'      Blue Team (Enter AI/Human): '} ").lower()
            if bluePlayer == "ai" or bluePlayer == "human":
                self.blueIsAi = False if bluePlayer == "human" else True
                break
        while True:
            default = input("\n      Would you like to use the default game settings? (Enter y/n): ").lower()
            if default == "y":
                print()
                return
            else:
                break
        while True:
            try:
                greenNum = int(input("Number of green agents (Enter an integer): "))
                self.greenNum = greenNum
                break
            except KeyboardInterrupt:
                exit()
            except:
                continue
        while True:
            try:
                greyNum = int(input("Number of grey agents (Enter an integer): "))
                self.greyNum = greyNum
                break
            except KeyboardInterrupt:
                exit()
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
            except KeyboardInterrupt:
                exit()
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
            except KeyboardInterrupt:
                exit()
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
            except KeyboardInterrupt:
                exit()
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
            except KeyboardInterrupt:
                exit()
            except:
                continue
        print()
        
        
    # Calculate percentage of voters and non-voters   
    def calcVoters(self):
        V, NV = 0, 0
        for node in self.nodes[2:self.greenNum+2]:
            if node.vote == True:
                V += 1
            else:
                NV += 1
        Vperc = V/self.greenNum * 100
        NVperc =NV/self.greenNum * 100
        return (Vperc, NVperc)


    # Visualisation of the current game state graph
    def showGraph(self, adj, clr, grey=None):
        plt.clf()
        self.graph.clear()
        colourMap = []
        voteList = {}
        
        gNodes = self.nodes[:self.greenNum + 2]
        if (len(self.nodes) != (self.greenNum + 2)):
            if grey == None:
                gNodes.append(self.nodes[self.greenNum+2])
            else:
                gNodes.append(grey)
            
        self.graph.add_nodes_from(gNodes)
        
        fixPos = {}
        nrows = math.ceil(math.sqrt(self.greenNum))
        for i in range(len(gNodes)):
            node = gNodes[i]
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
                if grey!=None:
                    if node.spy:
                        colourMap.append("red")
                        voteList[node] = "Spy"
                    else:
                        colourMap.append("blue")
                        voteList[node] = "Influencer"
                else:
                    colourMap.append("grey")
                    voteList[node] = f"x{len(self.nodes) - (self.greenNum + 2)}"
                fixPos[node] = (-nrows//3, nrows - 1)
            else:
                fixPos[node] = ((i-2) % nrows, (i-2) // nrows)
                if node.vote:
                    colourMap.append( (0, 0.5, 1) )
                    voteList[node] = f"Vote"
                else:
                    colourMap.append( (1, 0.5, 0) )
                    voteList[node] = f"Not Vote"
                
        self.graph.add_edges_from(adj)
        
        pos = nx.spring_layout(self.graph, pos=fixPos, fixed=gNodes)
        nx.draw(self.graph, pos = pos, with_labels=False, node_color=colourMap, edge_color=clr, node_size=30)
        
        labelPos = {}
        for p in pos.keys():
            labelPos[p] = (pos[p][0] - nrows/50, pos[p][1] + nrows/45)
        
        nx.draw_networkx_labels(self.graph, pos=labelPos, labels=voteList, font_size=9)
        plt.pause(0.2)

    # Create green node network connections
    def connectGreen(self):
        self.greenAdj = []
        
        # Generate random edges
        for i in range(2, 2+self.greenNum):
            for j in range(i+1, 2+self.greenNum):
                if (random.random() < self.connectProb):
                    self.greenAdj.append( (self.nodes[i], self.nodes[j]) )
    
    # Creates an initial game state graph 
    def createPop(self):
        self.nodes = [Blue(), Red()]
        
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
            if (i+1 <= self.greyNum * self.spyProp):
                spy = True
            self.nodes.append(Grey(spy))
    
    # Checks the current game state to see if any team has met the winning conditions
    def checkWin(self):
        if (self.nodes[0].energy == 0 and len(self.redAdj) == 0 and len(self.nodes) == self.greenNum + 2):
            Voters = 0
            NonVoters = 0
            for k in range(self.greenNum):
                node = self.nodes[k+2]
                if (node.vote):
                    Voters += 1
                else:
                    NonVoters += 1
            if Voters >= NonVoters:
                return 1
            else:
                return 2

        # No actions available, higher proportion wins
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
    
    # Green-to-Green uncertainty interaction calculation
    def calcUncertainty(self, agent, diff, increase):
        if increase:
            agent.uncertainty += (CHANGE_MAGNITUDE * diff) / math.pow(CERTAINTY_SCALE, (1 - agent.uncertainty))
        else:
            agent.uncertainty -= (CHANGE_MAGNITUDE * diff) / math.pow(CERTAINTY_SCALE, (1 - agent.uncertainty))

        # Opinion swap
        if (agent.uncertainty > 1):
            overflow = agent.uncertainty - 1
            agent.vote = not agent.vote
            agent.uncertainty = 1 - overflow
        
        if (agent.uncertainty < -1):
            agent.uncertainty = -1.0
    
    # Other-to-Green uncertainty interaction calculation
    def calcInfluence(self, agent, strength, increase):
        if increase:
            agent.uncertainty += (agent.uncertainty+CERTAINTY_INFLUENCE)*strength*BC_INFLUENCE
        else:
            agent.uncertainty -= (agent.uncertainty+CERTAINTY_INFLUENCE)*strength*BC_INFLUENCE

        # Opinion swap
        if (agent.uncertainty > 1):
            overflow = agent.uncertainty - 1
            agent.vote = not agent.vote
            agent.uncertainty = 1 - overflow
        
        if (agent.uncertainty < -1):
            agent.uncertainty = -1.0

    # In the case of an other-to-Green interaction, @param agent1 is passed as red/blue/grey
    def interact(self, agent1, agent2, message):
        # Green-to-Green interaction
        if (type(agent1) == Green and type(agent2) == Green):
            # Agreeing opinions
            if (agent1.vote == agent2.vote):
                uncDiff = abs(agent1.uncertainty - agent2.uncertainty)
                if agent1.uncertainty < agent2.uncertainty:
                    self.calcUncertainty(agent1, uncDiff, True)
                    self.calcUncertainty(agent2, uncDiff, False)
                else:
                    self.calcUncertainty(agent1, uncDiff, False)
                    self.calcUncertainty(agent2, uncDiff, True)
            # Differing opinions
            else:
                uncDiff = (1 - agent1.uncertainty) + (1 - agent2.uncertainty)
                self.calcUncertainty(agent1, uncDiff, True)
                self.calcUncertainty(agent2, uncDiff, True)
        # Other-to-Green interaction
        else:
            if (type(agent1) == Blue):
                if (agent2.vote):   # Voter
                    self.calcInfluence(agent2, message["strength"], False)
                else:               # Non-voter
                    self.calcInfluence(agent2, message["strength"], True)
            else:
                if (agent2.vote):   # Voter
                    self.calcInfluence(agent2, message["strength"], True)
                else:               # Non-voter
                    self.calcInfluence(agent2, message["strength"], False)
    
    # Green network communications within itself along the existing network connections
    def socialise(self):
        for edge in self.greenAdj:
                self.interact(edge[0], edge[1], None)
        return
    
    # Broadcasting message to all Green nodes
    def broadcast(self, message, receivers, team, penalty):
        if (team == "blue"):
            # broadcast message to all receivers
            for node in receivers:
                self.interact(self.nodes[0], node[1], message)
            if (penalty):
                self.nodes[0].energy -= message["cost"]
        else: # red team
            # broadcast message to all receivers
            for node in receivers:
                self.interact(self.nodes[1], node[1], message)
            if (penalty):
                for node in receivers:
                    if (random.random() < message["loss"]):
                        self.redAdj.remove(node)
        return
    
    # Calculates and prints out the proportion of Voters and Non-Voters
    def printStat(self):
        V, NV = 0, 0
        for node in self.nodes[2:self.greenNum+2]:
            if node.vote == True:
                V += 1
            else:
                NV += 1
        
        VStr = f"{round(V/self.greenNum * 100,1)}% ({V})"
        NVStr = f"{round(NV/self.greenNum * 100,1)}% ({NV})"
        
        print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}")
        print(f"{'|':>10}{'Proportion of Voters':^30}{'|':<10}{'|':>10}{'Proportion of Non-Voters':^30}{'|':<10}")
        print(f"{'|':>10}{VStr:^30}{'|':<10}{'|':>10}{NVStr:^30}{'|':<10}")
        print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}\n")

    # Starts the game and controls the overall flow of the game.
    def runGame(self, fastMode):
        win = self.checkWin()
        
        round = 1       # Game starts from round 1
        times = []      # Used for timing round lengths
        while (win == 0):
            turnStart = time.time()
            if (not fastMode):
                # Round Begins
                print(f"============================================= ROUND  {round} =============================================\n")
                self.showGraph([], (0,0,0,0))
                
                # Red's turn begins
                print(f"-------------------------------------------- Red's Turn --------------------------------------------\n")
                
                self.printStat()

                print(f"{'-'*90:^100}\n")
                
                print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}")
                print(f"{'|':>10}{'Number of Followers':^30}{'|':<10}{'|':>10}{'Grey Agents Available':^30}{'|':<10}")
                print(f"{'|':>10}{len(self.redAdj):^30}{'|':<10}{'|':>10}{len(self.nodes) - (self.greenNum + 2):^30}{'|':<10}")
                print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}\n")
            
            redMsg = self.nodes[1].chooseAction(self)
            
            if (not fastMode):
                actionStr = f"Red has broadcasted '{redMsg['message']}' to {len(self.redAdj)} followers"
                print(f"{'-'*94:^100}")
                print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                print(f"{'-'*94:^100}\n")
            
            if (len(self.redAdj) != 0):
                self.broadcast(redMsg, self.redAdj, "red", True)
                
            if (not fastMode):
                self.showGraph(self.redAdj, (1,0,0,0.4))
                
                # Blue's turn
                print(f"------------------------------------------- Blue's Turn --------------------------------------------\n")
                
                self.printStat()
                
                print(f"{'-'*90:^100}\n")
                
                print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}")
                print(f"{'|':>10}{'Energy Available':^30}{'|':<10}{'|':>10}{'Grey Agents Available':^30}{'|':<10}")
                print(f"{'|':>10}{self.nodes[0].energy:^30}{'|':<10}{'|':>10}{len(self.nodes) - (self.greenNum + 2):^30}{'|':<10}")
                print(f"{'-'*30:>40}{' '*20}{'-'*30:<40}\n")
                
            blueMsg = self.nodes[0].chooseAction(self.nodes[self.greenNum + 2:],self)
            
            # If Blue chooses to introduce a Grey Agent
            if (blueMsg == 1):
                
                if (not fastMode):
                    actionStr = f"Blue has introduced a Grey agent"
                    print(f"{'-'*94:^100}")
                    print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                    print(f"{'-'*94:^100}\n")
                    
                    print(f"------------------------------------------- Grey's Turn --------------------------------------------\n")
                
                grey = random.choice(list(self.nodes[self.greenNum + 2:]))
                greyAdj = list(zip([grey]*self.greenNum, self.nodes[2:self.greenNum+2]))
                if (grey.spy):
                    actionStr = f"Grey is a Spy, it has broadcasted '{grey.messages['RED']['message']}' to EVERYONE!"
                    self.broadcast(grey.messages["RED"], greyAdj, "red", False)
                else:
                    actionStr = f"Grey is an Influencer, it has broadcasted '{grey.messages['BLUE']['message']}' to EVERYONE!"
                    self.broadcast(grey.messages["BLUE"], greyAdj, "blue", False)
                if (not fastMode):
                    print(f"{'-'*94:^100}")
                    print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                    print(f"{'-'*94:^100}\n")
                    self.showGraph(greyAdj, (0.5,0.5,0.5,0.4), grey)
                self.nodes.remove(grey)
            
            # If Blue does not make an action
            elif (blueMsg == -1):
                if (not fastMode):
                    actionStr = f"Blue does not make an action"
                    print(f"{'-'*94:^100}")
                    print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                    print(f"{'-'*94:^100}\n")
            
            # If Blue chooses to broadcast a message
            else:
                if (not fastMode):
                    actionStr = f"Blue has broadcasted '{blueMsg['message']}' to EVERYONE"
                    print(f"{'-'*94:^100}")
                    print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                    print(f"{'-'*94:^100}\n")
                self.broadcast(blueMsg, self.blueAdj, "blue", True)
                if (not fastMode):
                    self.showGraph(self.blueAdj, (0,0,1,0.4))

            # Green's Turn
            if (not fastMode):
                print(f"------------------------------------------- Green's Turn -------------------------------------------\n")
                self.printStat()
                actionStr = f"Green has socialised"
                print(f"{'-'*94:^100}")
                print(f"{'|':>3}{actionStr:^94}{'|':<3}")
                print(f"{'-'*94:^100}\n")
            
            self.socialise()
            if (not fastMode):
                self.showGraph(self.greenAdj, (0,1,0,0.4))
            
            # Dynamic change of the Green network
            self.connectGreen()
                
            # Check win
            win = self.checkWin()
            # Increment round
            round += 1
            # Timing information
            turnEnd = time.time()
            times.append(turnEnd - turnStart)
            
        if (not fastMode):
            print(f"Total rounds: {round}")
        return win, round, times

    # Initialise the game state
    def initGame(self, fastMode):
        if (not fastMode):
            self.startGame()
        self.createPop()
        return self.runGame(fastMode)

def main(simulate = False):
    # Warning suppressions to ensure the terminal visualisations are uninterrupted
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    warnings.filterwarnings("ignore")
    
    # Simulation (development feature)
    if simulate:
        total = 100
        
        variable = [(-0.5, 0.5)]
        for trial in variable:
            blue = 0
            red = 0
            gameTimes = []
            gameRounds = []
            redWinRounds = []
            blueWinRounds = []
            gameDurations = []
            for i in range(total):
                G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,trial,INIT_VOTE, True, True)
                gameStart = time.time()
                result, rounds, times = G1.initGame(True)
                gameEnd = time.time()
                if result == 1:
                    blue += 1
                    blueWinRounds.append(rounds)
                else:
                    red += 1
                    redWinRounds.append(rounds)
                
                gameTimes.append(sum(times)/rounds)
                gameRounds.append(rounds)
                gameDurations.append(gameEnd - gameStart)
            
            print(f"\nUncertainty Interval: {trial}")
            print(f"\tBlue: {round(blue*100/total, 2)}%\tRed: {round(red*100/total, 2)}%")
            print(f"\tAverage game duration:\t\t{sum(gameDurations)/len(gameDurations)}")
            print(f"\tAverage rounds per game:\t{sum(gameRounds)/len(gameRounds)}")
            print(f"\tAverage rounds it takes for Blue to win: \t{round(sum(blueWinRounds)/len(blueWinRounds),1)}")
            print(f"\tAverage rounds it takes for Red to win: \t{round(sum(redWinRounds)/len(redWinRounds),1)}")
            print(f"\tAverage seconds per round:\t{sum(gameTimes)/len(gameTimes)}")
    
    # Runs the game
    else:
        G1 = Game(GREY_NUM,GREEN_NUM,CON_PROB,SPY_PROP,UNC_RANGE,INIT_VOTE,False,False)
        result, rounds, times = G1.initGame(False)
        if result == 1:
            print("Blue Won")
        else:
            print("Red Won")

if __name__=="__main__":
    main()
