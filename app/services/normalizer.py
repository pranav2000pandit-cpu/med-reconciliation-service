def normalize_medication(med):
    name = med.name.lower().strip()

    dose = med.dose.lower().replace(" ", "")

    status = med.status.lower() if med.status else "active"

    return {
        "name": name,
        "dose": dose,
        "status": status
    }