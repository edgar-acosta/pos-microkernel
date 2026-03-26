from fastapi import APIRouter
router = APIRouter()
@router.get("/stock")
def get_stock(): return {"items": 500, "status": "Inyectado en Runtime"}