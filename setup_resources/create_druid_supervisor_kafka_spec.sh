curl -X POST -H 'Content-Type: application/json' -d @../druid/ingestion_specs/manf_data_kafka.json http://<HOSTNAME>:8090/druid/indexer/v1/supervisor

curl -X POST -H 'Content-Type: application/json' -d @../druid/ingestion_specs/averages_superv.json http://<HOSTNAME>:8090/druid/indexer/v1/supervisor

curl -X POST -H 'Content-Type: application/json' -d @../druid/ingestion_specs/errors_supervisor_kafka.json http://<HOSTNAME>:8090/druid/indexer/v1/supervisor
