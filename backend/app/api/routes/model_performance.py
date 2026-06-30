from fastapi import APIRouter, HTTPException

from app.services.model_performance_service import (
    get_model_performance
)

router = APIRouter(
    prefix="/model",
    tags=["Model Performance"]
)


@router.get("/performance")
def model_performance():

    try:
        return get_model_performance()

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )