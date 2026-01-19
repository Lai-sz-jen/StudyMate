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


@pytest.fixture
def grown():
    tree = Tree()
    tree.add("0")
    tree.add("0.0", 0)
    tree.add("0.0.0", 0, 0)
    tree.add("1")
    tree.add("1.0", 1)
    tree.add("1.1", 1)
    tree.add("1.2", 1)
    tree.add("1.3", 1)
    tree.add("2")
    tree.add("2.0", 2)
    tree.add("2.1", 2)
    tree.add("2.1.0", 2, 1)
    tree.add("2.2", 2)
    return tree


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
    
    
    @pytest.mark.slow
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
    
    
    @pytest.mark.slow
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
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(0)
            
    
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
            
    
    @pytest.mark.slow
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
            
    
    @pytest.mark.slow
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
            
            
class TestRemove:
    def test_remove_leaves(self, grown):
        grown.remove(0, 0, 0)
        assert grown.get(0, 0) == "0.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(0, 0, 0)
        
        grown.remove(1, 0)
        assert grown.get(1, 0) == "1.1"
        assert grown.get(1, 2) == "1.3"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(1, 3)
      
        grown.remove(2, 0)
        assert grown.get(2, 0, 0) == "2.1.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2, 1, 0)
            
    
    def test_remove_root(self):
        tree_0 = Tree()
        tree_1 = Tree("data")
        with pytest.raises(ValueError, match=" root "):
            tree_0.remove()
        with pytest.raises(ValueError, match=" root "):
            tree_1.remove()
            
        tree_0.add("1")
        tree_1.add("1")
        with pytest.raises(ValueError, match=" root "):
            tree_0.remove()
        with pytest.raises(ValueError, match=" root "):
            tree_1.remove()
            
    
    @pytest.mark.parametrize("path", [(0, ), (0, 0), (1, ), (2, 1)])
    def test_remove_stem(self, grown, path):
        with pytest.raises(ValueError, match=" non-leaf "):
            grown.remove(*path)
            
            
    @pytest.mark.parametrize("ghost_path", [
            pytest.param((-1, ), id="negative index"),
            pytest.param((3, ), id="out of range_0"),
            pytest.param((0, 1), id="out of range_1"),
            pytest.param((1, 4), id="out of range_2"),
            pytest.param((2, 0, 0), id="out of depth_0"),
            pytest.param((1, 3, 0), id="out of depth_1")
            ])
    def test_remove_ghost_path(self, grown, ghost_path):
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.remove(*ghost_path)


class TestPrune:
    def test_prune_leaf(self, grown):
        grown.prune(0, 0, 0)
        assert grown.get(0, 0) == "0.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(0, 0, 0)
        
        grown.prune(1, 0)
        assert grown.get(1, 0) == "1.1"
        assert grown.get(1, 2) == "1.3"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(1, 3)
      
        grown.prune(2, 0)
        assert grown.get(2, 0, 0) == "2.1.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2, 1, 0)
    
    
    def test_prune_stem_cannot_be_reach(self, grown):
        grown.prune(0, 0)
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(0, 0)
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(0, 0, 0)
         
            
    def test_prune_stem_shift_the_rest(self, grown):
        grown.prune(1)
        assert grown.get(1) == "2"
        assert grown.get(1, 1, 0) == "2.1.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2)
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2, 0)
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2, 1, 0)
        
    
    def test_prune_root(self):
        tree_0 = Tree()
        tree_1 = Tree("data")
        with pytest.raises(ValueError, match=" root "):
            tree_0.prune()
        with pytest.raises(ValueError, match=" root "):
            tree_1.prune()
    
        tree_0.add("1")
        tree_1.add("1")
        with pytest.raises(ValueError, match=" root "):
            tree_0.prune()
        with pytest.raises(ValueError, match=" root "):
            tree_1.prune()
    
    @pytest.mark.parametrize("ghost_path", [
            pytest.param((-1, ), id="negative index"),
            pytest.param((3, ), id="out of range_0"),
            pytest.param((0, 1), id="out of range_1"),
            pytest.param((1, 4), id="out of range_2"),
            pytest.param((2, 0, 0), id="out of depth_0"),
            pytest.param((1, 3, 0), id="out of depth_1")
            ])
    def test_prune_ghost_path(self, grown, ghost_path):
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.prune(*ghost_path)


class TestReset:
    @pytest.mark.parametrize("value", valid_value)
    def test_set_root(self, tree, value):
        tree.reset(value)
        assert tree.get() == value
    
    
    @pytest.mark.parametrize("tree", valid_value, indirect=True)
    @pytest.mark.parametrize("value", valid_value)
    def test_reset_root(self, tree, value):
        tree.reset(value)
        assert tree.get() == value      


    @pytest.mark.parametrize("value", valid_value)
    @pytest.mark.parametrize("path", [
        (0,),
        (0, 0),
        (0, 0, 0),
        (1,),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3)
        ])
    def test_reset_node(self, grown, value, path):
        prev = grown.get(*path)
        temp = grown.reset(value, *path)
        assert grown.get(*path) == value
        assert prev == temp 
        
    
    
    
    @pytest.mark.parametrize("invalid_value", [None])
    @pytest.mark.parametrize("path", [
        tuple(),
        (0,),
        (1, 3),
        (2, 1, 0)
        ])
    def test_reset_to_invalid_value(self, grown, invalid_value, path):
        prev = grown.get(*path)
        with pytest.raises(ValueError, match="^Invalid Value"):
            grown.reset(invalid_value, *path)
        assert prev == grown.get(*path)
        
    
    @pytest.mark.parametrize("invalid_path", [
        (0,),
        (1, 3),
        (2, 1, 0)
        ])    
    def test_reset_invalid_path(self, tree, invalid_path):
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.reset("data", *invalid_path)
        with pytest.raises(ValueError, match="^Invalid Path"):
            tree.get(*invalid_path)
            

