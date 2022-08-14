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
Firstly a baseline (normal state of the machine without other programs running) needs to be established. The baseline is the mean CPU & Memory utilization over a defined period (for example 10 Minutes).

To create a baseline, run the following command:
```
python3 utilization.py -m
```
After for example 10 minutes the user has to manually exit the program (PRESS CTRL+ C). After performing this keyboard interrupt, the script should generate 2 files: ressources.csv and ressources_evaluation.csv. ressources_evaluation.csv is the mean of the CPU and Memory consumption over the choosen interval.

### How to evaluate the Resource Utilization of a Program (i.e. Monitor Controller):
Firstly execute the program to evaluate. Then perform the same experiment as you did with the baseline.
In the end take the new ressource_evalutation.csv values and subtract them from the baseline ressource_evaluation.csv values. This should provide you with the isolated CPU and Memory utilization values.
