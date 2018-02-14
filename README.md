# manf-part-production
Demo for streaming part production data, analysis of thresholds versus tested data, alerting, and dashboarding for end users

4 parts:
- MySQL database, into which the datagen.py script writes rows
- NiFi flow that moves the data to HDFS/Hive/Druid
- NiFi flow that queries Hive to determine whether a moving average of recent records fall below a threshold
- Custom dashboard that shows violations and part production status
