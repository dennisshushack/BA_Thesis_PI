import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
            task text,
            category text,
            monitors array,
            server text,
            time integer,
            date_added integer,
            date_completed integer,
            status integer,
            position integer
            )""")

create_table()

def insert_todo(todo: Todo):
    """
    Inserts a todo into the database. Gives the correct index for the position.
    """
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :monitors, :server, :time, :date_added, :date_completed, :status, :position)',
        {'task': todo.task, 'category': todo.category, 'monitors': todo.monitors, 'server': todo.server , 'time': todo.time, 'date_added': todo.date_added,
         'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position })


def get_all_todos() -> List[Todo]:
    c.execute('select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete_todo(position):
    """
    Deletes a todo from the database.
    Shifts the position of the todos after the deleted todo down by 1.
    """
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]

    with conn:
        # This moves the other entries in the table 1 position down after the deleted entry.
        c.execute("DELETE from todos WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)


def change_position(old_position: int, new_position: int, commit=True):
    """
    Changes the position of all todos if an old todo got deleted.
    """
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()


def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position',
                  {'position': position, 'date_completed': datetime.datetime.now().timestamp()})


# Gets the position of the todo with the given task.
def get_position(task: str) -> int:
    c.execute('select position from todos where task = :task', {'task': task})
    return c.fetchone()[0]