from fastapi import FastAPI
from app.models import MedicationRequest
from app.services.normalizer import normalize_medication
from app.services.conflict_detector import detect_conflicts
from app.database import snapshots_collection, conflicts_collection
from datetime import datetime
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Medication Reconciliation API running"}


@app.post("/patients/{patient_id}/medications")
def ingest_medications(patient_id: str, payload: MedicationRequest):

    print(f"[INFO] Processing patient {patient_id}")

    if not payload.medications:
        return {"error": "No medications provided"}

    if payload.source not in ["clinic_emr", "hospital_discharge", "patient_reported"]:
        return {"error": "Invalid source"}

    normalized_meds = [normalize_medication(m) for m in payload.medications]
    print(f"[INFO] Normalized: {normalized_meds}")

    conflicts = detect_conflicts(normalized_meds)
    print(f"[INFO] Conflicts: {conflicts}")

    snapshot = {
        "patient_id": patient_id,
        "source": payload.source,
        "medications": normalized_meds,
        "timestamp": datetime.utcnow()
    }

    snapshots_collection.insert_one(snapshot)

    for conflict in conflicts:
        conflict_record = {
            "patient_id": patient_id,
            "drug": conflict["drug"],
            "type": conflict["type"],
            "description": conflict["description"],
            "resolved": False,
            "created_at": datetime.utcnow()
        }

        conflicts_collection.insert_one(conflict_record)

    return {
        "message": "Stored successfully",
        "conflicts": conflicts
    }
@app.get("/patients/with-conflicts")
def get_patients_with_conflicts():
    
    pipeline = [
        {"$match": {"resolved": False}},
        {
            "$group": {
                "_id": "$patient_id",
                "conflict_count": {"$sum": 1}
            }
        }
    ]

    results = list(conflicts_collection.aggregate(pipeline))

    response = [
        {
            "patient_id": r["_id"],
            "conflict_count": r["conflict_count"]
        }
        for r in results
    ]

    return response

@app.get("/patients/high-risk")
def high_risk_patients():
    
    pipeline = [
        {"$match": {"resolved": False}},
        {
            "$group": {
                "_id": "$patient_id",
                "conflict_count": {"$sum": 1}
            }
        },
        {"$match": {"conflict_count": {"$gte": 2}}}
    ]

    results = list(conflicts_collection.aggregate(pipeline))

    return [
        {
            "patient_id": r["_id"],
            "conflict_count": r["conflict_count"]
        }
        for r in results
    ]
from bson import ObjectId

@app.patch("/conflicts/{conflict_id}/resolve")
def resolve_conflict(conflict_id: str):

    conflicts_collection.update_one(
        {"_id": ObjectId(conflict_id)},
        {"$set": {"resolved": True}}
    )

    return {"message": "Conflict marked as resolved"}