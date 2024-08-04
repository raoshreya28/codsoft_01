import tkinter as tk
from tkinter import messagebox, filedialog
import json

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = []

      
        self.load_tasks()

        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)

        
        self.task_listbox = tk.Listbox(
            self.task_frame,
            selectmode=tk.SINGLE,
            width=50,
            height=10,
            bg="lightblue",
            bd=0,
            fg="black",
            font=("Arial", 12),
            selectbackground="grey",
            activestyle="none"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

       
        self.task_scrollbar = tk.Scrollbar(self.task_frame)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.task_listbox.config(yscrollcommand=self.task_scrollbar.set)
        self.task_scrollbar.config(command=self.task_listbox.yview)

       
        self.task_entry = tk.Entry(root, font=("Arial", 12))
        self.task_entry.pack(pady=10)

        
        self.category_var = tk.StringVar(root)
        self.category_var.set("Select Category")
        self.category_menu = tk.OptionMenu(
            root,
            self.category_var,
            "Work",
            "Personal",
            "Other"
        )
        self.category_menu.pack(pady=5)

        
        self.add_task_button = tk.Button(root, text="Add Task", width=48, command=self.add_task)
        self.add_task_button.pack(pady=5)

        
        self.delete_task_button = tk.Button(root, text="Delete Task", width=48, command=self.delete_task)
        self.delete_task_button.pack(pady=5)

     
        self.complete_task_button = tk.Button(root, text="Mark as Completed", width=48, command=self.complete_task)
        self.complete_task_button.pack(pady=5)

        self.save_task_button = tk.Button(root, text="Save Tasks", width=48, command=self.save_tasks)
        self.save_task_button.pack(pady=5)

       
        self.update_task_listbox()

    def add_task(self):
        task = self.task_entry.get()
        category = self.category_var.get()
        if task and category != "Select Category":
            self.tasks.append({'task': task, 'completed': False, 'category': category})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.category_var.set("Select Category")
        else:
            messagebox.showwarning("Input Error", "Please enter a task and select a category.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]['completed'] = True
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = f"{task['task']} ({task['category']})"
            if task['completed']:
                task_text += " (Completed)"
            self.task_listbox.insert(tk.END, task_text)

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.tasks, file)
            messagebox.showinfo("Save Successful", "Tasks saved successfully!")

    def load_tasks(self):
        try:
            with open("tasks.json", 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    todo_list_app = ToDoListApp(root)
    root.mainloop()
