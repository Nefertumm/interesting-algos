from __future__ import annotations
from typing import Any

#########
# From: Problem Solving with Algorithms and Data Structures using Python
#       By Brad Miller and David Ranum
#       Modified to work with Dijkstra's Algorithm

class PriorityQueue:
    # Constructor
    def __init__(self, descending : bool = True) -> None:
        """PriorityQueue

        Args:
            descending (bool, optional): Maximum value is always removed first, set to False otherwise. Defaults to True.
        """
        self.__internal_list : list[tuple] = [(0, 0)]
        self.__size : int = 0
        self.__descending : bool = descending
        
    @property
    def size(self) -> int:
        return self.__size
    
    def empty(self) -> bool:
        return self.__size == 0
    
    def __str__(self) -> str:
        res = ''
        for idx, item in enumerate(self.__internal_list):
            if idx == 0:
                continue
            res += str(item[0]) + ' ' + str(item[1])
            if idx + 1 <= self.size:
                res += '\n'
        return res
    
    def __iter__(self):
        return iter(self.__internal_list[1:])
    
    def __len__(self):
        return self.size
    
    def __contains__(self, val: Any):
        for par in self.__internal_list:
            if par[1] == val:
                return True
        return False
    
    def percolate_up(self, pos: int) -> None:
        """
        Try to percolate the element to the top of the queue from the given position.

        Parameters
        ----------
        pos : int
            Position of the current node to percolate.

        Returns
        -------
        None
        """
        if pos // 2 == 0:
            return
        
        if self.__descending:
            if self.__internal_list[pos][0] > self.__internal_list[pos // 2][0]:
                aux = self.__internal_list[pos // 2]
                self.__internal_list[pos // 2] = self.__internal_list[pos]
                self.__internal_list[pos] = aux
        else:
            if self.__internal_list[pos][0] < self.__internal_list[pos // 2][0]:
                aux = self.__internal_list[pos // 2]
                self.__internal_list[pos // 2] = self.__internal_list[pos]
                self.__internal_list[pos] = aux
            
        self.percolate_up(pos // 2)
    
    def insert(self, item: Any) -> None:
        """
        Inserts a new element to the priority queue, maintaining the heap order property

        Parameters
        ----------
        item : Any
            Element to insert.

        Returns
        -------
        None
        """
        self.__internal_list.append(item)
        self.__size += 1
        # Percolate the added element if needed.
        self.percolate_up(self.size)
    
    def min_max_child(self, pos: int) -> int:
        """
        Finds the position of the minimum or maximum children.
        
        Parameters
        ----------
        pos : int
            Predecessor position.

        Returns
        -------
        int
            Position of the minimum or maximum children.
        """
        # Right child
        if pos * 2 + 1 > self.__size:
            return pos * 2
        else:
            if self.__descending:
                return pos * 2 if self.__internal_list[pos * 2][0] > self.__internal_list[pos * 2 + 1][0] else pos * 2 + 1
            else:
                return pos * 2 if self.__internal_list[pos * 2][0] < self.__internal_list[pos * 2 + 1][0] else pos * 2 + 1

    def percolate_down(self, pos: int) -> None:
        """
        Percolates down the element of the current position.

        Parameters
        ----------
        pos : int
            Position of the element to percolate.

        Returns
        -------
        None
        """
        if 2 * pos > self.__size:
            return

        # Look for the maximum or minimum child
        min_max_child = self.min_max_child(pos)
        if self.__descending:
            if self.__internal_list[pos][0] < self.__internal_list[min_max_child][0]:
                aux = self.__internal_list[pos]
                self.__internal_list[pos] = self.__internal_list[min_max_child]
                self.__internal_list[min_max_child] = aux
        else:
            if self.__internal_list[pos][0] > self.__internal_list[min_max_child][0]:
                aux = self.__internal_list[pos]
                self.__internal_list[pos] = self.__internal_list[min_max_child]
                self.__internal_list[min_max_child] = aux
        
        self.percolate_down(min_max_child)
        
    def advance(self) -> Any:
        """
        Deletes the first element of the priority queue

        Returns
        -------
        Any
            Deleted element.
        """
        deleted = self.__internal_list[1][1]
        self.__internal_list[1] = self.__internal_list[self.__size]
        self.__size -= 1
        self.__internal_list.pop()
        self.percolate_down(1)
        
        return deleted
    
    def build_heap(self, from_list : list) -> None:
        """
        Builds the heap from a list.
        
        Parameters
        ----------
        from_list : list

        Returns
        -------
        None
        """
        i = len(from_list) // 2
        self.__size = len(from_list)
        self.__internal_list = [(0, 0)] + from_list[:]
        while (i > 0):
            self.percolate_down(i)
            i -= 1
            
    def find_position(self, to_find: Any) -> int:
        pos = None
        i = 1
        while i <= self.size:
            if self.__internal_list[i][1] == to_find:
                pos = i
                break
            i += 1
        
        return pos
            
    def decrease_key(self, value: Any, new_val: int) -> None:
        pos = self.find_position(value)
        if not pos:
            return
        
        old_key = self.__internal_list[pos][0]
        self.__internal_list[pos] = (new_val, self.__internal_list[pos][1])
        
        if self.__descending:
            if old_key < new_val:
                self.percolate_up(pos)
            else:
                self.percolate_down(pos)
        else:
            if old_key < new_val:
                self.percolate_down(pos)
            else:
                self.percolate_up(pos)
    
if __name__ == '__main__':
    prio = PriorityQueue(descending=True)
    build_list = [(3, 1), (5, 2), (5, 3), (6, 4), (7, 5)]
    # for i in range(5):
    #     rand = (random.randint(1,10), 8)
    #     prio.insert(rand)
    prio.build_heap(build_list)
    prio.decrease_key(5, 99)
    print(prio)
    
    deleted_list = []
    for i in range(5):
        deleted = prio.advance()
        deleted_list.append(deleted)
    
    print(f'Was: {deleted_list}')