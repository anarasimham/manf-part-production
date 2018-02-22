import requests
from datetime import datetime
from org.apache.nifi.processor.io import StreamCallback

class DoDruidQuery(StreamCallback):

q = """
{
  "queryType": "topN",
  "dataSource": "partsdashboard-kafka",
  "metric": "count",
  "granularity": "all",

  "dimension": "shortname",
  "threshold": 10,

  "intervals": [
    "PT1H/<<now>>"
  ],
  "aggregations": [
    {
      "type": "longSum",
      "name": "count",
      "fieldName": "count"
    },
    {
      "type": "doubleSum",
      "name": "vibrSum",
      "fieldName": "vibrMeasure"
    },
    {
      "type": "doubleSum",
      "name": "vibrThrsMeasure",
      "fieldName": "vibrThreshold"
    }
  ],
  "postAggregations":[{
    "type": "arithmetic",
    "name": "average_vibr",
    "fn": "/",
    "fields": [
      {"type": "fieldAccess", "fieldName": "vibrSum"},
      {"type": "fieldAccess", "fieldName": "count"}
    ]
  },
  {
     "type": "arithmetic",
     "name": "average_vibr_thrs",
     "fn": "/",
     "fields": [
       {"type": "fieldAccess", "fieldName": "vibrThrsMeasure"},
       {"type": "fieldAccess", "fieldName": "count"}
     ]
   }

]
}
"""

now_dt = datetime.now().isoformat()
q = q.replace('<<now>>', now_dt)

headers = {'Content-Type': 'application/json'}
r = requests.post('http://localhost:8082/druid/v2/?pretty', headers=headers, data=q)
print(r.content)

