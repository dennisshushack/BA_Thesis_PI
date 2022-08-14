# CPU and Memory Utilization Script

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
Firstly a baseline needs to be established. This refers to the mean CPU & Memory utilization over a defined period (for example 10 Minutes).
The script would thus be run for 10 minutes:
```
python3 utilization.py -m
```
After the defined period the user has to manually exit the program (PRESS CTRL+ C). After receiving this keyboard interrupt, you should have 2 files: ressources.csv and ressources_evaluation.csv`.
