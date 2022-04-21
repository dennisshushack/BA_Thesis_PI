import click
import os
import time
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
@click.option('--task', '-d', prompt='Description of task', help='The task to be done.')
@click.option('--category', '-c',prompt='testing or training:', type=click.Choice(['training','testing']))
@click.option('--time', '-t', type=int, prompt='time in seconds', default=3600, help="Time in seconds.")
@click.option('--monitors', '-m', prompt='Monitors (i.e m1,m2,m3)', help="Comma separated list of monitors.")
@click.option('--server', '-s', prompt='Server path (i.e root@194.233.160.46:/root/data)', help="Server path.")
def add_todo(task, category ,time, monitors,server):
    """Adds a todo to the database."""
    # Checks if another todo is already running.
    click.echo("You would like to run the monitors {} for {} seconds and rsync the data to {} .".format(monitors, time,server))
    todos = get_all_todos()
    for todo in todos:
        if todo.status == 1:
            click.echo("There is already a todo that is not completed. Please wait for it first to be completed before adding a new one!")
            return
    # Checks, that the task is not a duplicate.
    if check_duplicate(task):
        click.echo("The task is already in the database.")
        return
    # Checks, that time > 0
    if time > 0:
        arr_monitors, active_services = check_monitors(monitors)
        server = create_directories_server(server, arr_monitors, category, task)
        check_directories_on_device(server)
        replace_env(server,time)
        click.echo("Adding {task}, {category} with services {active_services} and server {server} and running time {time}s to Todo".format(task=task, category=category, active_services=active_services, server=server, time=time))
        click.echo("Starting Monitor Services and running it for {time} seconds".format(time=time))
        todo = Todo(task, category, monitors, server ,time)
        insert_todo(todo)
        position = get_position(task)
        start_monitor(time, position, active_services)
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

@cli.command(name='services', help="See the status of the monitoring systemd services")
def services():
    os.system("systemctl status m1.service")
    os.system("systemctl status m2.service")
    os.system("systemctl status m3.service")


################ Helper Functios ################

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
    click.echo("Stopping Services if they are still running")
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

def create_directories_server(server:str, monitors: array, category: str, task: str):
    """
    Creates the directories on the server.
    """
    server_arr = server.split(':')
    server_path = server_arr[1]
    server_ssh = server_arr[0]
    task = task.replace(" ","_")
    path = "{server_path}/{category}/{task}".format(server_path=server_path, category=category, task=task)
    for monitor in monitors:
        os.system("ssh {server_ssh} mkdir -p {path}/{monitor}".format(server_ssh=server_ssh, path=path, monitor=monitor))
    new_path = server_ssh + ":" + path
    return new_path

def check_directories_on_device(server: str):
    """
    Creates the temporary directories to save the .csv/.log and .txt files if it does not exist
    """
    if not os.path.exists("/tmp/monitors"):
        os.system("mkdir /tmp/monitors")
        os.system("mkdir /tmp/monitors/m1")
        os.system("mkdir /tmp/monitors/m2")
        os.system("mkdir /tmp/monitors/m3")
    else:
        # Check if directory m1 m2 and m3 exist in /tmp/monitors
        # Sends the data in the folders of m1 and m2 to the server, if they exist for m1 and m2 m3 does it by itself
        if not os.path.exists("/tmp/monitors/m1"):
            os.system("mkdir /tmp/monitors/m1")
        else:
            # If the directory m1 contains one or more files call send_delete
            if len(os.listdir("/tmp/monitors/m1")) > 0:
                send_delete(server,"m1")
        if not os.path.exists("/tmp/monitors/m2"):
            os.system("mkdir /tmp/monitors/m2")
        else:
            # If the directory m2 contains one or more files call send_delete
            if len(os.listdir("/tmp/monitors/m2")) > 0:
                send_delete(server,"m2")
        if not os.path.exists("/tmp/monitors/m3"):
            os.system("mkdir /tmp/monitors/m3")
        else:
            # If the directory m3 contains one or more files call send_delete
            if len(os.listdir("/tmp/monitors/m3")) > 0:
                send_delete(server,"m3")


def start_monitor(seconds: int, position: int, active_services: array):
    """
    Monitors the todo for the given amount of seconds
    """
    total = 0
    click.echo("Please wait {seconds} seconds to start a new Monitoring Todo".format(seconds=seconds))
    for service in active_services:
        click.echo("Starting {service}".format(service=service))
        os.system("systemctl start {service} > /dev/null".format(service=service))
    # Wait 5 seconds to let all services properly start up:
    time.sleep(20)
    with click.progressbar(range(seconds)) as progress:
        for value in progress:
            time.sleep(1)
            total += 1
    click.echo("Finished montioring for {total} seconds.".format(total=total))
    for service in active_services:
        click.echo("Stopping {service}".format(service=service))
        os.system("systemctl stop {service} > /dev/null".format(service=service))
    complete(position)

def complete(position: int):
    """
    Sets the monitoring todo to completed
    """
    click.echo("Completed the task at position {position}".format(position=position))
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
        table.append([task.position+1, task.task, task.category, task.monitors, str(task.time), is_done, task.date_added,task.date_completed])
    table = tabulate(table, headers=["#", "Task", "Category", "Monitors", "Seconds", "Done","Added","Completed"], tablefmt="fancy_grid")
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
    click.echo("ENV replaced!")

def send_delete(server, directory):
    """
    Sends contents of the directory via rsync to the server and deletes all files in the directory
    """
    # Check if the directory exists
    click.echo("Sending data to server  for monitor {}...".format(directory))
    # Send all files located in the directory to the server
    os.system("rsync -vr /tmp/monitors/{directory}/ {server}/{directory}".format(server=server, directory=directory))
    os.system("rm -rf /tmp/monitors/{directory}/*".format(directory=directory))
    click.echo("Data sent to server and deleted from local directory")
    

def check_duplicate(task):
    """
    Checks if the task is already in the todo list.
    """
    tasks = get_all_todos()
    for task in tasks:
        if task.task == task:
            click.echo("Task already in todo list")
            return True
    return False

if __name__ == '__main__':
    cli()