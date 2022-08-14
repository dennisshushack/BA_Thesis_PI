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

## How to use it:
Firstly a baseline (normal state of the machine without other programs running) needs to be established. The baseline is the mean CPU & Memory utilization over a defined period of time (for example 10 Minutes).

To create a baseline, run the following command:
```
python3 utilization.py -m
```
After for example 10 minutes, the user has to manually exit the program (PRESS CTRL+ C). After performing this keyboard interrupt, the script should generate 2 files: ressources.csv and ressources_evaluation.csv. ressources_evaluation.csv is the mean of the CPU and Memory consumption over the choosen interval.

### How to evaluate the Resource Utilization of a Program (i.e. Monitor Controller):
Firstly execute the program, that you want to evaluate. Then perform the same experiment as you did with the baseline.
In the end take the new ressource_evalutation.csv values and subtract them from the baseline ressource_evaluation.csv values. This should provide you with the isolated CPU and Memory utilization values.

## CPU and Memory Consumption Monitoring of pre-processing, training and evaluation (FLASK) 
The CPU and Memory consumption can be measured either on the server or the Raspberry Pi sensor. This Thesis deployed it on the Raspberry Pi. As a hint, the following video may be helpfull in getting Tensorflow working on a Pi: https://www.youtube.com/watch?v=vekblEk6UPc&t=903s.
The Flask application creates during training (classification and anomaly detection) a file called output.csv. The following is a sample output of this file.
```
Name,Start,End,Duration
Preprocess KERN,1660449722.1098392,1660449722.2070506,0.09721136093139648
```
It contains the different timestamps for: pre-processing, training and evaluation of ML/DL algorithms. This file can be helpfull to measure the resource utilization of each of these steps. 
I.e. How much CPU & Memory was used for pre-process the KERN monitoring data.

The following will show you how it works:
1. Deploy the Flask Application on the Sensor (rather difficult, but possible) or the Server/Desktop
2. Create a baseline, as you did before and save the file ressource_evalutation.csv in a different directory 
3. Remove the files ressource_evalutation.csv and ressources.csv
4. Start the Flask Application
5. Start this script `python3 utilization.py -m`
6. Perform a training procedure for either Classification or Anomaly Detection (Monitor Controller Send Command or use the file /middleware/test_request.py to do it manually.
7. Wait till the training procedure stopped and then press CTRL + C
8. Keep only the new ressources.csv file and remove ressource_evalutation.csv
9. Add the baseline ressource_evalutation.csv and the output.csv file of the Flask Application to the same folder and exucute: `python3 utilization.py -e`
10. You should now have a file generated called final.csv, which contains all the information needed

Sample Output of final.csv:
```
task cpu memory
Preprocess KERN	28.16	84.28
Preprocess KERN with baseline	25.19	45.58
```
The row with baseline means the baseline has already been deducted from the new measurement. It is the one you need. So pre-processing RES monitoring data took 25.19 % CPU and 45.58 % Memory.
