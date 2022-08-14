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

## CPU and Memory Consumption Monitoring of the training procedure (FLASK)
The Flask application cretes during training (classification and anomaly detection) a file called output.csv. The following is a sample part of the file:
```
Name,Start,End,Duration
Preprocess KERN,1660449722.1098392,1660449722.2070506,0.09721136093139648
Preprocess RES,1660449722.2072127,1660449722.326735,0.1195223331451416
Cleaning SYS's data,1660449722.3270695,1660449727.8525183,5.525448799133301
Creating the corpus,1660449727.8526247,1660449728.7032807,0.8506560325622559
``
