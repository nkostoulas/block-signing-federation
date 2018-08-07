### Federation Block Signing Demo

Simple demonstration of the Federation Block Signing protocol in Elements.

This demo uses Kafka as a communication protocol between 3 signing nodes running locally, implementing a 2-of-3 Federation.

This can be easily extended for nodes running in remote locations/containers by changing the configuration accordingly.

#### Instructions

- Build Elements Daemon
- Install Zookeeper and Kafka and start both services
- Install python3 and requirements `pip3 install requirements.txt`

#### Demonstration

The Federation will run with a 60 second block time amd consist of 3 signing nodes by default. Nodes will connect to the kafka server running on `localhost:9092`. To change any configuration options look at: `Federation.py`, `BlockSigning.py`, `nodeX/elements.conf`.

Run the demo: `python3 Federation.py`

The Federation could be moved to remote locations by running each node on separate locations. Localhost addresses will have to be replaced with the new remote host addresses in `elements.conf` and the `KAFKA_SERVER` parameter would have to be set to the remote address of the Kafka server. The federation script will have to be run in each remote host.
