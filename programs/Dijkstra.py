'''
given a matrix with m rows and n columns, m adjacent numbers are chosen from m rows, where two numbers are adjacent to each other if they are directly connected vertically and diagonally. Design a dynamic programming algorithm to find the smallest sum

'''
from Bridges.GraphAdjList import *
from heapq import heappush, heappop

class Dijkstra():
    def __init__(self, inputFile, startingVertex, goalVertex):
        # an initially empty dictionary containing mapping: vertex: [child, weight]
        self.adjacency = {}
        # collection of vertices
        self.vertices = []
        # each dictionary entry contains mapping of vertex:parent
        self.parent = {}
        # startingVertex, goalVertex
        self.startingVertex, self.goalVertex = startingVertex, goalVertex

        self.visited = []

        # The following reads in the input file and constructs an adjacency list of the graph.
        graph = open(inputFile)
        for line in graph:
            entry = line.split()

            # get the vertices
            self.vertices.append(entry[0])
            self.vertices.append(entry[1])

            if entry[0] not in self.adjacency:
                self.adjacency[entry[0]] = []

            # construct an edge for the adjacency list
            edge = (entry[1], int(entry[2]))
            self.adjacency[entry[0]].append(edge)

        # remove duplication in vertices
        self.vertices = list(set(self.vertices))

        # checking if start and goal are in vertices
        if startingVertex not in self.vertices:
            print('Starting vertex', startingVertex, 'not present in graph')
            quit()
        elif goalVertex not in self.vertices:
            print('Goal vertex', goalVertex, 'not present in graph')
            quit()

        # create Bridges graph
        self.g = GraphAdjList()
        for vertex in self.vertices:
            self.g.add_vertex(vertex, "")
            self.g.get_vertices().get(vertex).get_visualizer().set_color("red")
        
        for vertex in self.adjacency:
            for edge in self.adjacency[vertex]:
                self.g.add_edge(vertex, edge[0], edge[1])

    # solve it using Dijkstra algorithm
    #[priority_of_vertex, vertex, parent_vertex]
    def solve(self):
        heap = []
        #push first vertex onto priority queue
        heappush(heap, (0, self.startingVertex, None))
        #parent of first node is None
        self.parent[self.startingVertex] = None

        while heap:
            #pop lowest weight from priority queue
            temp = heappop(heap)
            
            #if vertex (temp[1]) has not been visited
            if temp[1] not in self.visited:
                #add vertex to visited list
                self.visited.append(temp[1])
                #assign parent(temp[2]) to current vertex (temp[1])
                self.parent[temp[1]] = temp[2]
                if temp[1] == self.goalVertex:
                    print(self.parent)
                    return True
                #push all values adjacent to current vertex onto priority queue
                for value in self.adjacency[temp[1]]:
                    print(value)
                    #[vertex, weight]
                    heappush(heap, (temp[0] + value[1], value[0], temp[1]))
                    

                



    # retrieve the path from start to the goal 
    def find_path(self):
        self.path = []
        # your code goes here:
        temp = self.goalVertex
        while temp != None:
            self.path.append(temp)
            temp = self.parent[temp]
        self.path.reverse()
        print(self.path)




    
    # draw the path as red
    def draw_path(self):
        for i in range(len(self.path)-1):
            self.g.get_link_visualizer(self.path[i], self.path[i+1]).set_color("red")

    # return the Bridges object
    def get_graph(self):
        return self.g
