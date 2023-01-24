from __future__ import annotations
from typing import Any
# Uncomment if you have pyvis
#from pyvis.network import Network

class Location:
    """Change this as whatever you want.
    """
    def __init__(self, x : float|int = 0, y : float|int = 0) -> None:
        self._x = x
        self._y = y
    
    @property
    def x(self) -> float|int:
        return self._x
    
    @x.setter
    def x(self, new_x : float|int) -> None:
        self._x = new_x
    
    @property
    def y(self) -> float|int:
        return self._y
    
    @y.setter
    def y(self, new_y : float|int) -> None:
        self._y = new_y

    def __sub__(self, b : Location):
        return (self.x - b.x, self.y - b.y)
    
    def __add__(self, b : Location):
        return (self.x + b.x, self.y + b.y)

class Vertex:
    """
    Represents each vertex on the graph, it uses a dictionary to connect each one of them.
    """
    def __init__(self, key : Any) -> None:
        self._id : Any = key
        self.connected_to : dict[Any, int] = {}
        self._dist : int = 0
        self._predecessor : Vertex = None
        # This can be changed to everything, used to calculate the heuristic value between 2 vertices.
        # I.E. lets say you're trying to find the best route between two cities, then your geo position would be
        # the coordinates of that city, and to calculate the heuristic you could use the distance between them.
        # The same could work with a grid for a videogame too.
        self._location : Location = None
        # If we have the heuristics pre-calculated, we could use it as well
        self._heuristic : float|int = 0
    
    def add_neighbor(self, neighbor : Any , weight : int = 0):
        """
        Adds a key as neighbor of another vertex with a certain weight

        Parameters
        ----------
        neighbor : Any
            Key of vertex' neighbor
        weight : int, optional
            Weight of the edge that connects both vertices. The default is 0.

        Returns
        -------
        None

        """
        self.connected_to[neighbor] = weight
    
    def __str__(self) -> str:
        return str(self._id) + 'connected to' + str([x._id for x in self.connected_to])
    
    def get_connections(self) -> list[Any]:
        """
        Get all the keys of neighbor vertices

        Returns
        -------
        list
            List of vertices' keys.

        """
        return self.connected_to.keys()
    
    @property
    def key(self) -> Any:
        return self._id
    
    @property
    def dist(self) -> int:
        return self._dist
    
    @dist.setter
    def dist(self, new_dist: int) -> None:
        self._dist = new_dist
        
    @property
    def predecessor(self) -> Vertex:
        return self._predecessor
    
    @predecessor.setter
    def predecessor(self, new_predecessor) -> None:
        self._predecessor = new_predecessor
    
    @property
    def location(self) -> Location:
        return self._location
    
    @location.setter
    def location(self, new_location : Location) -> None:
        self._location = new_location
        
    @property
    def heuristic(self) -> float|int:
        return self._heuristic
    
    @heuristic.setter
    def heuristic(self, new_heuristic : float|int) -> None:
        self._heuristic = new_heuristic
        
    def get_weight(self, neighbor : Any) -> int:
        """
        Get the weight of the edge from the key of neighbor

        Parameters
        ----------
        neighbor : Any
            The key of the neighbor

        Returns
        -------
        int
            Weight

        """
        return self.connected_to[neighbor]
    
class Graph:
    def __init__(self) -> None:
        self.vertex_list : dict[Any, Vertex] = {}
        self.total_vert : int = 0
    
    def add_vertex(self, key : Any) -> Vertex:
        """
        Adds a vertex with a key.

        Parameters
        ----------
        key : Any
            Key of the vertex

        Returns
        -------
        Vertex
            Vertex added.

        """
        self.total_vert += 1
        new_vertex = Vertex(key)
        self.vertex_list[key] = new_vertex
        return new_vertex
    
    def get_vertex(self, key : Any) -> Vertex:
        """
        Get the vertex with the spicified key. It will return None if the key was not found.

        Parameters
        ----------
        key : Any
            Key to search.

        Returns
        -------
        Vertex
            Vertex with the specified key.

        """
        if key in self.vertex_list:
            return self.vertex_list[key]
        else:
            return None
    
    def __contains__(self, n : Any):
        return n in self.vertex_list
    
    def add_edge(self, ffrom : Any, to : Any, weight : int = 0) -> None:
        """
        Adds an edge between two vertices with given keys with the given weight.
        If the vertices were not already added in the graph, they will be added.

        Parameters
        ----------
        ffrom : Any
            Key of the vertex which the edge starts
        to : Any
            Key of the vertex which the edge ends
        weight : int, optional
            Weight of the edge. The default is 0.

        Returns
        -------
        None

        """
        if ffrom not in self.vertex_list:
            self.add_vertex(ffrom)
        if to not in self.vertex_list:
            self.add_vertex(to)
        self.vertex_list[ffrom].add_neighbor(self.vertex_list[to], weight)
        
    def get_vertex_keys(self):
        return self.vertex_list.keys()
    
    def __iter__(self):
        return iter(self.vertex_list.values())

##########
# We could use pyvis for visualization. Uncomment the code below if you have pyvis installed.
# Install using Anaconda: conda install -c conda-forge pyvis
# Install using pip: pip install pyvis

# class GraphVis:
#     """
#     Make interactive graphs to visualize our class.
#     To use it, simply instantiate this class with the desired graph to visualize as parameter.
#     """
#     def __init__(self, graph : Graph, name : str = 'graph.html', directed = True):
#         self.__network = Network(directed = directed, height = '900px')
#         self.__graph : Graph = graph
        
#         # Vertexes
#         for v in self.__graph:
#             self.__network.add_node(v.key, shape='circle')
        
#         # Edges
#         for v in self.__graph:
#             for c in v.get_connections():
#                 self.__network.add_edge(v.key, c.key, value = v.get_weight(c), title = str(v.get_weight(c)), arrowStrikethrough=False)
        
#         self.__network.show(name)
    