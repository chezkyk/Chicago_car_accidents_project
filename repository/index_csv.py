from database.connect import day_collection

day_collection.create_index({ 'AREA': 1 })

executionStats_without_index = (day_collection
      .find({ 'AREA': '225' })
      .hint({ '$natural': 1})
      .explain()['executionStats'])

executionStats = (day_collection
      .find({ 'AREA': '225' })
      .hint({ 'AREA': 1})
      .explain()['executionStats'])

print(executionStats_without_index)
print(executionStats)