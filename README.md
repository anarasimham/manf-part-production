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
1. Keep in mind, you will need to edit some of the below scripts to provide environment-specific server hostnames/ports/credentials
1. Create MySQL table using the script for the manufacturing table in the github.com/anarasimham/data-gen repository
2. Create the NiFi flow. You can find the export XML for this in the `setup_resources` folder of this project. You'll need to add the template to NiFi and then import it. You'll also need to configure NiFi with the appropriate environment details (hostnames, etc.)
3. Setup the Kafka topics. You can find a script for doing this in the `setup_resources` folder
4. Setup the Druid Kafka ingestion services to pull in data from Kafka. There is a script for this in `setup_resources`
5. Start up the custom dashboard. Run `python app/server.py`. You should be able to navigate to `<hostname>:5000` to see a hello world page
6. Start up the data generator. Instructions for this are in the anarasimham/data-gen GitHub repo
7. You should start seeing data come up in the dashboard after 30 seconds with a page refresh if everything is configured correctly

Notes:
- You will need to configure either two Druid MiddleManager nodes or increase the capacity of tasks your MiddleManager can handle (change druid.worker.capacity in Ambari). Default value is 3 but we will need at least 7. I've configured 12.
