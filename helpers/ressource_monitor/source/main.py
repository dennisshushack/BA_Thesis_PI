import os 
import sys
import time
import signal
import datetime
import psutil

# Measure CPU usage for the entire system.
def monitor_cpu_usage_system():
    """
    Returns the CPU usage in percent.
    """
    return psutil.cpu_percent(interval=1, percpu=False)

# Measures Memory usage for the entire system every second.
def monitor_memory_usage_system():
    """
    Returns the memory usage of the entire system in MegaBytes.
    System has 1 GB of RAM.
    """
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024

def monitor_cpu_frequency_system():
    """
    Returns the CPU frequency in MHz.
    """
    return psutil.cpu_freq().current

# Measures CPU heat for the entire system every second.
def monitor_cpu_heat_system():
    """
    Returns the CPU heat in °C.
    """
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result

def monitor_disk_usage_system():
    """
    Adds up all read and write bytes for all disks.
    """
    result = 0
    for disk in psutil.disk_io_counters(perdisk=True):
        result += disk.read_bytes + disk.write_bytes
    return result / 1024 / 1024

def monitor_reads_per_second():
    """
    Returns the amount of reads per second.
    """
    return psutil.disk_io_counters(perdisk=False, nowrap=True).read_count

def monitor_read_mb_per_second():
    """
    Returns the amount of read MB per second.
    """
    return psutil.disk_io_counters(perdisk=False, nowrap=True).read_bytes / 1024 / 1024

def monitor_writes_per_second():
    """
    Returns the amount of writes per second.
    """
    return psutil.disk_io_counters(perdisk=False, nowrap=True).write_count

def monitor_write_mb_per_second():
    """
    Returns the amount of write MB per second.
    """
    return psutil.disk_io_counters(perdisk=False, nowrap=True).write_bytes / 1024 / 1024

def monitor_MB_received_per_second():
    """
    Returns the amount of MB received per second.
    """
    return psutil.net_io_counters(pernic=False, nowrap=True).bytes_recv / 1024 / 1024

def monitor_MB_sent_per_second():
    """
    Returns the amount of MB sent per second.
    """
    return psutil.net_io_counters(pernic=False, nowrap=True).bytes_sent / 1024 / 1024

# Measure CPU usage and Memory usage for the entire system for 5 seconds and print the results.
def monitor_system():
    cpu_usage = monitor_cpu_usage_system()
    cpu_frequency = monitor_cpu_frequency_system()
    cpu_heat = monitor_cpu_heat_system()
    memory_usage = monitor_memory_usage_system()
    reads_per_second = monitor_reads_per_second() 
    read_mb_per_second = monitor_read_mb_per_second()
    writes_per_second = monitor_writes_per_second() 
    write_mb_per_second = monitor_write_mb_per_second()
    MB_received_per_second = monitor_MB_received_per_second()
    MB_sent_per_second = monitor_MB_sent_per_second()
    return [cpu_usage, cpu_frequency, cpu_heat, memory_usage, reads_per_second, read_mb_per_second, writes_per_second, write_mb_per_second, MB_received_per_second, MB_sent_per_second]
    

def main():
    if len(sys.argv) > 2:
        time_loop = sys.argv[1]
        directory = sys.argv[2]
        time_now = round(time.time())
        try:
            time_loop = int(time_loop)
            directory = str(directory)
        except ValueError:
            print("The time must be an integer & directory must be a string")
            sys.exit(1)
        # Creates a .csv file with the name 'evaluation.csv' in input directory.
        print("Start monitoring system for " + str(time_loop) + " seconds.")
        print("Save results in " + directory + "/{}_evaluation.csv".format(time_now))
        with open('{}/{}_evaluation.csv'.format(directory,time_now), 'w') as f:
            f.write('timestamp,cpu_usage,cpu_frequency,cpu_heat,memory_usage,reads_per_second,read_mb_per_second,writes_per_second,write_mb_per_second,MB_received_per_second,MB_sent_per_second\n')     
            # Measures the system ressource every second for the given time.
            value_list = [0] * 10
            iteration = 0
            for i in range(time_loop):
                monitor_list = monitor_system()
                # Add the values to the list.
                value_list = [x + y for x, y in zip(value_list, monitor_list)]
                timestamp = round(time.time())
                iteration += 1
                # Write the measured values to the .csv file.
                f.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(timestamp, monitor_list[0], monitor_list[1], monitor_list[2], monitor_list[3], monitor_list[4], monitor_list[5], monitor_list[6], monitor_list[7], monitor_list[8], monitor_list[9]))
        print("Finished Monitoring")
        # Calculate the mean of each column in the .csv file 
        print("Adding the mean of all values to the end")
        with open('{}/{}_evaluation.csv'.format(directory,time_now), 'a') as f:
            # Divide the values by the number of iterations.
            value_list = [x / iteration for x in value_list]
            f.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format("mean", value_list[0], value_list[1], value_list[2], value_list[3], value_list[4], value_list[5], value_list[6], value_list[7], value_list[8], value_list[9]))
        print("Done")
        sys.exit(0)
    else:
        print("Please enter the time in seconds and the directory name.")
        sys.exit(1)
       


# Main function.
if __name__ == "__main__":
    main()