import click
import os
import time
import logging
import socket
import threading
from array import array
from re import ASCII 
from tabulate import tabulate
from model import *
from database import *
import dotenv

@click.group()
def cli():
    """Cli Group"""
    pass

################ CLI Commands ################

# A cli_tools command that adds a todo to the database.
@cli.command(name='add',help="Adds a todo to the database.")
@click.option('--task', '-d', prompt='normal, ransom1, ransom2 or ransom3:', type=click.Choice(['normal','ransom1', 'ransom2', 'ransom3']))
@click.option('--category', '-c',prompt='testing or training:', type=click.Choice(['training','testing']))
@click.option('--time', '-t', type=int, prompt='time in seconds:', default=3600, help="Time in seconds.")
@click.option('--monitors', '-m', prompt='monitors (i.e m1,m2,m3):', help="Comma separated list of monitors.")
@click.option('--server', '-s', prompt='Server path (i.e root@194.233.160.46:/root/data):', help="Server path.")
@click.option('--mltype', '-c',prompt='anomaly or classification:', type=click.Choice(['anomaly','classification']))
def add_todo(task, category ,time, monitors,server, mltype):
    """Adds a todo to the database."""
    # First check:
    if category == 'training' and mltype == 'anomaly':
        if task in ['ransom1', 'ransom2', 'ransom3']:
            click.echo("You can not use the ransomware tasks in the training set for anomaly detection.")
            return

    # Checks if another todo is already running.
    todos = get_all_todos()
    for todo in todos:
        if todo.status == 1:
            click.echo("There is already a todo that is not completed. Please wait for it first to be completed before adding a new one!")
            return
    
    # Checks if the connection to the server works or not:
    if check_server(server) == False:
        click.echo("The server is not reachable. Please check the path.")
        logging.debug("The server is not reachable. Please check the path.")
        return

    # Checks, that time > 0
    if time > 0:
        arr_monitors, active_services = check_monitors(monitors)
        server = create_directories_server(server, arr_monitors, category, task, mltype)
        check_directories_on_device()
        replace_env(server,time)
        click.echo("Starting Monitor Services and running it for {time} seconds".format(time=time))
        logging.info("Starting Monitor Services and running it for {time} seconds".format(time=time))
        todo = Todo(task, category, mltype, monitors, server ,time)
        insert_todo(todo)
        position = get_position(task, time)
        start_monitor(time, position, active_services,server)
        for monitor in arr_monitors:
            send_delete(server,monitor)
        show_table()
        return
    else:
        click.echo("Time must be greater than 0")
        return

@cli.command(name='delete', help="Deletes a todo from the table")
@click.option('--position', '-p',type=int, prompt='Position to delete', help="Position of the todo to delete.")
def delete(position: int):
    click.echo("Deleting Entry at position {position}".format(position=position))
    delete_todo(position-1)
    show_table()

@cli.command(name='show', help='Show Table')
def show():
    """
    Shows all open and completed todos.
    """    
    show_table()

@cli.command(name='status_services', help="See the status of the monitoring systemd services")
def status_services():
    os.system("systemctl status m1.service")
    os.system("systemctl status m2.service")
    os.system("systemctl status m3.service")

