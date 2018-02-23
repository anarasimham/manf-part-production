/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper <ZK_QUORUM> --create --topic partsdashboard --replication-factor 1 --partitions 1

/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper <ZK_QUORUM> --create --topic manf_averages_errors --replication-factor 1 --partitions 1

/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper <ZK_QUORUM> --create --topic manf_all_errors --replication-factor 1 --partitions 1
