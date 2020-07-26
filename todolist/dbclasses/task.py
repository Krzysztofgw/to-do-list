from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())
    # datetime.strptime(self.deadline, "%d %b")

    def __repr__(self):
        return str(self.id) + '. ' + self.task + ". " + self.deadline.strftime("%d %b")


def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def read_table_today(session):
    today = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline == today).all()
    print('Today', today.day, today.strftime('%b'))
    if len(rows) > 0:
        for i in rows:
            print(str(i)[0:str(i).rfind('.') + 1])
    else:
        print('Nothing to do!')
    print()


def read_table_week(session):
    today = datetime.today().date()
    for i in range(0, 7):
        current_day = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == current_day).all()
        print(current_day.strftime("%A %d %b"))
        if len(rows) > 0:
            for j in rows:
                print(str(j)[0:str(j).rfind('.') + 1])
            print()
        else:
            print('Nothing to do!')
            print()


def read_table_all(session):
    print('All tasks:')
    rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
    if len(rows) > 0:
        counter = 1
        for i in rows:
            print(str(counter) + '. ' + i[0] + '.', str(i[1].strftime("%d %b")).lstrip('0'))
            counter += 1
        print()
    else:
        print('Nothing to do!')
        print()


def add_row(session, _task, _deadline):
    new_row = Table(task=_task,
                    deadline=datetime.strptime(_deadline, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')
    print()


def delete_task(session, id_bind):
    session.query(Table).filter(Table.id == id_bind).delete()
    session.commit()
    print("The task has been deleted!")
    pass


def delete_tasks_menu(session):
    rows = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline).all()
    if len(rows) > 0:
        print("Chose the number of the task you want to delete:")
        counter = 1
        id_bind = {}
        for i in rows:
            print(str(counter) + '. ' + str(i[0]) + i[1] + '.', str(i[2].strftime("%d %b")).lstrip('0'))
            id_bind[counter] = i[0]
            counter += 1
        task_to_delete = input()
        if 0 < int(task_to_delete) <= counter:
            delete_task(session, id_bind[int(task_to_delete)])
        else:
            print('Nothing to delete!')
    else:
        print('Nothing to delete!')
        print()



def missed_tasks(session):
    print('Missed tasks:')
    today = datetime.today().date()
    rows = session.query(Table.task, Table.deadline).filter(Table.deadline < today).all()
    if len(rows) > 0:
        counter = 1
        for i in rows:
            print(str(counter) + '. ' + i[0] + '.', str(i[1].strftime("%d %b")).lstrip('0'))
            counter += 1
        print()
    else:
        print('Nothing is missed!')
        print()


Base.metadata.create_all(engine)