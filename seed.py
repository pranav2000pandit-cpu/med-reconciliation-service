# seed script for demo data
from app.database import snapshots_collection, conflicts_collection
from datetime import datetime
import random

patients = ["p1", "p2", "p3"]

sources = ["clinic_emr", "hospital_discharge", "patient_reported"]

medications_pool = [
    {"name": "aspirin", "dose": "100mg"},
    {"name": "aspirin", "dose": "75mg"},
    {"name": "ibuprofen", "dose": "200mg"},
    {"name": "paracetamol", "dose": "500mg"},
]


def seed_data():
    snapshots_collection.delete_many({})
    conflicts_collection.delete_many({})

    for patient in patients:
        meds = random.sample(medications_pool, 2)

        snapshot = {
            "patient_id": patient,
            "source": random.choice(sources),
            "medications": meds,
            "created_at": datetime.utcnow()
        }

        snapshots_collection.insert_one(snapshot)

    print("✅ Seed data inserted")


if __name__ == "__main__":
    seed_data()