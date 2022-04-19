import click
import os
import time
from array import array
from re import ASCII 
from tabulate import tabulate
from model import *
from database import *

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
@click.option('--monitors', '-m', prompt='Monitors (i.e m1,m2,m3): ', help="Comma separated list of monitors.")
@click.option('--server', '-s', prompt='Server path (i.e root@194.233.160.46:/root/data): ', help="Server path.")
def add_todo(task, category ,time, monitors,server):
    """Adds a todo to the database."""
    # Checks if another todo is already running.
    todos = get_all_todos()
    for todo in todos:
        if todo.status == 1:
            click.echo("There is already a todo that is not completed. Please wait for it first to be completed before adding a new one!")
            return
    # Checks, that time > 0
    if time > 0:
        active_services = check_monitors(monitors)
        check_directories(server)
        click.echo("Adding {task}, {category} with services {active_services} and server {server} and running time {time}s to Todo".format(task=task, category=category, active_services=active_services, server=server, time=time))
        click.echo("Starting Monitor Services and running it for {time} seconds".format(time=time))
        todo = Todo(task, category, monitors, server ,time)
        insert_todo(todo)
        position = get_position(task)
        monitor(time, position, active_services)
        # send_delete(server)
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
        monitors = monitors.split(",")
    except:
        click.echo("Please use the correct format for monitors.")
        return
    active_services = []
    click.echo("Stopping Services if they are still running")
    for monitor in monitors:
        if monitor == "m1":
            active_services.append('m1.service')
            os.system("systemctl stop m1.service > /dev/null")
        elif monitor == "m2":
            active_services.append('m2.service')
            os.system("systemctl stop m2.service > /dev/null")
        elif monitor == "m3":
            active_services.append('m3.service')
            os.system("systemctl stop m3.service > /dev/null")
        else:
            click.echo("You have entered an invalid monitor!")
            return
    return active_services



def check_directories(server: str):
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
            # send_delete(server)
            pass
        if not os.path.exists("/tmp/monitors/m2"):
            os.system("mkdir /tmp/monitors/m2")
        else:
            # send_delete(server) 
            pass


def monitor(seconds: int, position: int, active_services: array):
    """
    Monitors the todo for the given amount of seconds
    """
    total = 0
    click.echo("Please wait {seconds} seconds to start a new Monitoring Todo".format(seconds=seconds))
    for service in active_services:
        click.echo("Starting {service}".format(service=service))
        os.system("systemctl start {service} > /dev/null".format(service=service))
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
    show_table()

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



if __name__ == '__main__':
    cli()