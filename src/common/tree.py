# -*- coding: utf-8 -*-
from __future__ import annotations
"""
Created on Mon Jan 12 18:59:55 2026

@author: laisz
"""
from typing import Iterator
from copy import copy
import weakref


class Node:
    def __init__(self, value: object = None, parent: Node = None):
        self.value = value
        self.__child = []
        self.__parent = parent
    
    @property
    def has_value(self) -> bool:
        return self.value is not None
    
    @property
    def size(self) -> int:
        return len(self.__child)
    
    @property
    def index(self) -> int:
        if self.is_root:
            return -1
    
        index = 0
        for node in self.parent:
            if node is self:
                break
            index += 1
            
        return index
    
    @property
    def is_leaf(self) -> bool:
        return self.size == 0
    
    @property
    def is_root(self) -> bool:
        return self.__parent is None
    
    @property
    def parent(self) -> Node:
        return self.__parent
    
    @parent.setter
    def parent(self, node: Node|None):
        if node is not None:
            self.__parent = weakref.proxy(node)
        else:
            self.__parent = None
    
    def has_child(self, index: int) -> bool:        
        return index >= 0 and index < len(self.__child)
    
    def get_child(self, index: int) -> Node:
        if not self.has_child(index):
            raise IndexError(f"'{index}'")
        return self.__child[index]

    def get_next(self):
        return self.parent.get_child(self.index + 1)
    
    def get_leaves(self) -> Iterator[object]:
        if self.is_leaf:
            yield self.value
            return
        
        for node in self.__child:
            yield from node.get_leaves()
            
        

    def branch(self, value: object, index: int=None) -> None:
        self.attach(Node(value, self), index)
        
    def attach(self, node: Node, index: int = None) -> None:
        if index is None:
            index = len(self.__child)
        node.parent = self
        self.__child.insert(index, node)
    
    def prune(self, index: int) -> object:
        if not self.has_child(index):
            raise IndexError("index out of range")
            
        return self.__child.pop(index)
    
    def __copy__(self) -> Node:
        new_node = Node(self.value, self.__parent)
        for node in self.__child:
            new_node.branch(copy(node))
            
        return new_node
        
    def __iter__(self) -> Iterator[Node]:
        return iter(self.__child)
    
    def __getitem__(self, index: int) -> object:
        return self.get_child(index)
        

if __name__ == "__main__":
    pass
