from .dbclasses.task import read_table_all, read_table_today, missed_tasks, delete_tasks_menu
from .dbclasses.task import read_table_week, Table, create_session, add_row


class ToDo:
    table_obj = None

    def __init__(self):
        self.table_obj = Table()

    def print_menu(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

    def main(self):
        session = create_session()
        while True:
            self.print_menu()
            choice = input()
            if choice == "0":
                print("Shutdown")
                break
            if choice == "1":
                read_table_today(session)
            elif choice == "2":
                read_table_week(session)
            elif choice == "3":
                read_table_all(session)
            elif choice == '4':
                missed_tasks(session)
            elif choice == "5":
                print('Enter task')
                task = input()
                print('Enter deadline')
                deadline = input()
                add_row(session, task, deadline)
            elif choice == '6':
                delete_tasks_menu(session)
            else:
                print('Type the correct value!')


if __name__ == '__main__':
    object_todo = ToDo()
    object_todo.main()



