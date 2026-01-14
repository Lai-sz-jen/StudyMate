# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 11:17:48 2026

Contain Profiler class.

@author: laisz
"""

class Profiler:
    """
    A singleton classs that generate reports for courses. 
    Also in charge of user profile, and update it base on reports.
    
    
    ## Attribute
        questionnaire: Questionnaire
            The questions for survey
        profile: Profile
            The profile of user
    
    
    ## Methods
        review(course_ID) -> None
            generate the weekly report and add it to the course
            
        sum_up(course_ID, response: tuple) -> None
            generate the final report base on the previous reports and
            the response of the survey. Also update the user's profile
            accordingly
            
        view(course_ID) -> list[Report]
            return all the reports of a course in issuing order

        visualize_progress(course_ID) -> 
            return the bar chart of time spent each day
        
        visualize_velocity(course_ID) ->
            return the line chart of the trend of user's velocity through
            out the course
    """
    