class TestGetLeaves:
    def test_get_leaf_from_empty(self):
        tree = Tree()
        values = []
        for data in tree.get_leaves():
            values.append(data)
        assert len(values) == 0
        
    
    @pytest.mark.parametrize("tree, expected", 
        zip(valid_value, valid_value), indirect=["tree"])
    def test_get_leaf_of_single_node(self, tree, expected):
        values = []
        for data in tree.get_leaves():
            assert data == expected
            values.append(data)
        assert len(values) == 1
        
        
    def test_get_leaevs_from_grown(self, grown):
        count = 0
        grown.reset("ROOT")
        expected = ["0.0.0",
                    "1.0",
                    "1.1",
                    "1.2",
                    "1.3",
                    "2.0",
                    "2.1.0",
                    "2.2"]
        for data in grown.get_leaves():
            assert data == expected[count]
            count += 1
        assert count == len(expected)
        
    def test_get_leaevs_from_grown_empty_root(self, grown):
        count = 0
        expected = ["0.0.0",
                    "1.0",
                    "1.1",
                    "1.2",
                    "1.3",
                    "2.0",
                    "2.1.0",
                    "2.2"]
        for data in grown.get_leaves():
            assert data == expected[count]
            count += 1
        assert count == len(expected)
            
            
class TestCopy:
    def test_copy_empty_tree(self):
        tree = Tree()
        copied = tree.copy()
        assert copied.is_empty
        assert copied.get() is None
        
    
    @pytest.mark.parametrize("tree, expected", 
        zip(valid_value, valid_value), indirect=["tree"])
    def test_copy_single_node(self, tree, expected):
        copied = tree.copy()
        assert copied.get() == expected
        with pytest.raises(ValueError, match="^Invalid Path"):
            copied.get(0)
            
    
    def test_copy_grown_tree_structure(self, grown):
        copied = grown.copy()
        # Verify root is None (same as original)
        assert copied.get() is None
        # Verify structure matches original
        assert copied.get(0) == "0"
        assert copied.get(0, 0) == "0.0"
        assert copied.get(0, 0, 0) == "0.0.0"
        assert copied.get(1) == "1"
        assert copied.get(1, 0) == "1.0"
        assert copied.get(1, 1) == "1.1"
        assert copied.get(1, 2) == "1.2"
        assert copied.get(1, 3) == "1.3"
        assert copied.get(2) == "2"
        assert copied.get(2, 0) == "2.0"
        assert copied.get(2, 1) == "2.1"
        assert copied.get(2, 1, 0) == "2.1.0"
        assert copied.get(2, 2) == "2.2"
        
    
    def test_copy_independence_modify_original(self, grown):
        copied = grown.copy()
        # Modify the original tree
        grown.reset("MODIFIED", 0)
        grown.prune(1, 0)
        grown.add("NEW_NODE", 2)
        
        # Verify copy is unaffected
        assert copied.get(0) == "0"
        assert copied.get(1, 0) == "1.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            copied.get(2, 3)
    
    
    def test_copy_independence_modify_copy(self, grown):
        copied = grown.copy()
        # Modify the copy
        copied.reset("MODIFIED", 0)
        copied.prune(1, 0)
        copied.add("NEW_NODE", 2)
        
        # Verify original is unaffected
        assert grown.get(0) == "0"
        assert grown.get(1, 0) == "1.0"
        with pytest.raises(ValueError, match="^Invalid Path"):
            grown.get(2, 3)
            
            
    def test_copy_leaves_match(self, grown):
        copied = grown.copy()
        original_leaves = list(grown.get_leaves())
        copied_leaves = list(copied.get_leaves())
        assert original_leaves == copied_leaves
        
    
    def test_copy_iteration_match(self, grown):
        grown.reset("ROOT")
        copied = grown.copy()
        original_values = list(grown)
        copied_values = list(copied)
        assert original_values == copied_values


class TestIter:
    def test_iter_empty(self):
        tree = Tree()
        count = 0
        for data in tree:
            count += 1
        assert count == 0
    
    
    @pytest.mark.parametrize("tree, expected", 
                             zip(valid_value, valid_value),
                             indirect=["tree"])
    def test_iter_root_only(self, tree, expected):
        values = []
        for data in tree:
            values.append(data)
        assert len(values) == 1
        assert values[0] == expected
        
        
    def test_iter_order_root_empty(self, grown):
        values = []
        for data in grown:
            values.append(data)
        copy = values.copy()
        values.sort()
        assert values == copy
     
        
    def test_iter_order_root_filled(self, grown):
        grown.reset("")
        values = []
        for data in grown:
            values.append(data)
        copy = values.copy()
        values.sort()
        assert values == copy
     
    
    def test_iter_coverage_root_empty(self, grown):
        count = 0
        for data in grown:
            count += 1
        assert count == 13
     
        
    def test_iter_coverage_root_filled(self, grown):
        grown.reset("")
        count = 0
        for data in grown:
            count += 1
        assert count == 14