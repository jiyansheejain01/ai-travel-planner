from fastapi import APIRouter

from app.schemas.planner import PlannerRequest
from app.services.planner_service import PlannerService

router = APIRouter(
    prefix="/planner",
    tags=["Planner"],
)

planner_service = PlannerService()


@router.post("/")
async def plan_trip(request: PlannerRequest):
    state, total_time = await planner_service.plan_trip(request.message)

    return {
        "trip": state.trip,
        "results": state.previous_results,
        "planning_time_seconds": total_time,
        "agents_registered": len(planner_service.dispatcher.registry.list_agents()),
    }