from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Activity:
    name: str
    cost: float
    duration_hours: float
    category: str
    city: str

@dataclass
class Accommodation:
    name: str
    cost_per_night: float
    rating: str
    address: str

@dataclass
class DayPlan:
    day_number: int
    activities: List[Activity] = field(default_factory=list)
    
    @property
    def total_cost(self) -> float:
        return sum(a.cost for a in self.activities)
    
    @property
    def total_duration(self) -> float:
        return sum(a.duration_hours for a in self.activities)

@dataclass
class Itinerary:
    city: str
    days: List[DayPlan] = field(default_factory=list)
    accommodation: Optional[Accommodation] = None
    num_nights: int = 0
    
    @property
    def total_cost(self) -> float:
        act_cost = sum(day.total_cost for day in self.days)
        acc_cost = (self.accommodation.cost_per_night * self.num_nights) if self.accommodation else 0
        return act_cost + acc_cost
