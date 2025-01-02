import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_PATH = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.tasks = self.load_tasks()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.task_listbox.pack(side=tk.LEFT, padx=10)
        self.load_tasks_into_listbox()

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Marcar como Completada", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def load_tasks(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(FILE_PATH, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_tasks_into_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔️" if task["completed"] else "❌"
            self.task_listbox.insert(tk.END, f"{status} {task['title']}")

    def add_task(self):
        task_title = self.entry.get()
        if not task_title.strip():
            messagebox.showerror("Error", "El título de la tarea no puede estar vacío")
            return
        self.tasks.append({"title": task_title, "completed": False})
        self.save_tasks()
        self.load_tasks_into_listbox()
        self.entry.delete(0, tk.END)

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada")
            return
        index = selected[0]
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.load_tasks_into_listbox()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")
            return
        index = selected[0]
        del self.tasks[index]
        self.save_tasks()
        self.load_tasks_into_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
