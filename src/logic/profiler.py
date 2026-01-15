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
        review(plan_ID) -> None
            generate the weekly report and add it to the plan
            
        sum_up(plan_ID, response: tuple) -> None
            generate the final report base on the previous reports and
            the response of the survey. Also update the user's profile
            accordingly
            
        view(plan_ID) -> list[Report]
            return all the reports of a plan in issuing order

        visualize_progress(plan_ID) -> 
            return the bar chart of time spent each day
        
        visualize_velocity(plan_ID) ->
            return the line chart of the trend of user's velocity through
            out the plan
    """
    
