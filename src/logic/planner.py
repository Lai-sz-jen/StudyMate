# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 12:10:57 2026

Contain Planner class.

@author: laisz
"""
from scheduler import Scheduler

class Planner:
    """
    A singleton class that is responsible for creation and evolution of plans
    All attempts to edit a plan should go through Planner.
    
    
    ## Attribute:
        active_schedules: list[str]
            the ID referrences of all the schedules that is active
        
        master_schedule: Schedule
            the aggregation of all the active schedules
            
        rest_days: RestDay
            the dates and weekdays to avoid when scheduling
        
        
    ## Methods:
        create(course_ID: str, start_date: datetime, due_date: datetime=None,
               *exclude: tuple) -> str
            create a checklist and a schedule for finishing the course and 
            return the ID of the plan
        
        day_off(day: date, **weekly: bool=False) -> None
            preventing any more new agenda on a day/weekday.
            does not affect existing schedules.
            
        work_on(day: date) -> None
            make the day available for scheduling if it is not available already
            
        due(plan_ID, day: date, **force: bool=False) -> None
            set/update a due day for the schedule.
            will raise an error if attempting to shorten the schedule without
            forcing it.
        
        get_agenda(day: date) -> list[str]
            get agenda of the day
        
        cross(task_ID, duration: timedelta) -> None
            mark a task as finished and record the time it actually took
        
        move(task_ID: str, day: date) -> None
            move the task to the day specified
            
        remove(task_ID: str) -> Task
            remove a task from the active plan. The task will be marked as
            abandoned
        
        check_status(course_ID: str) -> bool
            check whether the course delay exceed the threshold
        
        delay(day: date) -> None
            move all the unfinished tasks on the day to the next day
        
        extend(days: int) -> None
            extend the due_date by days (days > 0). will trigger an error if 
            due_date is not set
        
        abandon(plan_ID: str) -> None
            abandaon the plan specified. The abandoned plan will no longer
            be tracked.
            
    """

