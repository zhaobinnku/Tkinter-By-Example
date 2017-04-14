import tkinter as tk
import tkinter.messagebox as msg
import os
import sqlite3

class Todo(tk.Tk):
    def __init__(self, tasks=None):
        ...

        self.title("To-Do App v3")

        ...

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        current_tasks = self.load_tasks()
        for task in current_tasks:
            task_text = task[0]
            self.add_task(None, task_text, True)

        ...

    def add_task(self, evt, task_text=None, from_db=False):
        if not task_text:
            task_text = self.task_create.get(1.0,tk.END).strip()

        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)

            self.set_task_colour(len(self.tasks), new_task)

            new_task.bind("<Button-1>", self.remove_task)
            new_task.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_task)

            if not from_db:
                self.save_task(task_text)

        self.task_create.delete(1.0, tk.END)

    def remove_task(self, evt):
        task = evt.widget
        if msg.askyesno('Really Delete?', 'Delete ' + task.cget('text') + '?'):
            self.tasks.remove(evt.widget)

            delete_task_query = 'DELETE FROM tasks WHERE task=?'
            delete_task_data = (task.cget('text'),)
            self._runQuery(delete_task_query, delete_task_data)

            evt.widget.destroy()

            self.recolour_tasks()

    ...

    def save_task(self, task):
        insert_task_query = 'INSERT INTO tasks VALUES (?)'
        insert_task_data = (task,)
        self._runQuery(insert_task_query, insert_task_data)

    def load_tasks(self):
        load_tasks_query = 'SELECT task FROM tasks'
        my_tasks = self._runQuery(load_tasks_query, receive=True)

        return my_tasks

    @staticmethod
    def _runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def _firstTimeDB():
        create_tables = 'CREATE TABLE tasks (task TEXT)'
        Todo._runQuery(create_tables)

        default_task_query = 'INSERT INTO tasks VALUES (?)'
        default_task_data = ('--- Add Items Here ---',)
        Todo._runQuery(default_task_query, default_task_data)


if __name__ == "__main__":
    if not os.path.isfile('tasks.db'):
        Todo._firstTimeDB()
    todo = Todo()
    todo.mainloop()