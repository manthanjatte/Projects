import sqlite3

DB_NAME = "tasks.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT,
            status TEXT CHECK(status IN ('pending', 'completed')) NOT NULL DEFAULT 'pending'
        )
    """)
    conn.commit()
    return conn

def add_task():
    description = input("Enter task description: ").strip()
    deadline = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ").strip()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, deadline, status) VALUES (?, ?, 'pending')", (description, deadline))
    conn.commit()
    conn.close()
    print("Task added successfully!")

def view_tasks(status=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    if status:
        cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    else:
        cursor.execute("SELECT * FROM tasks")
    
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("No tasks found.")
    else:
        print("\nTasks List:")
        for task in tasks:
            print(f"[{task[0]}] {task[1]} | Deadline: {task[2] or 'No deadline'} | Status: {task[3]}")

def update_task():
    task_id = input("Enter task ID to update: ").strip()
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    
    if not task:
        print("Task not found!")
        conn.close()
        return
    
    print(f"Current Task: {task[1]} | Status: {task[3]}")
    
    print("1. Mark as Completed")
    print("2. Change Description")
    choice = input("Choose an option: ").strip()
    
    if choice == "1":
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        print("Task marked as completed!")
    elif choice == "2":
        new_desc = input("Enter new description: ").strip()
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_desc, task_id))
        print("Task description updated!")
    else:
        print("Invalid choice!")
    
    conn.commit()
    conn.close()

def delete_task():
    task_id = input("Enter task ID to delete: ").strip()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    print("Task deleted successfully!")

def main_menu():
    while True:
        print("\nTask Management System")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Exit")

        choice = input("Select an option: ").strip()
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks(status="pending")
        elif choice == "4":
            view_tasks(status="completed")
        elif choice == "5":
            update_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
