from typing import Any
import numpy as np
from utils.graph import Graph, Vertex
from utils.priority_queue import PriorityQueue

def load_location_data(graph: Graph, filename: str) -> None:
    """
    Load location data from a file.
    Format: Vertex,XCord|Latitude,YCord|Longitude or modify it to whatever you want

    Args:
        graph (Graph): graph to be filled with data.
    """
    with open(filename, 'r') as file:
        for line in file:
            v_k, x, y : str = line.rstrip('\n').split(',')
            vertex : Vertex = graph.get_vertex(v_k)
            vertex.location = (float(x), float(y))

def build_graph_from_list(data: list) -> Graph:
    """
    Given a list of tuples, build a graph

    Args:
        # Here each vertex is a key, so it can be anything
        data (list): list of tuples (vertex1 : Any, vertex2 : Any, weight : int/float)

    Returns:
        Graph
    """
    graph = Graph()
    for vk_1, vk_2, weight in data:
        graph.add_edge(vk_1, vk_2, weight)
    
    return graph

def load_from_file(filename : str) -> Graph:
    """
    Load data from a file to build a Graph
    Extension: .txt - .csv
    Data format: VertexKey,VertexKey,weight
    ## Example: Berlin,Amsterdam,655
    
    Args:
        filename (str): Name of the file

    Returns:
        Graph: graph loaded with data.
    """
    
    data : list[tuple] = []
    with open(filename, 'r') as file: 
        for line in file:
            vertex1, vertex2, weight = line.rstrip('\n').split(',')
            data.append((vertex1, vertex2, int(weight)))
    
    return build_graph_from_list(data)

def get_path(graph: Graph, to: Any) -> list[Any]:
    """
    Get the path from a certain vertex to another.
    @Important: Impossible path not checked.

    Args:
        graph (Graph): Graph where the vertex are contained
        to (Any): end vertex

    Returns:
        list[Any]: path
    """
    it : Vertex = graph.get_vertex(to)
    path : list[Any] = [it.key]
    while it.predecessor:
        path.append(it.predecessor.key)
        it = it.predecessor
    
    return path[::-1]
    
def heuristic_value(a: Vertex, end: Vertex):
    """
    Choose a proper heuristic value here. For this we are doing a simple Mannhatan distance

    Args:
        a (Vertex): Any vertex from the graph
        b (Vertex): End point
    """
    loc_diff = end.location - a.location
    return loc_diff[0] + loc_diff[1]

def dijkstras_algorithm(graph: Graph, start: Vertex, end: Vertex) -> None:
    """
    Dijkstra's Algorithm
    Intended Big-O: O( (V + E) * log(V) )

    Args:
        graph (Graph): graph to run the Dijkstra's Algorithm
        start (Vertex): starting vertex
    """
    
    pq : PriorityQueue[int, Vertex] = PriorityQueue(descending = False)
    for v in graph:
        v.dist = np.Inf
    
    start.dist = 0
    pq.build_heap([(v.dist, v) for v in graph])
    while not pq.empty():
        current : Vertex = pq.advance()
        if current == end:
            # We're already there
            break
        for next in current.get_connections():
            new_dist = current.dist + current.get_weight(next)
            if new_dist < next.dist:
                next.dist = new_dist
                next.predecessor = current
                pq.decrease_key(next, new_dist)

def a_star_algorithm(graph: Graph, start: Vertex, end: Vertex) -> None:
    """
    A* Star Algorithm

    Args:
        graph (Graph): graph to run the A* Algorithm
        start (Vertex): starting vertex
    """
    
    pq : PriorityQueue[int, Vertex] = PriorityQueue(descending = False)
    for v in graph:
        v.dist = np.Inf
    
    start.dist = 0
    pq.build_heap([(v.dist, v) for v in graph])
    while not pq.empty():
        current : Vertex = pq.advance()
        if current == end:
            # We're already there
            break
        for next in current.get_connections():
            # Calculate g:
            new_dist = current.dist + current.get_weight(next)
            # Calculate f for the priority queue:
            f = new_dist + heuristic_value(next, end)
            if new_dist < next.dist:
                next.dist = new_dist
                next.predecessor = current
                pq.decrease_key(next, f)
