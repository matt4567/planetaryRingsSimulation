# Project Title

A simulation of the motion of the ring system of planetary bodies. This project uses the\
 three-body approximation to model the motion of test particles around a host planet and \
 under the motion of a moon giving rise to divisions and gaps inside of planetary ring \
 systems. The system is fully optimised for multi-threaded use to enable full use of your\
 machine.
 

### Prerequisites

To ensure you have all the prerequisites required run the following command

```
pip install requirements.txt
```


## Getting Started

To use the simulator simply clone this repo

```
git clone https://github.com/matt4567/planetaryRingsSimulation.git
```

then run the multithreads.py file as follows:

```
python multithreads
```

You will be met with some instructions allowing you to continue



## Documentation

####Changing number of threads

Inside of multithreads.py there is a variable:

```
no_Threads = 4
```
Change this to match your machines number of processors.

All planetary constants and physical constants can be found in systempicker.py

To adjust a system or create your own systems edit the dictionary 
```
planetLookUp
```

To adjust the physics of the system edit Physics.py





## Authors

* **Matt Moore** - *

