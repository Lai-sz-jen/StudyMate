# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 09:40:18 2026

Contain Scheduler class.

@author: laisz
"""

class Scheduler:
    """
    A singleton class that is responsible for creating and editing schedules.
    All attempts to edit schedules should go through Scheduler.
    
    
    ## Attribute:
        active_schedules: list[str]
            the ID referrences of all the schedules that is active
        
        master_schedule: Schedule
            the aggregation of all the active schedules
            
        rest_days: RestDay
            the dates and weekdays to avoid when scheduling
        
        
    ## Methods:
        create(units: Unit, start_date: datetime, due_date: datetime | None
               ) -> Schedule
            create a schedule for finishing the units and 
            return the schedule
        
        day_off(day: date, **weekly: bool=False) -> None
            preventing any more new agenda on a day/weekday.
            does not affect existing schedules.
            
        work_on(day: date) -> None
            make the day available for scheduling if it is not available already
            
        due(schedule: Schedule, day: date, **force: bool=False) -> None
            set/update a due day for the schedule.
            will raise an error if attempting to shorten the schedule without
            forcing it.
        
        get_agenda(day: date) -> list[str]
            get agenda of the day
        
        move(task_ID: str, day: date) -> None
            move the task to the day specified
        
        delay(day: date) -> None
            move all the unfinished tasks on the day to the next day
        
        extend(days: int) -> None
            extend the due_date by days (days > 0). will trigger an error if 
            due_date is not set
        
        abandon(plan_ID: str) -> None
            abandaon the schedule of the plan specified. The abandoned schedule
            will no longer be tracked.
            
    """
    

