from collections import UserDict
import pickle
import os



class Field: # батьківський клас у якому прописані __init__, @property, @setter, які наслідують класи Tag, Title, Content
    def __init__(self, value) -> None:
        self.value = value



class Tag(Field): # тег 

    def __init__(self, value):
        super().__init__(value)
        self.notes = []
  
    def add_note(self, note):
        self.notes.append(note.id)



class Title(Field): # заголовок
    pass


class Content(Field): # основний зміст нотатки
    pass


class Note: 
    def __init__(self, title: Title, content: Content):
        self.title = title 
        self.content = content 
        self.id = 0


class NoteBook(UserDict): # контейнер для нотаток
    
    def __init__(self):
        super().__init__()
        self.__max_note_id = self.__get_max_note_id()
        self.tag_list = []
        self.__address_db_file = "note_book_data.dat"
    
    def __get_max_note_id(self):
        if len(self.data) > 0:
            return max([note.id for note in self.data.values()], reverse=True)

        return 0

    def add_note(self, note: Note): # додає нотатку в словник ключем якого є id
        self.__max_note_id += 1
        note.id = self.__max_note_id
        self.data[note.id] = note

    def owerwrite(self, note_id: int, new_note: Note):    
        self.data[note_id] = new_note
   
    def add_tag(self, tag: Tag, note_id: int):
        pass

    def del_tag(self, tag: Tag):
        pass

    def untag_note(Tag, note_id):
        pass

    def clear_tags(note_id):
        pass

    def search_by_id (self, note_id):
        for id, note in self.data.items():
            if id == note_id:
                return note
            else:
                print("Note not found")

    def search_by_title(self, title): # пошук по заголовку
        pass

    def search_by_tag(self, tag): # пошук по гегу
        pass

    def show_all(self): # поврптає усі нотатки
        pass

    def del_note(self, note_id): # видаляє нотатки по id
        self.data.pop(note_id)
        return self.data

    def save_to_file(self): # зберігає у файлі
        with open(self.__address_db_file, "ab") as file:
            if file.writable():
                pickle.dump(self.data, file)
            else:
                print(f"Cannot save to {self.__address_db_file} file!")
                return False
        return True

    def load_from_file(self): # завантажує з файлу
        if not os.path.isfile(self.__address_db_file):
            print("Database file was not found!")
            return False
        
        with open(self.__address_db_file, 'rb') as file:
            if file.readable():
                self.data = pickle.load(file)
            else:
                print(f"Cannot read from {self.__address_db_file} file!")
                return False
        return True