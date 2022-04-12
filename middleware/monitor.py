from array import array
import typer
import time 
import os
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, get_position

# Creates a typer CLI-Application:
console = Console()
app = typer.Typer()

######################### CLI Commands executatable by User #########################

@app.command(short_help="Get doucmentation on how to use this app")
def doc():
    typer.echo("This is the documentation for the monitor app:")
    os.system("cat documentation")

@app.command(short_help='Adds a Monitor todo to the list')
def add(task: str, category: str, monitors: str, server: str, time: int):
    todos = get_all_todos()
    for todo in todos:
        if todo.status == 1:
            typer.echo(f"!!! There is already a todo that is not completed.\n"
                          f"Please wait for it first to be completed before adding a new one !!!")
            return
    if category == "test" or category == "training":
        if time > 0:
            active_services = check_monitors(monitors)
            check_directories(server)
            typer.echo(f"Adding {task}, {category} with services {active_services} and server {server} and running time {time}s to Todo")
            typer.echo(f"Starting Monitor Services and running it for {time} seconds")
            todo = Todo(task, category, active_services, server ,time)
            insert_todo(todo)
            position = get_position(task)
            monitor(time, position, active_services)
            send_delete(server)
        else:
            typer.echo("Time must be greater than 0")
            return
    else:
        typer.echo("Category must be either test or training")
        return
 
@app.command(short_help="Deletes a todo from the table")
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_todo(position-1)
    show()

@app.command(short_help="Shows all todos in the table")
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]Monitoring Scripts Todos[/bold magenta]!", ":D")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=10)
    table.add_column("Category", min_width=6, justify="right")    
    table.add_column("Monitors", min_width=6, justify="right")
    table.add_column("Seconds", min_width=5, justify="right")
    table.add_column("Done", min_width=6, justify="right")
    table.add_column("Added", min_width=6, justify="right")
    table.add_column("Completed", min_width=12, justify="right")    

    def get_category_color(category):
        COLORS = {'test': 'red', 'training': 'green'}
        return COLORS[category]

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = 'Done' if task.status == 2 else 'Monitoring'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', task.monitors ,str(task.time), is_done_str, task.date_added, task.date_completed)
    console.print(table)

@app.command(short_help="See the status of the monitoring systemd services")
def services():
    os.system("systemctl status m1.service")
    os.system("systemctl status m2.service")
    os.system("systemctl status m3.service")

######################### Functions #########################

def check_monitors(monitors: str):
    """
    Creates a list of systemd services runnung for the given monitors.
    Shuts down the systemd services, if they are still running.
    """
    try:
        monitors = monitors.split(",")
    except:
        typer.echo("Please use a comma to separate the monitors")
        return
    active_services = []
    typer.echo("Stopping Services if they are still running")
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
            typer.echo("You have entered an invalid monitor!")
            return
    return active_services


def complete(position: int):
    """
    Sets the monitoring todo to completed
    """
    typer.echo(f"complete {position}")
    complete_todo(position)
    show()


def monitor(seconds: int, position: int, active_services: array):
    """
    Monitors the todo for the given amount of seconds
    """
    total = 0
    typer.echo("Please wait {} seconds to start a new Monitoring Todo".format(seconds))
    for service in active_services:
        typer.echo(f"Starting {service}")
        os.system("systemctl start {} > /dev/null".format(service))
    with typer.progressbar(range(seconds)) as progress:
        for value in progress:
            time.sleep(1)
            total += 1
    typer.echo(f"Finished montioring for {total} seconds.")
    for service in active_services:
        typer.echo(f"Stopping {service}")
        os.system("systemctl stop {} > /dev/null".format(service))
    complete(position)


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
            send_delete(server)
        if not os.path.exists("/tmp/monitors/m2"):
            os.system("mkdir /tmp/monitors/m2")
        else:
            send_delete(server) 
  
def send_delete(server: str):
    """
    Checks the directories of m1 and m2 if they are empty. If they are not empty it will rsync the folder to 
    the indicated server and delete the directory 
    """
    typer.echo("Sending data to server please wait...")
    if os.path.exists("/tmp/monitors/m1"):
        if os.listdir("/tmp/monitors/m1") == []:
            typer.echo("m1 output is empty, no files to send!")
        else:
            typer.echo("m1 output is not empty, sending files to server...")
            os.system("rsync -avz /tmp/monitors/m1 {}".format(server))
            os.system("rm -rf /tmp/monitors/m1")
            typer.echo("Files from m1 have been sent to server!")
    else:
        typer.echo("m1 does not exist")
    if os.path.exists("/tmp/monitors/m2"):
        if os.listdir("/tmp/monitors/m2") == []:
            typer.echo("m2 output is empty, no files to send!")
        else:
            typer.echo("m2 output is not empty, sending files to server...")
            os.system("rsync -avz /tmp/monitors/m2 {}".format(server))
            os.system("rm -rf /tmp/monitors/m2")
            typer.echo("Files from m2 have been sent to server!")
    else:
        typer.echo("m2 does not exist")
    
    typer.echo("Files for m3 are sent continously to server")
    show()


if __name__ == "__main__":
    app()

