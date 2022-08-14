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
The Flask application creates during training (classification and anomaly detection) a file called output.csv. The following is a sample of this file.
```
Name,Start,End,Duration
Preprocess KERN,1660449722.1098392,1660449722.2070506,0.09721136093139648
```
It contains the different timestamps for: pre-processing, training and evaluation of ML/DL algorithms. This file can be used to measure the resource utilization of each of these steps. I.e. How much CPU & Memory was used for Cleaning SYS's call data.

The following will show you how it works:
1. Create a baseline, as you did before and save the file ressource_evalutation.csv in a different directory 
2. Remove the files ressource_evalutation.csv and ressources.csv
3. Start the Flask Application
4. Start this script `python3 utilization.py -m`
5. Perform a training procedure for either Classification or Anomaly Detection (Monitor Controller Send Command or use the file /middleware/test_request.py to do it manually.
6. Wait till the training procedure stopped and then press CTRL + C
7. Keep only the new ressources.csv file and remove ressource_evalutation.csv
8. Add the baseline ressource_evalutation.csv and the output.csv file of the Flask Application to the same folder and exucute: `python3 utilization.py -e`
9. You should now have a file generated called final.csv, which contains all the information needed

Sample Output of final.csv:
```
Preprocess KERN	28.16	84.28
Preprocess KERN with baseline	25.19	45.58
```
