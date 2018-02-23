# Manufacturing Part Production Demo
Demo for streaming part production data, analysis of thresholds versus tested data, alerting, and dashboarding for end users. Uses the Hortonworks HDF and HDP platforms.

This is meant to simulate a part production line, where produced parts are written as rows into an RDBMS (MySQL in this case). Those rows are then processed by the platform and made available via dashboard, with mechanisms for alerting the appropriate parties when event thresholds are breached.

There are 5 parts:
- MySQL database, into which the datagen.py script writes rows
- NiFi flow that does two things: 
  - Moves the raw data to a Druid datasource
  - Parses the data to check for violations and inserts the records in violation into another datasource
- NiFi flow that queries Druid to determine whether a moving average of recent records falls below a threshold. If it does, insert that into a Druid datasource
- Superset configurable dashboard to visualize different queries
- Custom dashboard that shows part production status as well as recent violations of the moving average

To use:
1. Create MySQL table using the script for the manufacturing table in the github.com/anarasimham/data-gen repository
2. Create the NiFi flow. You can find the export XML for this in the `setup_resources` folder of this project

Notes:
- You will need to configure either two Druid MiddleManager nodes or increase the capacity of tasks your MiddleManager can handle (change druid.worker.capacity in Ambari)
