from pydantic import BaseModel, Field
from typing import List, Literal

class ClaimInformation(BaseModel):
    claim_id: str = Field(..., min_length=2, max_length=10)
    name: str = Field(..., min_length=2, max_length=100)
    vehicle: str = Field(..., min_length=2, max_length=100)
    loss_desc: str = Field(..., min_length=10, max_length=500)
    damage_area: List[
        Literal[
            "windshield",
            "front",
            "rear",
            "side",
            "roof",
            "hood",
            "door",
            "bumper",
            "fender",
            "quarter panel",
            "trunk",
            "glass"
        ]
    ] = Field(..., min_items=1)


class ClaimRouting(BaseModel):
    claim_id: str
    queue: Literal["glass", "fast_track", "material_damage", "total_loss"]


class SeverityAssessment(BaseModel):
    severity: Literal["Minor", "Moderate", "Major"]
    est_cost: float = Field(..., gt=0)
