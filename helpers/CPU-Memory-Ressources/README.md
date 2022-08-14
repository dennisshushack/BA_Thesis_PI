# CPU-Memory-Resources Utilization Script

When deployed on the sensor, this script was used to evaluate the CPU and Memory consumption of the Data Analysis Application (Flask) 
and the Monitor Controller. See Chapter Experiments: Performance Metrics Experiment.

## Installation
Deploy the script on the sensor and run the following:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usgage
Firstly a baseline needs to be established. This refers to the mean CPU & Memory utilization over a defined period. 
