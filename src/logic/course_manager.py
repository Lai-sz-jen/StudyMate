# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 08:54:59 2026

Contain CourseManager class.

@author: laisz
"""

class CourseManager:
    """
    A singleton class that manage courses contents.
    
    
    ## Methods:
        create(name: str, TOC: str) -> str
            create a course using specified parameters and return course ID
        
        units(course_ID: str) -> Unit
            return a copy of the TOC of the course specified
        
        edit_unit(course_ID: str, path: tuple, new_info: UnitInfo) -> None
            rename the unit at the specific path in the specified course
            to the title given
            
        add_unit(course_ID: str, parent_path: tuple, unit_info: UnitInfo) -> None
            add another unit under the parent unit
        
        remove_unit(course_ID: str, path: tuple) -> UnitInfo
            remove all units under the specified path    
        
        get_plan(plan_ID: str) -> Plan
            return the plan object specified within the course specified
        
        get_log(plan_ID) -> str
            return the changes log of the specified plan
        
        delete(course_ID: str) -> None
            delete the course with specified ID
            
        save(course_ID: str=None) -> None
            save the course object with specified ID; 
            save all altered courses if no ID is given
        
        load(file_path: str) -> None
            load the course data from an external db file.
            
        backup(file_path: str) -> None
            create a db file containing all the existing course data at the
            given directory
        """
