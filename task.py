from collections import UserDict
from datetime import datetime as dtdt
from datetime import timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found."
        except IndexError:
            return "The name not found in list."
        except Exception as e:
            return f"Exception is {e}"

    return inner

import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            dtdt.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone added."

    def remove_phone(self, phone):
        for i in range(len(self.phones)):
            if i == phone:
                self.phones.pop(i)
        return "Phone deleted."

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
              if phone.value == old_phone:
                    phone.value = new_phone
        return "phone updated."

    def find_phone(self, phone):
        for phone in self.phones:
              if phone.value == phone:
                return phone.value

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]
    
    def get_upcoming_birthdays(self):
        # знаходимо поточну дату
        time_now = dtdt.today().date()

        new_list = []

        # перебираємо список по записах
        for record in self:
            if self[record].birthday:  # перевіряємо, чи існує дата народження
                birthday = dtdt.strptime(str(self[record].birthday), "%d.%m.%Y").date()  # отримуємо дату народження з об'єкта запису
                birthday = birthday.replace(year=time_now.year)  # змінюємо рік на поточний рік
                days = (birthday - time_now).days  # визначаємо кількість днів до народження

                if days <= 7:
                    if birthday.weekday() == 5:  # якщо день народження випадає на суботу
                        birthday += timedelta(days=2)  # переносимо привітання на понеділок
                    elif birthday.weekday() == 6:  # якщо день народження випадає на неділю
                        birthday += timedelta(days=1)  # переносимо привітання на понеділок

                    current_dict = {'name': self[record].name.value, 'congratulation_date': dtdt.strftime(birthday, "%Y.%m.%d")}
                    new_list.append(current_dict)

        return new_list

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book[name] = record
    return "Contact added."

@input_error
def change_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book[name] = record
    return "Contact updated."

@input_error
def show_phone(args, book):
    name = args[0]
    phone = book[name]
    return phone

@input_error
def show_all(book):
    for k, v in book.items():
        print(f"{k}: {v}")

@input_error
def add_birthday(args, book):
    name, birthday = args
    book.find(name).birthday = birthday
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    birt = book.get(name)
    return birt

def birthdays(book):
    return book.get_upcoming_birthdays()
    

def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    add_contact(['Edd', '1234567890'], book)
    add_birthday(['Edd', '28.02.1996'], book)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            show_all(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

    save_data(book)  # Викликати перед виходом з програми

if __name__ == "__main__":
    main()