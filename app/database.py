from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["med_reconciliation"]

snapshots_collection = db["snapshots"]
conflicts_collection = db["conflicts"]