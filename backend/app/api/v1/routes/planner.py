from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.data.database.models.user import User
from app.schemas.planner import PlannerRequest
from app.services.planner_service import PlannerService

router = APIRouter(
    prefix="/planner",
    tags=["Planner"],
)

planner_service = PlannerService()


@router.post("/")
async def plan_trip(
    request: PlannerRequest,
    current_user: User = Depends(get_current_user),
):
    state, total_time = await planner_service.plan_trip(
        message=request.message,
        user_id=str(current_user.id),
    )

    return {
        "trip": state.trip,
        "results": state.previous_results,
        "planning_time_seconds": total_time,
        "agents_registered": len(planner_service.dispatcher.registry.list_agents()),
        "user_id": str(current_user.id),
    }
