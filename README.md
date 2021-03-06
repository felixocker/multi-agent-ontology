# multi-agent-ontology
Source files for the RA-L/ CASE 2019 paper "A Framework for Automatic Initialization of Multi-Agent Production Systems Using Semantic Web Technologies". The paper is authored by Felix Ocker, Ilya Kovalenko, Kira Barton, Dawn Tilbury, and Birgit Vogel-Heuser.  
The paper is published open access: https://ieeexplore.ieee.org/document/8779665  
__Status__: Archive (code is provided as-is, no updates expected)

## Abstract
*Mass customization and global competition require Cyber-Physical Systems of Systems (CPSoS) to become increasingly flexible. Modern CPSoS have to be able to create a wide and versatile variety of products, which takes centralized approaches to their limits. In addition, they have to produce these products as quickly as possible. Hence, they must be able to react promptly if problems arise, such as the failure of a single machine. Modern agent-based production systems provide the flexibility required to cope with these challenges. While resource agents (RAs) represent the available resources in the system, i.e. machines such as robots, individual customer orders can be represented by so-called product agents (PAs). However, a challenge in the design of agent-based production systems is still the amount of communication and computation which is necessary online. The PAs have to communicate their requests and the RAs their capabilities and capacities. On this basis, PAs must compute the appropriate production equence. We propose to automatically initialize every agent with a Knowledge Base (KB) created a priori using Semantic Web Technologies (SWT). On the one hand, the KBs of RAs describe the RAs’ capabilities in terms of product features and production processes. Every KB of a PA, on the other hand, expresses all possible production sequences based on the customer specification and the CPSoS in question. This allows consistency checks regarding the specification as well as more purposeful communication that focuses on aspects that actually need to be determined at runtime, such as the resources’ current capacities. Hence, the framework presented aims to reduce both the communication and computational load necessary at runtime for agent-based CPSoS.*

## Contents
* Exemplary csv files
* Transformation csv -> ttl
* SPARQL queries and batch file to run queries automatically
* Transformation csv -> json

## Further notes

For the implementation of the simulation see [semiconductor-simulation](https://github.com/ikovalenko92/SemiconductorSimulation).

Python 3.6+ is recommended for running the python scripts.

For executing the SPARQL queries, e.g., [stardog](https://www.stardog.com/) can be used.

# Citation
Please use the following bibtex entry:
```
@article{ocker2019ral,
author={Ocker, Felix and Kovalenko, Ilya and Barton, Kira and Tilbury, Dawn and Vogel-Heuser, Birgit},
title={A Framework for Automatic Initialization of Multi-Agent Production Systems Using Semantic Web Technologies},
journal={Robotics and Automation Letters},
volume={4},
number={4},
pages={4330--4337},
year={2019},
publisher={IEEE}
}
```

## License
GPL v3.0

## Contact
Felix Ocker - [felix.ocker@tum.de](mailto:felix.ocker@tum.de)\
Technical University of Munich - Institute of Automation and Information Systems <https://www.mw.tum.de/en/ais/homepage/>
