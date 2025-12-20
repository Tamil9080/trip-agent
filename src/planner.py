import random
from typing import List, Callable, Optional
from .models import Activity, DayPlan, Itinerary, Accommodation
from .data import get_activities_for_city

class TravelPlanner:
    def __init__(self):
        self.max_daily_hours = 10.0  # Reasonable active hours per day

    def plan_trip(self, city: str, days: int, budget: float, preferences: List[str], on_log: Optional[Callable[[str], None]] = None, custom_activities: Optional[List[Activity]] = None, accommodation: Optional[Accommodation] = None) -> Itinerary:
        def log(message: str):
            if on_log:
                on_log(message)
            else:
                print(message)

        log(f"Planning trip to {city} for {days} days with budget ₹{budget}...")
        
        # Handle Accommodation
        itinerary = Itinerary(city=city, num_nights=days) # Assuming nights = days for simplicity
        if accommodation:
            itinerary.accommodation = accommodation
            acc_cost = accommodation.cost_per_night * days
            log(f"Accommodation selected: {accommodation.name} (₹{accommodation.cost_per_night}/night)")
            log(f"Total Accommodation Cost: ₹{acc_cost}")
            
            if acc_cost >= budget:
                log("⚠️ Critical Warning: Accommodation alone exceeds the total budget!")
        
        if custom_activities:
            available_activities = custom_activities
            log(f"Using {len(available_activities)} activities retrieved from AI.")
        else:
            available_activities = get_activities_for_city(city)
            
        if not available_activities:
            raise ValueError(f"No activities found for {city}")

        # Filter by preferences if any are specified
        preferred_activities = []
        if preferences:
            preferred_activities = [a for a in available_activities if a.category in preferences]
        
        # If not enough preferred activities, mix in others
        if len(preferred_activities) < days * 2:
            other_activities = [a for a in available_activities if a not in preferred_activities]
            pool = preferred_activities + other_activities
        else:
            pool = preferred_activities

        # Initial Plan Generation (Activities only)
        self._fill_itinerary_days(itinerary, days, pool)
        
        # Check constraints and Re-plan
        attempts = 0
        max_attempts = 10
        
        while itinerary.total_cost > budget and attempts < max_attempts:
            log(f"Budget exceeded (₹{itinerary.total_cost} > ₹{budget}). Re-planning (Attempt {attempts + 1})...")
            itinerary = self._replan_reduce_cost(itinerary, pool)
            attempts += 1
            
        if itinerary.total_cost > budget:
            log("Warning: Could not meet budget constraints exactly. Returning cheapest viable option.")

        return itinerary

    def _fill_itinerary_days(self, itinerary: Itinerary, num_days: int, activity_pool: List[Activity]):
        # Shuffle pool to get variety
        pool = activity_pool.copy()
        # random.shuffle(pool) # Removed random shuffle to keep AI order relevance if any
        
        used_activities = set()
        
        for i in range(1, num_days + 1):
            day = DayPlan(day_number=i)
            candidates = [a for a in pool if a.name not in used_activities]
            
            for activity in candidates:
                if day.total_duration >= self.max_daily_hours:
                    break
                    
                if day.total_duration + activity.duration_hours <= self.max_daily_hours:
                    day.activities.append(activity)
                    used_activities.add(activity.name)
            
            itinerary.days.append(day)

    def _generate_initial_plan(self, city: str, num_days: int, activity_pool: List[Activity]) -> Itinerary:
        # Deprecated in favor of _fill_itinerary_days which works on existing itinerary object
        itinerary = Itinerary(city=city)
        self._fill_itinerary_days(itinerary, num_days, activity_pool)
        return itinerary

    def _replan_reduce_cost(self, itinerary: Itinerary, pool: List[Activity]) -> Itinerary:
        # Strategy: Remove the most expensive activity or replace it with a cheaper one
        
        # Flatten all activities in the itinerary to find the most expensive one
        all_scheduled_activities = []
        current_activity_names = set()
        for day in itinerary.days:
            for act in day.activities:
                all_scheduled_activities.append((act, day))
                current_activity_names.add(act.name)
        
        if not all_scheduled_activities:
            return itinerary

        # Sort by cost descending
        all_scheduled_activities.sort(key=lambda x: x[0].cost, reverse=True)
        
        most_expensive, day_plan = all_scheduled_activities[0]
        
        # Remove it
        day_plan.activities.remove(most_expensive)
        current_activity_names.remove(most_expensive.name)
        
        # Try to find a cheaper replacement from the pool that fits time AND isn't already used
        cheaper_options = [a for a in pool if a.cost < most_expensive.cost]
        cheaper_options.sort(key=lambda x: x.cost) # Try cheapest first
        
        for option in cheaper_options:
            if option.name not in current_activity_names: # Ensure uniqueness
                if day_plan.total_duration + option.duration_hours <= self.max_daily_hours:
                    day_plan.activities.append(option)
                    current_activity_names.add(option.name)
                    break
        
        return itinerary
