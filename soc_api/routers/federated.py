from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/federated", tags=["federated"])


@router.get("/status")
async def get_federated_status():
    return {
        "current_round": 47,
        "global_model_version": "global-v47",
        "last_aggregation": "2025-01-15T08:00:00Z",
        "next_aggregation": "2025-01-15T09:00:00Z",
        "participating_zones": 6,
        "global_auc_roc": 0.974,
        "global_f1": 0.961,
        "privacy_epsilon_consumed": 47.0,
        "privacy_epsilon_budget": 1000.0,
    }
