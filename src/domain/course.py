# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 15:28:13 2026

Contain Class Course

@author: laisz
"""

class Course:
    """
    A core Domain Layer entity representing a subject of study.
    
    This class serves as a stateful data container. It provides the essential 
    structures (StudyMaterial, Plan) and internal state-transition logic 
    required by the Logic Layer managers.
    
    
    ## Attributes
        ID: str
            a unique ID used by managers to identify the course
        
        name: str
            the name of the course
        
        units: Unit
            the studying material associate with the course, could be a book,
            a video, etc.
            
        plans: list[str]]
            ID reference of all the plans created based on this course
            
    
    ## Methods
        add_plan(plan: Plan) -> None
            add an existing plan to the course
        
        discard_plan(plan_ID: str) -> None
            delete the plan reference
        
        rename_unit(path: tuple, title: str) -> None
            rename the unit at the specific path to the title given
            
        
    """
