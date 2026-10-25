from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .task_service import TaskService


class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TaskFlow Manager")
        self.geometry("1100x650")
        self.minsize(900, 540)
        self.configure(bg="#edf2f7")

        self.service = TaskService()
        self.selected_task_id: int | None = None

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("Header.TLabel", background="#1f2937", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        self.style.configure("Secondary.TButton", font=("Segoe UI", 10))

        self.build_ui()
        self.service.seed_demo_tasks()
        self.refresh_tasks()

    def build_ui(self) -> None:
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 18))

        title_label = ttk.Label(header, text="TaskFlow Manager", font=("Segoe UI", 22, "bold"))
        title_label.pack(anchor="w")

        subtitle = ttk.Label(header, text="Organize work, track deadlines, and stay productive.", font=("Segoe UI", 10))
        subtitle.pack(anchor="w", pady=(4, 0))

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        form_frame = ttk.Frame(content, padding=16, style="Card.TFrame")
        form_frame.pack(side="left", fill="y", padx=(0, 16))

        ttk.Label(form_frame, text="Task details", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 12))

        ttk.Label(form_frame, text="Title").pack(anchor="w")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(form_frame, textvariable=self.title_var, width=38)
        self.title_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Description").pack(anchor="w")
        self.description_text = tk.Text(form_frame, height=7, width=38, wrap="word")
        self.description_text.pack(fill="x", pady=(0, 10))

        status_row = ttk.Frame(form_frame)
        status_row.pack(fill="x", pady=(0, 10))

        ttk.Label(status_row, text="Status").pack(anchor="w")
        self.status_var = tk.StringVar(value="pending")
        self.status_combo = ttk.Combobox(
            status_row,
            textvariable=self.status_var,
            state="readonly",
            values=["pending", "in_progress", "completed"],
            width=16,
        )
        self.status_combo.pack(anchor="w", pady=(4, 0))

        ttk.Label(form_frame, text="Due date").pack(anchor="w")
        self.due_date_var = tk.StringVar()
        self.due_date_entry = ttk.Entry(form_frame, textvariable=self.due_date_var, width=38)
        self.due_date_entry.pack(fill="x", pady=(0, 16))

        buttons = ttk.Frame(form_frame)
        buttons.pack(fill="x")

        ttk.Button(buttons, text="Add task", command=self.add_task).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Update task", command=self.update_task).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Mark done", command=self.mark_done).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Delete", command=self.delete_task).pack(side="left")

        ttk.Button(form_frame, text="Clear form", command=self.clear_form).pack(anchor="w", pady=(12, 0))

        list_frame = ttk.Frame(content)
        list_frame.pack(side="right", fill="both", expand=True)

        toolbar = ttk.Frame(list_frame)
        toolbar.pack(fill="x", pady=(0, 10))

        ttk.Label(toolbar, text="Filter: ").pack(side="left")
        self.filter_var = tk.StringVar(value="all")
        self.filter_combo = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            state="readonly",
            values=["all", "pending", "in_progress", "completed"],
            width=15,
        )
        self.filter_combo.pack(side="left", padx=(5, 0))
        self.filter_combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh_tasks())

        stats = ttk.Frame(list_frame)
        stats.pack(fill="x", pady=(0, 12))

        self.total_var = tk.StringVar(value="0")
        self.pending_var = tk.StringVar(value="0")
        self.completed_var = tk.StringVar(value="0")

        for label_text, variable in (("Total", self.total_var), ("Pending", self.pending_var), ("Completed", self.completed_var)):
            stat_card = ttk.Frame(stats, padding=(12, 10), style="Card.TFrame")
            stat_card.pack(side="left", padx=(0, 12), fill="y")
            ttk.Label(stat_card, text=label_text, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(stat_card, textvariable=variable, font=("Segoe UI", 18, "bold")).pack(anchor="w")

        columns = ("id", "title", "status", "due_date")
        self.task_table = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        self.task_table.heading("id", text="ID")
        self.task_table.heading("title", text="Title")
        self.task_table.heading("status", text="Status")
        self.task_table.heading("due_date", text="Due date")

        self.task_table.column("id", width=60, anchor="center")
        self.task_table.column("title", width=360)
        self.task_table.column("status", width=120, anchor="center")
        self.task_table.column("due_date", width=120, anchor="center")
        self.task_table.bind("<<TreeviewSelect>>", self.on_task_selected)

        y_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_table.yview)
        x_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.task_table.xview)
        self.task_table.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.task_table.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="left", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

    def clear_form(self) -> None:
        self.selected_task_id = None
        self.title_var.set("")
        self.description_text.delete("1.0", "end")
        self.status_var.set("pending")
        self.due_date_var.set("")

    def get_form_data(self) -> tuple[str, str, str, str]:
        title = self.title_var.get().strip()
        description = self.description_text.get("1.0", "end").strip()
        status = self.status_var.get().strip().lower()
        due_date = self.due_date_var.get().strip()
        return title, description, status, due_date

    def add_task(self) -> None:
        title, description, status, due_date = self.get_form_data()
        if not title:
            messagebox.showwarning("Missing title", "Please add a task title before saving.")
            return

        self.service.add_task(title, description, status, due_date)
        self.clear_form()
        self.refresh_tasks()

    def update_task(self) -> None:
        if self.selected_task_id is None:
            messagebox.showinfo("Select a task", "Choose a task from the list before updating.")
            return

        title, description, status, due_date = self.get_form_data()
        if not title:
            messagebox.showwarning("Missing title", "Task title cannot be empty.")
            return

        self.service.update_task(self.selected_task_id, title=title, description=description, status=status, due_date=due_date)
        self.clear_form()
        self.refresh_tasks()

    def mark_done(self) -> None:
        if self.selected_task_id is None:
            messagebox.showinfo("Select a task", "Pick a task from the list before marking it complete.")
            return

        self.service.mark_done(self.selected_task_id)
        self.clear_form()
        self.refresh_tasks()

    def delete_task(self) -> None:
        if self.selected_task_id is None:
            messagebox.showinfo("Select a task", "Pick a task from the list before deleting.")
            return

        confirmed = messagebox.askyesno("Delete task", "Are you sure you want to delete this task?")
        if not confirmed:
            return

        self.service.delete_task(self.selected_task_id)
        self.clear_form()
        self.refresh_tasks()

    def on_task_selected(self, _event) -> None:
        selected = self.task_table.selection()
        if not selected:
            return

        task_id = int(self.task_table.item(selected[0], "values")[0])
        self.selected_task_id = task_id

        task = self.service.get_task(task_id)
        if task is None:
            return

        self.title_var.set(task.title)
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", task.description)
        self.status_var.set(task.status)
        self.due_date_var.set(task.due_date)

    def refresh_tasks(self) -> None:
        status_filter = self.filter_var.get()
        tasks = self.service.list_tasks(status_filter)

        for row in self.task_table.get_children():
            self.task_table.delete(row)

        for task in tasks:
            self.task_table.insert(
                "",
                "end",
                values=(task.id, task.title, task.status, task.due_date or "No date"),
            )

        all_tasks = self.service.list_tasks()
        pending_count = sum(1 for task in all_tasks if task.status == "pending")
        completed_count = sum(1 for task in all_tasks if task.status == "completed")

        self.total_var.set(str(len(all_tasks)))
        self.pending_var.set(str(pending_count))
        self.completed_var.set(str(completed_count))


def run_app() -> None:
    app = TaskManagerApp()
    app.mainloop()
