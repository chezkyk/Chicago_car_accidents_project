from database.connect import day_collection

def fetch_total_accidents_from_db(beat):
    total_accidents = day_collection.count_documents({'area': beat})
    return total_accidents