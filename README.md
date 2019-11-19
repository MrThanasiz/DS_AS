

# Music Client / Server Distributed Implementation

This program was created to as part of the Distributed Systems class at University of Derby.
Its a Client - Load Balancer - Client implementation of a very basic form of a music playing app. Allowing the user to make an account, view and play songs found on the server.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

Any **Windows**/**Linux**/**MacOs** machine running **Python 3.7** & Higher.

The program can run on any OS, however testing was mostly done in Windows, so there might be unexplored bugs with other operating systems.


### Usage

1. Download the latest Client, Load Balancer, Server Instance archives (.zip) from the [releases](https://github.com/MrThanasiz/DS_AS/releases) tab.
2. Extract the folders from the zip files.
3. Modify host & port values in DSClient.py & DSLoadBalancer.py as required (by default they're set to run on localhost and port 9999)
4. Make sure Load balancer & Server Instance folders are in the same directory.
5. Run DSServerLB.py on the server machine & DSClient.py on the client machine.


## Built With

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - The programming language used.
* Server & Client were provided by the teacher of the class, and were modified to work with the rest of the code.
* Some code has been reused from the Networks and Security project as well.


## Versioning

For the versions available, check the [Releases tab on the repository](https://github.com/MrThanasiz/DS_AS/releases). 
