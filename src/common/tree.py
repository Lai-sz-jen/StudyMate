# -*- coding: utf-8 -*-
from __future__ import annotations
"""
Created on Mon Jan 12 18:59:55 2026

@author: laisz
"""
from typing import Iterable, Iterator
from copy import deepcopy

__all__ = ["Tree"]

MISSING = object()
    
class Tree(Iterable):
    def __init__(self, root_value: object =MISSING):
        if root_value is None:
            raise ValueError(f"Invalid Value: {root_value}")
        
        self.__root: Node = Node(root_value)
        if root_value is MISSING:
            self.__root = Node(None)
    
    @property
    def is_empty(self) -> bool:
        return (not self.__root.has_child()) and self.__root.value is None
    
    
    def _to_branch(self, path: tuple[int], origin: Node=None) -> Node:
        if origin is None:
            node = self.__root
        else:
            node = origin
        
        location = []
        for index in path:
            try:
                node = node.get_child(index)
            except IndexError:
                raise ValueError(f"Invalid Path: path does not exist {tuple(location)}")
            location.append(index)
            
        return node
    
    
    def _dfs(self, start_node: Node) -> Iterator[Node]:
        yield start_node
        
        for child in start_node:
            yield from self._dfs(child)
            
    
    def add(self, value: object, *parent_path: int) -> tuple[int]:
        if value is None:
            raise ValueError(f"Invalid Value: {value}")
            
        node = self._to_branch(parent_path)
        node.branch(Node(value))
        return (*parent_path, node.size - 1)
        
    
    def insert(self, value: object, *path: int) -> tuple[int]:
        if value is None:
            raise ValueError(f"Invalid Value: {value}")
        if len(path) < 1:
            raise ValueError("Cannot insert value at root")
        
        node = self._to_branch(path[:-1])
        
        try:
            node.branch(Node(value, False), path[-1])
        except IndexError:
            raise ValueError("Invalid Path: skipping leaf nodes")
            
        return path
    
    
    def remove(self, *path: int) -> object:
        if len(path) < 1:
            raise ValueError("Cannot remove the root node")
            
        parent = self._to_branch(path[:-1])
        target = self._to_branch(path[-1:], parent)
        
        if not target.is_leaf:
            raise ValueError("Cannot remove a non-leaf node (use prune instead)")
            
        value = parent.prune(path[-1])
        return value


    def prune(self, *path: int) -> None:
        if len(path) < 1:
            raise ValueError("Cannot remove the root node")
        
        parent = self._to_branch(path[:-1])
        self._to_branch(path[-1:], parent) # path check
        parent.prune(path[-1])

    
    def reset(self, value: object, *path: int) -> object:
        if value is None:
            raise ValueError(f"Invalid Value: {value}")
            
        node = self._to_branch(path)
        temp = node.value
        node.value = value
        return temp
    
    
    def get(self, *path: int) -> object:
        node = self._to_branch(path)
        return deepcopy(node.value)
    
    
    def get_leaves(self) -> Iterator[object]:
        if not self.__root.has_child() and self.__root.value is None:
            return
        
        for node in self._dfs(self.__root):
            if node.is_leaf:
                yield node.value
    
    
    def copy(self) -> Tree:
        new_tree = Tree("")
        new_tree.__root = self.__root.copy()
        return new_tree
    
    
    def __iter__(self) -> Iterator[object]:
        if self.__root.value is not None:
            yield self.__root.value
            
        for child in self.__root:
            for node in self._dfs(child):
                yield node.value
            
    
    def __str__(self) -> str:
        def _build_str(node: Node, prefix: str, is_last: bool):
            if is_last:
                connector = "\u2514\u2500\u2500"            # "└──"
                new_prefix = prefix + " " * 6                        # "      "
            else:
                connector = "\u251C\u2500\u2500"            # "├──"
                new_prefix = prefix + "\u2502" + " " * 4    # "│    "
                
            text = f"{prefix}{connector}{node.value}\n"
            
            for i in range(node.size):
                text += _build_str(node[i], new_prefix, i==node.size - 1)
            
            return text
            
        if self.is_empty:
            return "<Empty Tree>"
        
        return _build_str(self.__root, "", True)

        
        
class Node:
    def __init__(self, value: object = None, is_root: bool = True):
        self.value = value
        self.__child = []
        self.__is_root = is_root
    
    @property
    def is_empty(self) -> bool:
        return self.value is None
    
    @property
    def size(self) -> int:
        return len(self.__child)
    
    @property
    def is_leaf(self) -> bool:
        return self.size == 0
    
    @property
    def is_root(self) -> bool:
        return self.__is_root
    
    def has_child(self, index: int=0) -> bool:        
        if index >= 0 and index < self.size:
            return True
        else:
            return False
    
    def get_child(self, index: int) -> Node:
        if not self.has_child(index):
            raise IndexError("Index out of range")
        
        return self.__child[index]

    
    def branch(self, node: Node, index: int =None) -> int:
        if index is None:
            index = self.size
        elif index > self.size or index < 0:
            raise IndexError("Index out of range")
            
        self.__child.insert(index, node)
        return index
    
    def prune(self, index: int) -> object:
        if not self.has_child(index):
            raise IndexError("index out of range")
            
        return self.__child.pop(index)
    
    def copy(self) -> Node:
        new_node = Node(self.value, self.is_root)
        for node in self.__child:
            new_node.branch(node.copy())
            
        return new_node
        
    def __iter__(self) -> Iterator[Node]:
        return iter(self.__child)
    
    def __getitem__(self, index: int) -> object:
        return self.get_child(index)
        

if __name__ == "__main__":
    tree = Tree()
    tree.add("2b", )
    tree.insert("2c", 1)
    tree.add("2d")
    tree.add("3a", 0)
    tree.insert("2a", 0)
    print(tree)
    for i in tree:
        print(i)
    
    print(list(tree.get_leaves()))
    
    tree2 = tree.copy()
    print(tree2)
