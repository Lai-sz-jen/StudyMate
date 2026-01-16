# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 16:49:17 2026

@author: laisz
"""
from common.tree import Tree
import pytest


valid_value = [
    pytest.param("", id = "empty string"),
    pytest.param("txt", id = "some string"),
    pytest.param(0, id = "0"),
    pytest.param(3, id = "positive number"),
    pytest.param(-10, id = "negative number"),
    pytest.param((2, "a"), id = "tuple")
    ]


@pytest.fixture(params=valid_value)
def tree(request):
    return Tree(request.param)


class TestInit:
    def test_default(self):
        tree = Tree()
        assert tree.get() is None
        assert tree.is_empty
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(0)
        
    
    @pytest.mark.parametrize("root_val", valid_value)
    def test_init(self, root_val):
        tree = Tree(root_val)
        assert tree.get() == root_val
        assert not tree.is_empty
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(0)
        
    
    def test_set_none(self):
        with pytest.raises(ValueError, match="^Invalid Value"):
            Tree(None)
  
            
class TestAdd:
    @pytest.mark.parametrize("branch_val", valid_value)
    def test_add_to_empty(self, branch_val):
        tree = Tree()
        tree.add(branch_val)
        assert tree.get() is None
        assert tree.get(0) == branch_val
        assert not tree.is_empty
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
        
        
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val", valid_value)
    def test_add_to_none_empty_root(self, root_val, branch_val):
        tree = Tree(root_val)
        tree.add(branch_val)
        assert tree.get() == root_val
        assert tree.get(0) == branch_val
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
    
    
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val_0", valid_value)
    @pytest.mark.parametrize("branch_val_1", valid_value)
    @pytest.mark.parametrize("branch_val_2", valid_value)
    def test_add_parallel(self, 
                          root_val, 
                          branch_val_0, 
                          branch_val_1,
                          branch_val_2):
        tree = Tree(root_val)
        tree.add(branch_val_0)
        tree.add(branch_val_1)
        tree.add(branch_val_2)
        assert tree.get() == root_val
        assert tree.get(0) == branch_val_0
        assert tree.get(1) == branch_val_1
        assert tree.get(2) == branch_val_2
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(0, 0)
    
    
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val_0", valid_value)
    @pytest.mark.parametrize("branch_val_1", valid_value)
    @pytest.mark.parametrize("branch_val_2", valid_value)
    def test_add_nested(self, 
                        root_val, 
                        branch_val_0, 
                        branch_val_1,
                        branch_val_2):
        tree = Tree(root_val)
        tree.add(branch_val_0)
        tree.add(branch_val_1, 0)
        tree.add(branch_val_2, *(0, 0))
        assert tree.get() == root_val
        assert tree.get(0) == branch_val_0
        assert tree.get(0, 0) == branch_val_1
        assert tree.get(0, 0, 0) == branch_val_2
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
        

    @pytest.mark.parametrize("invalid", [None])
    def test_add_invalid_value(self, 
                               tree, 
                               invalid):
        with pytest.raises(ValueError, match="^Invalid Value"):
            tree.add(invalid)
            
    
    @pytest.mark.parametrize("branch_val", valid_value)
    @pytest.mark.parametrize("path", [
        pytest.param((0, 0), id="too deep"),
        pytest.param((1, ), id="too broad"),
        pytest.param((-1, ), id="negative")
        ])
    def test_add_invalid_path(self, tree, branch_val, path):
        tree.add(branch_val)
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.add(branch_val, *path)
            
            
class TestInsert:
    @pytest.mark.parametrize("branch_val", valid_value)
    def test_insert_to_empty(self, branch_val):
        tree = Tree()
        tree.insert(branch_val, 0)
        assert tree.get() is None
        assert tree.get(0) == branch_val
        assert not tree.is_empty
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
            
    
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val", valid_value)
    def test_insert_to_none_empty(self, root_val, branch_val):
        tree = Tree(root_val)
        tree.insert(branch_val, 0)
        assert tree.get() == root_val
        assert tree.get(0) == branch_val
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
            
    
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val_0", valid_value)
    @pytest.mark.parametrize("branch_val_1", valid_value)
    @pytest.mark.parametrize("branch_val_2", valid_value)
    def test_insert_parallel(self,
                             root_val,
                             branch_val_0,
                             branch_val_1,
                             branch_val_2):
        tree = Tree(root_val)
        tree.insert(branch_val_2, 0)
        tree.insert(branch_val_1, 0)
        tree.insert(branch_val_0, 0)
        assert tree.get() == root_val
        assert tree.get(0) == branch_val_0
        assert tree.get(1) == branch_val_1
        assert tree.get(2) == branch_val_2
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(0, 0)
            
    
    @pytest.mark.parametrize("root_val", valid_value)
    @pytest.mark.parametrize("branch_val_0", valid_value)
    @pytest.mark.parametrize("branch_val_1", valid_value)
    @pytest.mark.parametrize("branch_val_2", valid_value)
    def test_insert_nested(self,
                             root_val,
                             branch_val_0,
                             branch_val_1,
                             branch_val_2):
        tree = Tree(root_val)
        tree.insert(branch_val_0, 0)
        tree.insert(branch_val_1, *(0, 0))
        tree.insert(branch_val_2, *(0, 0, 0))
        assert tree.get() == root_val
        assert tree.get(0) == branch_val_0
        assert tree.get(0, 0) == branch_val_1
        assert tree.get(0, 0, 0) == branch_val_2
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(1)
            
            
    @pytest.mark.parametrize("invalid", [None])
    def test_insert_invalid_value(self, 
                            tree,
                            invalid):
        with pytest.raises(ValueError, match="^Invalid Value"):
            tree.insert(invalid, 0)
            
            
    @pytest.mark.parametrize("branch_val", valid_value)
    @pytest.mark.parametrize("path", [
        pytest.param((0, 0), id="too deep"),
        pytest.param((1, ), id="too broad"),
        pytest.param((-1, ), id="negative")
        ])
    def test_insert_invalid_path(self, tree, branch_val, path):
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.insert(branch_val, *path)
            
            
