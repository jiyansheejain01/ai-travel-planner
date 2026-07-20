from pydantic import BaseModel


class ActivityPlan(BaseModel):
    time: str
    name: str
    description: str


class DayPlan(BaseModel):
    day: int
    activities: list[ActivityPlan]


class PlannerResponse(BaseModel):
    trip_name: str
    summary: str
    days: list[DayPlan]