import click
import os
import time
import socket
import threading
import requests 
from requests.auth import HTTPBasicAuth
from array import array
from re import ASCII 
from tabulate import tabulate
from model import *
from database import *
import random
import dotenv

@click.group()
def cli():
    """Cli Group"""
    pass

# END VERSION 1.0
################ Send Command ################
# This is for sending the data to the server:
@cli.command(name='send', help='Send the data to the server indicate the correct task number')
@click.option('--localhost', '-c', prompt='Flask application i.e 127.0.0.1:5000', help="Localhost path.")
@click.option('--index', '-t', type=int,prompt='Task index', help="Task index i.e 1:")
def send(localhost,index):
    # Gets all the data from the database at the given index
    todo = get_todo(index-1)
    serial = getserial()

    # Prints the data
    click.echo("Sending following data of device {serial} to server {localhost}...".format(serial=serial, localhost=localhost))
    click.echo("############################################################")
    click.echo("Task: {task}".format(task=todo.task))
    click.echo("Description: {description}".format(description=todo.description))
    click.echo("Server: {server}".format(server=todo.server))
    click.echo("Path: {path}".format(path=todo.path))
    click.echo("Monitors: {monitors}".format(monitors=todo.monitors))
    click.echo("Category: {category}".format(category=todo.category))
    click.echo("ML Type: {mltype}".format(mltype=todo.mltype))
    click.echo("############################################################")

    # Check if the server is up:
    try:
        response = requests.get("http://{localhost}/rest/test".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'))
    except:
        click.echo("Flask Application is not up!")
        return
    # Create a request:
    response = requests.post("http://{localhost}/rest/main".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'), json={"ml_type": todo.mltype, "experiment": todo.description.replace(' ','_'), "monitors": todo.monitors, "behavior": todo.task, "category": todo.category, "path": todo.path, "device": serial})
    
    # Set send:
    sent_todo(index-1)
    click.echo("Data sent to server")
    # Show the table
    show_table()
    return

# For Live Monitoring:
@cli.command(name='live', help='Live Monitoring')
@click.option('--localhost', '-c', prompt='Flask application i.e 127.0.0.1:5000', help="Localhost path.")
@click.option('--server', '-s', prompt='Server path (i.e root@194.233.160.46:/root/data)', help="Server path.")
@click.option('--monitors', '-m', prompt='Which monitors (i.e RES,KERN,SYS)', help="Comma separated list of monitors.")
def live(localhost, server, monitors):
    
    # Set defaults for live monitoring:
    category = "testing"
    seconds = 3600
    task = "live"
    description = "live"
    mltype = "anomaly"
    serial = getserial()
    request_number = 0

    # Check if the server is up:
    if check_server(server) == False:
        click.echo("The server is not reachable. Please check the path.")
        return

    # Check Flask Application is up:
    try:
        response = requests.get("http://{localhost}/rest/test".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'))
    except:
        click.echo("Flask Application is not up!")
        return
    
    # Setting everything up:
    arr_monitors, active_services = check_monitors(monitors)
    server, path_for_request = create_directories_server(description, server, arr_monitors, category, task, mltype)
    check_directories_on_device()
    replace_env(server,seconds)

    # Monitoring LOOP:
    total = 0
    click.echo("Starting a 1 hour long live monitoring session".format(seconds=seconds))
    for service in active_services:
        os.system("systemctl start {service} > /dev/null".format(service=service))
    # Wait to let all services properly start up:
    error = wait_till_counter_starts(active_services=active_services)
    if error:
        click.echo("Error: Could not start all services!")
        return 
    start = time.perf_counter()
    with click.progressbar(range(seconds)) as progress:
        for value in progress:
            time.sleep(1)
            if (total % 10 == 0) and (total != 0):
                t1 = threading.Thread(target=thread_work, args=(server,active_services, total))
                t1.start()
            if (total % 11 == 0) and (total != 0):
                # Sends a Post Request all 15 seconds to evaluate the data:
                requests.post("http://{localhost}/rest/live".format(localhost=localhost), auth=HTTPBasicAuth('admin', 'admin'), json={"monitors": monitors, "path": path_for_request, "device": serial, 'number': request_number})
                request_number += 1
            total += 1
    finish = time.perf_counter()
    actual_running_time = round(finish-start, 2)
    click.echo("Finished montioring for {total} seconds.".format(total=actual_running_time))
    for service in active_services:
        os.system("systemctl stop {service} > /dev/null".format(service=service))
    # Done live monitoring:
    click.echo("Live monitoring finished")
    return 



############### Collect Command ################
@cli.command(name='collect',help="Starts the monitoring process.")
@click.option('--description', '-c', prompt='Please add a short description for this task', help="Deskription for the task.")
@click.option('--task', '-d', prompt='normal, poc, dark or raas', type=click.Choice(['normal','poc', 'dark', 'raas']))
@click.option('--category', '-c',prompt='Which category testing or training', type=click.Choice(['training','testing']))
@click.option('--seconds', '-t', type=int, prompt='time in seconds', default=3600, help="Time in seconds.")
@click.option('--monitors', '-m', prompt='Which monitors (i.e RES,KERN,SYS)', help="Comma separated list of monitors.")
@click.option('--server', '-s', prompt='Server path (i.e root@194.233.160.46:/root/data)', help="Server path.")
@click.option('--mltype', '-c',prompt='Type anomaly or classification', type=click.Choice(['anomaly','classification']))
def add_todo(description, task, category ,seconds, monitors, server, mltype):

    #  Make sure, that anomaly training is not a ransomware:
    if category == 'training' and mltype == 'anomaly':
        if task in ['dark', 'raas', 'poc']:
            click.echo("You can not use the ransomware tasks in the training set for anomaly detection.")
            return
    
    # Check that the description is not empty and has not yet been used:
    if description == "" or description == 'live':
        click.echo("Please add a description.")
        return

 
    # Checks if another todo is already running:
    todos = get_all_todos()
    for todo in todos:
        if todo.status == 1:
            click.echo("There is already a todo that is not completed. Please wait for it first to be completed before adding a new one!")
            return
    
    # Checks if the connection to the server works or not:
    if check_server(server) == False:
        click.echo("The server is not reachable. Please check the path.")
        return

    # Checks, that time > 0
    if seconds > 0:
        arr_monitors, active_services = check_monitors(monitors)
        server, path_for_request = create_directories_server(description, server, arr_monitors, category, task, mltype)
        check_directories_on_device()
        replace_env(server,seconds)
        click.echo("Starting Monitor Services and running it for {seconds} seconds".format(seconds=seconds))
        todo = Todo(description, task, category, mltype, monitors, server, path_for_request, seconds)
        insert_todo(todo)
        position = get_position(task, seconds, description)
        error = start_monitor(seconds, position, active_services,server)
        if error:
            return
        for monitor in arr_monitors:
            send_delete(server,monitor)
        show_table()
        return
    else:
        click.echo("Time must be greater than 0")
        return

############# Show Command ################
@cli.command(name='show', help='Show Table')
def show():
    """
    Shows all open and completed todos.
    """    
    show_table()

################ Helper Functios ################
def check_server(server):
    """
    Tries to create a ssh connection.
    If it doesn't work returns False else returns True.
    """
    # Checks first if an @ is present 
    if '@' not in server:
        return False
    server = server.split(':')[0]
    server_ip = server.split('@')[1]
    port = 22
    # If connection error return False:
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.connect((server_ip, port))
    except Exception as e:
        # not up, log reason from ex if wanted
        return False
    else:
        test_socket.close()
    return True

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

def check_monitors(monitors: str):
    """
    Shuts down the systemd services, if they are still running.
    Creates an array with the systemd services to activate for the 
    monitoring process.
    """
    try:
        array_monitors = monitors.split(",")
    except:
        click.echo("Please use the correct format for monitors.")
        return
    active_services = []
    click.echo("Stopping Services if they are still running...")
    os.system("systemctl stop RES.service > /dev/null")
    os.system("systemctl stop KERN.service > /dev/null")
    os.system("systemctl stop SYS.service > /dev/null")
    # Get all active services for new todo:
    for monitor in array_monitors:
        if monitor == "RES":
            active_services.append('RES.service')
        elif monitor == "KERN":
            active_services.append('KERN.service')
        elif monitor == "SYS":
            active_services.append('SYS.service')
        else:
            click.echo("You have entered an invalid monitor!")
            return
    return array_monitors, active_services

def create_directories_server(description: str, server:str, monitors: array, category: str, task: str, mltype: str):
    """
    Creates the directories on the server.
    """
    # Gets the CPU Serial 
    cpu_serial = getserial()
    server_arr = server.split(':')
    server_path = server_arr[1]
    server_ssh = server_arr[0]
    task = task.replace(" ","_")
    description = description.replace(" ","_")
    if category == "training":
        path = "{server_path}/{cpu_serial}/{mltype}/{category}/{task}".format(server_path=server_path, cpu_serial=cpu_serial, mltype=mltype, category=category, task=task)
    else:
        path = "{server_path}/{cpu_serial}/{mltype}/{category}/{description}/{task}".format(server_path=server_path, cpu_serial=cpu_serial, mltype=mltype, category=category, description=description, task=task)
    for monitor in monitors:
        os.system("ssh {server_ssh} mkdir -p {path}/{monitor}".format(server_ssh=server_ssh, path=path, monitor=monitor))
    new_path = server_ssh + ":" + path
    path_for_request = "{server_path}/{cpu_serial}/{mltype}/{category}".format(server_path=server_path, cpu_serial=cpu_serial, mltype=mltype, category=category)
    return new_path, path_for_request


def check_directories_on_device():
    """
    Creates the temporary directories to save the .csv/.log and .txt files if it does not exist
    """
    if os.path.exists("/tmp/monitors"):
        os.system("rm -rf /tmp/monitors")

    os.system("mkdir /tmp/monitors")
    os.system("mkdir /tmp/monitors/RES")
    os.system("mkdir /tmp/monitors/KERN")
    os.system("mkdir /tmp/monitors/SYS")
       

def start_monitor(seconds: int, position: int, active_services: array, server: str):
    """
    Main monitoring logic.
    """
    total = 0
    click.echo("Please wait {seconds} seconds to start a new Monitoring Todo".format(seconds=seconds))
    for service in active_services:
        os.system("systemctl start {service} > /dev/null".format(service=service))
    # Wait to let all services properly start up:
    error = wait_till_counter_starts(active_services=active_services)
    if error:
        click.echo("Error: Could not start all services!")
        # Delete Todo at the position
        delete_todo(position)
        # Show table
        show_table()
        return error
    start = time.perf_counter()
    with click.progressbar(range(seconds)) as progress:
        for value in progress:
            time.sleep(1)
            if (total % 10 == 0) and (total != 0):
                t1 = threading.Thread(target=thread_work, args=(server,active_services, total))
                t1.start()
            total += 1
    finish = time.perf_counter()
    actual_running_time = round(finish-start, 2)
    click.echo("Finished montioring for {total} seconds.".format(total=actual_running_time))
    for service in active_services:
        os.system("systemctl stop {service} > /dev/null".format(service=service))
    complete(position)
    return error


def complete(position: int):
    """
    Sets the monitoring todo to completed
    """
    complete_todo(position)


def show_table():
    """
    Shows the table with all todos
    """
    tasks = get_all_todos()
    table = []
    for task in tasks:
        sent = "Done" if task.sent == 2 else "Not Done"
        is_done = "Done" if task.status == 2 else "Not Done"
        table.append([task.position+1, task.description, task.task, task.category,task.mltype, task.monitors, str(task.seconds), is_done, sent, task.date_added,task.date_completed])
    table = tabulate(table, headers=["#", "Description", "Task", "Category", "Type", "Monitors", "Seconds", "Done", "Sent", "Added","Completed"], tablefmt="fancy_grid")
    click.echo("Table for the device with the following cpu-id: {cpu_id}".format(cpu_id=getserial()))
    click.echo(table)


def replace_env(server: str ,seconds: int):
    """
    Changes the environmental variables in SYS.env and 
    reloads the systemd service.
    """
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ["RSYNCF"] = "{}/SYS".format(server)
    os.environ["SECONDS"] = "{}\seconds".format(str(seconds))
    dotenv.set_key(dotenv_file, "RSYNCF", os.environ["RSYNCF"])
    dotenv.set_key(dotenv_file, "SECONDS", os.environ["SECONDS"])
    os.system("cp .env /etc/systemd/system/SYS.env")
    os.system("sudo systemctl daemon-reload")


def send_delete(server, directory):
    """
    Sends contents of the directory via rsync to the server and deletes all files in the directory
    """
    click.echo("Sending data to server  for monitor {}...".format(directory))
    os.system("rsync -vr /tmp/monitors/{directory}/ {server}/{directory} > /dev/null".format(server=server, directory=directory))
    click.echo("Data sent to server and deleted from local directory")


def send_data(server, services):
    """
    This sends the data from KERN, SYS and RES to the server every 10 seconds, just to make sure it does 
    not get lost, through ransomware or a shutdown of the device.
    """
    for service in services:
        monitor = service.split(".")[0]
        if monitor != "SYS":
            os.system("rsync -r /tmp/monitors/{monitor}/ {server}/{monitor} > /dev/null".format(monitor=monitor, server=server))


def check_services(services):
    """
    Checks if the services are still running and restarts them if they are not
    """
    for service in services:
        status = os.system('systemctl is-active --quiet {service}'.format(service=service))
        if status != 0:
            os.system("systemctl restart {service} > /dev/null".format(service=service))



def thread_work(server: str, active_services: array, total: int):
    """
    This is the thread that runs concurrently to the for loop
    1. It sends the data of monitor m1 & m2 all 10 seconds to the server
    2. It checks all 10 seconds if the services are still running and restarts them if needed
    """
    # Send data every hour:
    send_data(server, active_services)
    check_services(active_services)


def wait_till_counter_starts(active_services: list):
    """
    Checks if data is available in the /tmp/monitor directory:
    """
    start_time = time.time()
    error = True
    while True:

        list_of_file_numbers = []

        # Check if the files are present in the directories:
        for service in active_services:
            monitor = service.split(".")[0]
            list_of_file_numbers.append(len(os.listdir("/tmp/monitors/{monitor}".format(monitor=monitor))))
      

        if time.time() - start_time > 60:
            click.echo("You have been waiting for 60 seconds, there must be something wrong with your setup!")
            click.echo("Stopping Services if they are still running...")
            os.system("systemctl stop RES.service > /dev/null")
            os.system("systemctl stop KERN.service > /dev/null")
            os.system("systemctl stop SYS.service > /dev/null")
            break

        # Checks if all numbers in the list_of_file_numbers are > 0:
        if all(x > 0 for x in list_of_file_numbers):
            error = False
            break
        else:
            time.sleep(1)
    
    return error



    
if __name__ == '__main__':
    cli()





