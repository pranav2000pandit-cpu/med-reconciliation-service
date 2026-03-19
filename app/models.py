from pydantic import BaseModel
from typing import List, Optional


class Medication(BaseModel):
    name: str
    dose: str
    status: Optional[str] = "active"  # active / stopped


class MedicationRequest(BaseModel):
    source: str
    medications: List[Medication]