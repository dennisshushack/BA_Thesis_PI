import time 
import psutil
import time
import csv
import os
import pandas as pd
import argparse


# Takes the arguments from the command line
parser = argparse.ArgumentParser()

# -m for measure: and -e for evaluate:
parser.add_argument("-m", "--measure", help="Measure the ressources", action="store_true")
parser.add_argument("-e", "--evaluate", help="Evaluate the ressources", action="store_true")
args = parser.parse_args()

# If the user wants to measure the ressources:
if args.measure:
    with open("ressources.csv", "w") as file:
        file.write("timestamp,cpu_usage,memory_usage\n")
        # Get the current ressources
        while True:
            cpu_usage = psutil.cpu_percent(percpu=False)
            memory_usage = psutil.virtual_memory().percent
            # If a keyboard interrupt is received, break the loop
            try:
                # Write the current ressources to the .csv file
                file.write(str(time.time()) + "," + str(cpu_usage) + "," + str(memory_usage) + "\n")
                # Sleep for 0.01 seconds
                time.sleep(0.01)
            except KeyboardInterrupt:
                break
    time.sleep(5)
    # Evaluation of the ressources
    # Read the .csv file
    data = pd.read_csv("ressources.csv",sep=",")
    # Calculate the mean of the cpu_usage and memory_usage
    cpu_usage_mean = data["cpu_usage"].mean()
    memory_usage_mean = data["memory_usage"].mean()
    # Save this as a .csv file
    with open("ressources_evaluation.csv", "w") as file:
        # Header of the .csv file with the mean of the cpu_usage and memory_usage
        file.write("cpu_usage_mean,memory_usage_mean\n")
        file.write(str(cpu_usage_mean) + "," + str(memory_usage_mean) + "\n")
        # close the file
        file.close()
    print("The mean of the cpu_usage is: " + str(cpu_usage_mean))
    print("The mean of the memory_usage is: " + str(memory_usage_mean))
    

# if the user wants to evaluate the ressources:
if args.evaluate:
    # Check if the documents ressources.csv and output.csv exist
    if os.path.isfile("./ressources.csv") and os.path.isfile("./output.csv") and os.path.isfile("./ressources_evaluation.csv"):
        # Get the ressource , cpu from ressource_evaluation.csv
        res_eval = pd.read_csv("./ressources_evaluation.csv",sep=",")
        cpu_eval = float(res_eval["cpu_usage_mean"].values[0])
        mem_eval = float(res_eval["memory_usage_mean"].values[0])

        data = pd.read_csv("ressources.csv",sep=",")
        data_output = pd.read_csv("output.csv",sep=",")
        # Save the mean of the cpu_usage and memory_usage in the final .csv file
        with open("final.csv", "a") as file:
            # Set header of the .csv file
            file.write("process_name,cpu_usage_mean,memory_usage_mean\n")
            #close the file
            file.close()

        # For every row in the data_output:
        for index, row in data_output.iterrows():
            # Name of the row 
            name = row["Name"]
            begin = float(row["Start"])
            end = float(row["End"])
            # Calculate the mean of the cpu_usage and memory_usage in the given time interval
            try:
                cpu_usage_mean = data[(data["timestamp"] >= begin) & (data["timestamp"] <= end)]["cpu_usage"].mean()
                memory_usage_mean = data[(data["timestamp"] >= begin) & (data["timestamp"] <= end)]["memory_usage"].mean()
                # Subtract the cpu_eval and memory_eval from the cpu_usage_mean and memory_usage_mean
                cpu_usage_mean_with_mean = float(cpu_usage_mean) - cpu_eval
                memory_usage_mean_with_mean = float(memory_usage_mean) - mem_eval
                if cpu_usage_mean_with_mean < 0:
                    cpu_usage_mean_with_mean = 0
                if memory_usage_mean_with_mean < 0:
                    memory_usage_mean_with_mean = 0
            except:
                cpu_usage_mean = 0
                memory_usage_mean = 0
            
            # Round the cpu_usage_mean_with_mean and memory_usage_mean_with_mean to 2 decimals
            cpu_usage_mean_with_mean = round(cpu_usage_mean_with_mean, 2)
            memory_usage_mean_with_mean = round(memory_usage_mean_with_mean, 2)
            cpu_usage_mean = round(cpu_usage_mean, 2)
            memory_usage_mean = round(memory_usage_mean, 2)
            
            # Open final.csv and write the mean of the cpu_usage and memory_usage in the final .csv file
            with open("final.csv", "a") as file:
                file.write(name + " without baseline" + "," + str(cpu_usage_mean) + "," + str(memory_usage_mean) + "\n")
                file.write(name + " with baseline" + "," + str(cpu_usage_mean_with_mean) + "," + str(memory_usage_mean_with_mean) + "\n")
                # Close the file
                file.close()
    else:
        print("The documents ressources.csv and output.csv do not exist")
        exit()


