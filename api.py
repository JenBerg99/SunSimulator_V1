from fastapi import APIRouter, status
from models.SunLightProperties import SunLightProperties
from models.CompleteModel import CompleteModel, CompleteModelSmall
from cache import cache
from services import calculate_sunlight_properties

router = APIRouter()

@router.get("/sunlight-properties", response_model=SunLightProperties)
def get_sunlight_properties():
    return cache.get_sunlight_properties()

@router.put("/sunlight-properties", status_code=status.HTTP_200_OK)
def set_sunlight_properties(sunlight: SunLightProperties):
    cache.set_sunlight_properties(sunlight)
    return {"success": True, "message": "Sunlight properties updated."}

@router.get("/complete-model", response_model=CompleteModel)
def get_complete_model():
    return cache.get_complete_model()

@router.put("/complete-model", status_code=status.HTTP_200_OK)
def set_complete_model(completemodelsmall: CompleteModelSmall):
    result = calculate_sunlight_properties(completemodelsmall)
    return {"success": True, "message": "Complete model updated."}
