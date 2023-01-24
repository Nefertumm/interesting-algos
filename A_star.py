from typing import Any
import numpy as np
import time as tm
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
            v_k, x, y = line.rstrip('\n').split(',')
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

def load_heuristic_data(graph : Graph, filename : str) -> None:
    """
    Loads heuristic data from file to the graph.

    Args:
        graph (Graph): Graph
        filename (str): File name.
    """
    with open(filename, 'r') as file:
        for line in file:
            v_k, heur = line.rstrip('\n').split(',')
            vertex = graph.get_vertex(v_k)
            vertex.heuristic = int(heur)

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
    Actual example: we just have pre-calculated heuristic data, so we don't need to use two vertex, I keep it this way as
    for complex cases we would want to calculate it.

    Args:
        a (Vertex): Any vertex from the graph
        b (Vertex): End point
    """
    #loc_diff = end.location - a.location
    #return loc_diff[0] + loc_diff[1]
    return a.heuristic

def dijkstras_algorithm(graph: Graph, start: Vertex, end: Vertex) -> None:
    """
    Dijkstra's Algorithm
    Intended Big-O: O( (V + E) * log(V) )

    Args:
        graph (Graph): graph to run the Dijkstra's Algorithm
        start (Vertex): starting vertex
    """
    
    # counter
    operations : int = 0
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
            operations += 1
            new_dist = current.dist + current.get_weight(next)
            if new_dist < next.dist:
                next.dist = new_dist
                next.predecessor = current
                pq.decrease_key(next, new_dist)

    print(operations)

def a_star_algorithm(graph: Graph, start: Vertex, end: Vertex) -> None:
    """
    A* Star Algorithm

    Args:
        graph (Graph): graph to run the A* Algorithm
        start (Vertex): starting vertex
    """
    
    # counter
    operations : int = 0
    pq : PriorityQueue[int, Vertex] = PriorityQueue(descending = False)
    for v in graph:
        v.dist = np.Inf
    
    start.dist = 0
    # this will know which nodes were already added to the queue.
    visited : dict[Vertex, bool] = {start: True}
    pq.insert((start.dist, start))
    while not pq.empty():
        current : Vertex = pq.advance()
        if current == end:
            # We're already there
            break
        for next in current.get_connections():
            operations += 1
            # Calculate g:
            new_dist = current.dist + current.get_weight(next)
            # Calculate f for the priority queue:
            f = new_dist + heuristic_value(next, end)
            if new_dist < next.dist:
                next.dist = new_dist
                next.predecessor = current
                if next in visited:
                    pq.decrease_key(next, f)
                else:
                    pq.insert((f, next))
                    visited[next] = True
    
    print(operations)

if __name__ == '__main__':
    graph1 = load_from_file('data.txt')
    load_heuristic_data(graph1, 'heuristics.txt')
    start = tm.perf_counter()
    a_star_algorithm(graph1, graph1.get_vertex('A'), graph1.get_vertex('J'))
    end = tm.perf_counter()
    print(get_path(graph1, 'J'), 'Time: ', end - start)
    
    
    graph2 = load_from_file('data.txt')
    load_heuristic_data(graph2, 'heuristics.txt')
    start = tm.perf_counter()
    dijkstras_algorithm(graph2, graph2.get_vertex('A'), graph2.get_vertex('J'))
    end = tm.perf_counter()
    print(get_path(graph2, 'J'), 'Time: ', end - start)