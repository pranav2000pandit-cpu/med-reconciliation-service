# Medication Reconciliation & Conflict Reporting Service

## 📌 Overview

This project is a backend service designed to ingest medication lists from multiple sources and detect potential conflicts such as dosage mismatches and unsafe drug combinations.

It simulates a real-world healthcare scenario where patient medication data is fragmented across systems (e.g., clinic EMR, hospital discharge summaries, patient-reported data), and reconciliation is required to ensure safety.

---

## 🚀 Features

* Ingest medication lists from multiple sources
* Normalize medication data
* Detect conflicts:

  * Dose mismatch
  * Drug interactions
* Store longitudinal medication snapshots
* Store and track conflict records
* Reporting endpoints for conflict analysis
* Resolve conflicts (mark as resolved)

---

## 🛠 Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** MongoDB
* **Validation:** Pydantic
* **Testing:** Pytest

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd med-reconciliation
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB

Make sure MongoDB is running locally at:

```
mongodb://localhost:27017
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

### 6. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 1. Ingest Medications

```
POST /patients/{patient_id}/medications
```

### 2. Get Patients with Conflicts

```
GET /patients/with-conflicts
```

### 3. Get High Risk Patients

```
GET /patients/high-risk
```

### 4. Resolve Conflict

```
PATCH /conflicts/{conflict_id}/resolve
```

---

## 🧠 System Architecture

```
Input → Normalize → Conflict Detection → Store → Report
```

### Components:

* **FastAPI** → API layer
* **Services Layer** → normalization + conflict detection
* **MongoDB** → persistent storage

---

## 🗂 Data Model

### Snapshots Collection

* patient_id
* source
* medications[]
* timestamp

### Conflicts Collection

* patient_id
* drug
* type
* description
* resolved
* created_at

---

## ⚠️ Conflict Types

1. **Dose Mismatch**

   * Same drug with different doses

2. **Drug Interaction**

   * Blacklisted drug combinations (from rules.json)

---

## 📊 Sample Request

```json
{
  "source": "clinic_emr",
  "medications": [
    {"name": "Aspirin", "dose": "100 mg"},
    {"name": "Ibuprofen", "dose": "200 mg"},
    {"name": "Aspirin", "dose": "75 mg"}
  ]
}
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🌱 Seed Data

```bash
python seed.py
```

This generates synthetic patient data with conflicts.

---

## 🧾 Assumptions

* Drug interaction rules are static (defined in JSON)
* No external drug database is used
* Each ingestion creates a new snapshot

---

## ⚖️ Trade-offs

* Used rule-based system instead of real pharmacological database
* No authentication layer for simplicity
* Simplified normalization logic

---

## 🚧 Limitations

* Limited drug interaction rules
* No real-time updates or streaming
* No UI/dashboard

---

## 🔮 Future Improvements

* Integration with real drug databases (e.g., RxNorm)
* Machine learning-based conflict detection
* Real-time notifications
* Frontend dashboard for clinicians

---
## Final Update
Project completed with all required features.

---

## 👨‍💻 Author

Pranav D Pandit
