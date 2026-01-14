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
            return the TOC of the course specified
        
        rename_unit(course_ID: str, path: tuple, title: str) -> None
            rename the unit at the specific path in the specified course
            to the title given
            
        get_plan(course_ID: str, plan_ID) -> Plan
            return the plan object specified within the course specified
        
        get_log(course_ID: str, plan_ID) -> str
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
