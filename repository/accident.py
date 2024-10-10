from database.connect import day_collection

def fetch_total_accidents_from_db(beat):
    total_accidents = day_collection.count_documents({'area': beat})
    return total_accidents

def accidents_by_area_and_date_from_db(query,collection):
    total_accidents = collection.count_documents(query)
    return total_accidents

def accidents_by_main_reason_from_db(pipeline):
    results = list(day_collection.aggregate(pipeline))
    return results