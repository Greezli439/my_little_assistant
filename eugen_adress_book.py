from collections import UserDict
from datetime import datetime
from pathlib import Path
import pickle



class AdressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def __str__(self):
        s_return = ''
        for value in self.data.values():
            s_return = s_return + str(value) + ' '
        return s_return

    def iterator(self, n = 3):
        self.n = n
        records_list = []
        counter = 0
        for record in self.data:
            records_list.append(record)
            counter += 1
            if counter == self.n:
                yield records_list
                records_list = []
                counter = 0
        if records_list:
            yield records_list

    def save_in_file(self):
        path = Path()
        with open(f'{path}\\save_data.bin', 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        path = Path()
        with open(f'{path}\\save_data.bin', 'rb') as file:
            self.data = pickle.load(file)
            return self.data
        
    def find_contact(self, name_or_phone):
        count = 0
        for contacts in self.data.values():
            if contacts.name.value.startswith(name_or_phone[0]):
                print(f'{contacts.name.value} - {contacts.phone.value}' + '\n'+ '_' * 25 )
                count += 1
            if contacts.phone.value.startswith(name_or_phone[0]):
                print(f'{contacts.name.value} - {contacts.phone.value}'+ '\n' + '_' * 25)
                count += 1
        if not count:
            return('There are no any coincidence')
        return ''
         
class Record:
    
    def __init__(self, name, phone, birthday = None) -> None:
        self.name = name
        self.phone = phone
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, phones):
        for phone in phones:
            self.add_phone(phone)

    def del_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def days_to_birthday(self):
        self.birth = self.birthday
        today = datetime.now()
        this_day = datetime(today.year, today.month, today.day)
        birthday_next_year = datetime(today.year+1, self.birth.value.month, self.birth.value.day)
        birthday_this_year = datetime(today.year, self.birth.value.month, self.birth.value.day)
        difference = birthday_this_year - this_day
        if difference.days < 0:
            difference = birthday_next_year - this_day
        return f'{difference.days} days'
    
    def show_all(self) -> str:
        return "\n".join([str(v) for v in self.items()])
    
 

class Field:
    
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if len(value) != 12:
            raise ValueError("Phone must contains 12 symbols.")
        if not value.startswith('380'):
            raise ValueError("Phone must starts from '380'.")
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        self._value = value


class BirthDay(Field):

    @Field.value.setter
    def value(self, value):
        try:
            self.birthday = datetime.strptime(value, '%d %m %Y')
        except:
            raise ValueError('format birthday: dd mm yyyy')
        self._value = self.birthday




def input_error(func):
    def inner(*args):
    
        try:
            result  = func(*args)
            return result
        except ValueError:
            print('Enter user name')
        except KeyError:
            print('Unknwn comand! Please try again')
        except IndexError:
            print('Give me name and phone please')   
           
    return inner


@input_error
def hallo(args):
    hi = "How can I help you?"
    return hi

@input_error
def add(args):  
    if args[1].isdigit():
        name = Name(args[0])
        phone = Phone(args[1])
        record = Record(name, phone)
        ab = AdressBook()
        ab.add_record(record) 
        ab.save_in_file()
    else:
        raise IndexError

@input_error
def change(args):
    if args[1].isdigit():
        name = Name(args[0])
        phone = Phone(args[1])
        record = Record(name, phone)
        ab = AdressBook()
        ab.add_record(record) 
        ab.save_in_file()
    else:
        raise IndexError

@input_error
def show_phonee(name):
    ab = AdressBook()
    ab.load_from_file()
    for contact, v in ab.data.items():
        if contact == name[0]:
            return(v.phone.value)
            


@input_error
def show_all(args):
    ab = AdressBook()
    ab.load_from_file()
    for k, v in ab.data.items():
        return(v.name.value, v.phone.value)

@input_error
def good_bye(args):
    return "Good bye!"
    
@input_error
def save_in_file(args):
    ab = AdressBook
    ab.save_in_file()

@input_error
def load_from_file(args):
    ab = AdressBook()
    ab.load_from_file()

@input_error
def find(args):
    ab = AdressBook()
    ab.load_from_file()
    ab.find_contact(args)


COMANDS = {
    'hallo': hallo,
    'add': add,
    'change': change,
    'phone' : show_phonee,
    'show all': show_all,
    'good bye': good_bye,
    "close": good_bye, 
    "exit": good_bye,
    "save": save_in_file,
    "load": load_from_file,
    "find": find
}


def parser_comand(in_put):
    comands = in_put.lower()
    comands  = comands.split(' ')
    if comands[0] == 'good':
        comand = f'{comands[0]} {comands[1]}'
        args = ''
        return comand, args
    elif comands[0] == 'show':
        comand = f'{comands[0]} {comands[1]}'
        args = ''
        return comand, args
    else:
        comand = comands[0]
        args = comands[1:]
        return comand, args


@input_error
def main(*args):
    
    while True:
        comand, args = parser_comand(input('>>>'))
        
        if args:
            handler = (COMANDS[comand])
            if handler(args) != None:
                print(handler(args))                    
        else:
            handler = (COMANDS[comand])
            print(handler(args))        
            if handler(args) == 'Good bye!':
                break


if __name__ == '__main__':
    main()
    