@cli.command(name='stop_services', help="Stop all services")
def stop_services():
    os.system("systemctl stop m1.service")
    os.system("systemctl stop m2.service")
    os.system("systemctl stop m3.service")
    os.system("systemctl daemon-reload")



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
    Creates a list of systemd services runnung for the given monitors.
    Shuts down the systemd services, if they are still running.
    """
    try:
        array_monitors = monitors.split(",")
    except:
        click.echo("Please use the correct format for monitors.")
        return
    active_services = []
    click.echo("Stopping Services if they are still running...")
    os.system("systemctl stop m1.service > /dev/null")
    os.system("systemctl stop m2.service > /dev/null")
    os.system("systemctl stop m3.service > /dev/null")
    # Get all active services for new todo:
    for monitor in array_monitors:
        if monitor == "m1":
            active_services.append('m1.service')
        elif monitor == "m2":
            active_services.append('m2.service')
        elif monitor == "m3":
            active_services.append('m3.service')
        else:
            click.echo("You have entered an invalid monitor!")
            return
    return array_monitors,active_services

def create_directories_server(server:str, monitors: array, category: str, task: str, mltype: str):
    """
    Creates the directories on the server.
    """
    # Gets the CPU Serial 
    cpu_serial = getserial()
    server_arr = server.split(':')
    server_path = server_arr[1]
    server_ssh = server_arr[0]
    task = task.replace(" ","_")
    # Get id of devi
    path = "{server_path}/{cpu_serial}/{mltype}/{category}/{task}".format(server_path=server_path, cpu_serial=cpu_serial, mltype=mltype, category=category, task=task)
    for monitor in monitors:
        os.system("ssh {server_ssh} mkdir -p {path}/{monitor}".format(server_ssh=server_ssh, path=path, monitor=monitor))
    new_path = server_ssh + ":" + path
    return new_path


def check_directories_on_device():
    """
    Creates the temporary directories to save the .csv/.log and .txt files if it does not exist
    """
    if os.path.exists("/tmp/monitors"):
        os.system("rm -rf /tmp/monitors")

    os.system("mkdir /tmp/monitors")
    os.system("mkdir /tmp/monitors/m1")
    os.system("mkdir /tmp/monitors/m2")
    os.system("mkdir /tmp/monitors/m3")
       
def start_monitor(seconds: int, position: int, active_services: array, server: str):
    """
    Monitors the todo for the given amount of seconds
    """
    total = 0
    click.echo("Please wait {seconds} seconds to start a new Monitoring Todo".format(seconds=seconds))
    for service in active_services:
        os.system("systemctl start {service} > /dev/null".format(service=service))
    # Wait to let all services properly start up:
    wait_till_counter_starts()
    logging.info("Starting Monitoring")
    start = time.perf_counter()
    with click.progressbar(range(seconds)) as progress:
        for value in progress:
            time.sleep(1)
            if (total % 60 == 0) and (total != 0):
                t1 = threading.Thread(target=thread_work, args=(server,active_services))
                t1.start()
            total += 1
    finish = time.perf_counter()
    actual_running_time = round(finish-start, 2)
    click.echo("Finished montioring for {total} seconds.".format(total=actual_running_time))
    logging.info("Finished montioring for {total} seconds.".format(total=actual_running_time))
    for service in active_services:
        os.system("systemctl stop {service} > /dev/null".format(service=service))
    complete(position)

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
    # Adds all todos to the ASCII table
    table = []
    for task in tasks:
        is_done = "Done" if task.status == 2 else "Not Done"
        table.append([task.position+1, task.task, task.category,task.mltype, task.monitors, str(task.time), is_done, task.date_added,task.date_completed])
    table = tabulate(table, headers=["#", "Task", "Category", "Type", "Monitors", "Seconds", "Done","Added","Completed"], tablefmt="fancy_grid")
    click.echo("Table for the device with the following cpu-id: {cpu_id}".format(cpu_id=getserial()))
    click.echo(table)

def replace_env(server: str ,time: int):
    """
    Changes the environmental variables in m3.env and reloads the systemd service
    """
    # Loads the m3.env file
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    
    # Set new Value:
    os.environ["RSYNCF"] = "{}/m3".format(server)
    os.environ["SECONDS"] = "{}\seconds".format(str(time))
    # Write changes to .env file.
    dotenv.set_key(dotenv_file, "RSYNCF", os.environ["RSYNCF"])
    dotenv.set_key(dotenv_file, "SECONDS", os.environ["SECONDS"])

    # Copy the contents of file .env into /etc/systemd/system/m3.env 
    os.system("cp .env /etc/systemd/system/m3.env")
    os.system("sudo systemctl daemon-reload")

def send_delete(server, directory):
    """
    Sends contents of the directory via rsync to the server and deletes all files in the directory
    """
    # Check if the directory exists
    click.echo("Sending data to server  for monitor {}...".format(directory))
    # Send all files located in the directory to the server
    os.system("rsync -vr /tmp/monitors/{directory}/ {server}/{directory} > /dev/null".format(server=server, directory=directory))
    # os.system("rm -rf /tmp/monitors/{directory}/*".format(directory=directory))
    click.echo("Data sent to server and deleted from local directory")

def send_data(server, services):
    """
    This sends the data from m1 & m2 to the server every 60 seconds, just to make sure it does 
    not get lost, through ransomware or a shutdown of the device.
    """
    monitors = []
    for service in services:
        monitor = service.split(".")[0]
        os.system("rsync -vr /tmp/monitors/{monitor}/ {server}/{monitor} > /dev/null".format(monitor=monitor, server=server))

def check_services(services):
    """
    Checks if the services are still running and restarts them if they are not
    """
    for service in services:
        status = os.system('systemctl is-active --quiet {service}'.format(service=service))
        if status != 0:
            os.system("systemctl restart {service} > /dev/null".format(service=service))
            logging.debug("Restarted service {}".format(service))


def thread_work(server: str, active_services: array):
    """
    This is the thread that runs concurrently to the for loop
    1. It sends the data of monitor m1 & m2 all 60 seconds to the server
    2. It checks all 60 seconds if the services are still running and restarts them if needed
    """
    send_data(server, active_services)
    check_services(active_services)

def wait_till_counter_starts():
    """
    This function waits a certain time till the actual timer countdown starts!
    Checks if in the directories /tmp/monitors/m1 and /tmp/monitors/m2 & /tmp/monitors/m3 any files are present
    """
    while True:
        # Check if there is a file in the directory /tmp/monitors/m1
        list_m1 = os.listdir('/tmp/monitors/m1') 
        number_files_m1 = len(list_m1)
        
        # Check if there is a file in the directory /tmp/monitors/m2
        list_m2 = os.listdir('/tmp/monitors/m2') 
        number_files_m2 = len(list_m2)

        # Check if there is a file in the directory /tmp/monitors/m3
        list_m3 = os.listdir('/tmp/monitors/m3')
        number_files_m3 = len(list_m3)

        if (number_files_m1 > 0) and (number_files_m2) > 0 and (number_files_m3) > 0:
            break
        else:
            time.sleep(1)
    
if __name__ == '__main__':
    # Create log file
    logging.basicConfig(filename='cli.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    cli()


