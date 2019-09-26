# Ryan Kupka
# 
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, distance

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def __init__(self):
        self.dc = None

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        if self.dc == None:
            self.dc = distance.Calculator(currentGameState.data.layout)


        "*** YOUR CODE HERE ***"
        #get the food positions as a list
        foodPositions = newFood.asList()
        #calculate the distance to each piece of food and add to foodDistances list
        foodDistances = [self.dc.getDistance(newPos, foodPosition) for foodPosition in foodPositions]
        #return score plus inverse of minimum food distance
        return successorGameState.getScore() + (1/min(foodDistances) if foodDistances else 1)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #for each possible action, get the value of that action and append to values list
        values = [self.value(gameState.generateSuccessor(0, action), 1, 0) for action in gameState.getLegalActions(0)]
        #return the action that has the same index as the max value
        return gameState.getLegalActions(0)[values.index(max(values))]

        util.raiseNotDefined()

    def value(self, state, index, depth):
        #increment depth for each max level
        if index == 0:
            depth += 1
        #if a terminal state is reached (pacman wins or loses or maximum depth is reached) return the value at that state
        if state.isWin() or state.isLose() or (depth == self.depth):
            return self.evaluationFunction(state)
        #if agent index is 0, the agent is pacman and is a max node
        if index == 0:
            return self.maxValue(state, index, depth)
        #if the state is not 0 and it is not a terminal state, the agent is a ghost and is a min node
        return self.minValue(state, index, depth)
        

    def maxValue(self, state, index, depth):
        v = float('inf') * -1
        for action in state.getLegalActions(index):
            v = max(v, self.value(state.generateSuccessor(index, action), (index + 1 % state.getNumAgents()), depth))
        #return the maximum value of all actions
        return v


    def minValue(self, state, index, depth):
        v = float('inf')
        for action in state.getLegalActions(index):
            v = min(v, self.value(state.generateSuccessor(index, action), ((index + 1) % state.getNumAgents()), depth))
        #return the minimum value of all actions
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        values = []
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            #append the value of each action to values list
            values.append(self.value(gameState.generateSuccessor(0, action), 1, 0, alpha, beta))
            #if the last element of values (the value corresponding to the current action) is greater than beta, break out of the for loop (prune other branches)
            if values[-1] > beta:
                break
            #if the last element is not greater than beta, alpha is equal to the max of the last element and current alpha
            alpha = max(alpha, values[-1])
        #get the maximum value
        maxVal = max(values)
        #return the action that corresponds to the maximum value
        return gameState.getLegalActions(0)[values.index(maxVal)]

        util.raiseNotDefined()

    def value(self, state, index, depth, alpha, beta):
        #increment depth for each max level
        if index == 0:
            depth += 1
        #if a terminal state is reached (pacman wins or loses or maximum depth is reached) return the value at that state
        if state.isWin() or state.isLose() or (depth == self.depth):
            return self.evaluationFunction(state)
        #if agent index is 0, the agent is pacman and is a max node
        if index == 0:
            return self.maxValue(state, index, depth, alpha, beta)
        #if the state is not 0 and it is not a terminal state, the agent is a ghost and is a min node
        return self.minValue(state, index, depth, alpha, beta)
        

    def maxValue(self, state, index, depth, alpha, beta):
        v = float('inf') * -1
        for action in state.getLegalActions(index):
            v = max(v, self.value(state.generateSuccessor(index, action), (index + 1 % state.getNumAgents()), depth, alpha, beta))
            #if v is greater than beta, return v and don't consider other actions
            if v > beta:
                return v
            #alpha is equal to the maximum of alpha and the value of the current action
            alpha = max(alpha, v)
        #return maximum value of each action (assuming this branch has not been pruned)
        return v


    def minValue(self, state, index, depth, alpha, beta):
        v = float('inf')
        for action in state.getLegalActions(index):
            v = min(v, self.value(state.generateSuccessor(index, action), ((index + 1) % state.getNumAgents()), depth, alpha, beta))
            #if v is less than alpha, return v and don't consider other actions
            if v < alpha:
                return v
            #beta is equal to the minimum of beta and the value of the current action
            beta = min(beta, v)
        #return the minimum value of each action (assuming this branch has not been pruned)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        #for each possible action, get the value of that action and append to values list
        values = [self.value(gameState.generateSuccessor(0, action), 1, 0) for action in gameState.getLegalActions(0)]
        #get the maximum value from the list of values
        maxValue = max(values)
        #return the action that has the max value
        return gameState.getLegalActions(0)[values.index(maxValue)]

        util.raiseNotDefined()

    def value(self, state, index, depth):
        #increment depth for each max level
        if index == 0:
            depth += 1
        #if a terminal state is reached (pacman wins or loses or maximum depth is reached) return the value at that state
        if state.isWin() or state.isLose() or (depth == self.depth):
            return self.evaluationFunction(state)
        #if agent index is 0, the agent is pacman and is a max node
        if index == 0:
            return self.maxValue(state, index, depth)
        #if the state is not 0 and it is not a terminal state, the agent is a ghost and is a min node
        return self.expValue(state, index, depth)
        

    def maxValue(self, state, index, depth):
        v = float('inf') * -1
        for action in state.getLegalActions(index):
            v = max(v, self.value(state.generateSuccessor(index, action), (index + 1 % state.getNumAgents()), depth))
        #return maximum value of all actions
        return v


    def expValue(self, state, index, depth):
        v = 0
        for action in state.getLegalActions(index):
            prob = 1/len(state.getLegalActions(index))
            v += prob * self.value(state.generateSuccessor(index, action), ((index + 1) % state.getNumAgents()), depth)
        #return minimum value of all actions
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: return the inverse of the minimum manhattan distance to the closest piece of food - makes pacman actively seek out food pieces
    Pacman will avoid ghosts that are 1 away from him because the score function returns a huge negative number if pacman dies
    """
    "*** YOUR CODE HERE ***"

    
    #get all food from the state
    food = currentGameState.getFood()
    #get pacmans position (x,y tuple)
    pacPos = currentGameState.getPacmanPosition()
    #convert food to list
    foodPositions = food.asList()
    #calculate manhattan distance to each piece of food and add to food distances list
    foodDistances = [abs(pacPos[0] - food[0]) + abs(pacPos[1] - food[1]) for food in foodPositions]
    #return score + inverse of smallest food distance
    return currentGameState.getScore() + (1/min(foodDistances) if foodDistances else 1)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
