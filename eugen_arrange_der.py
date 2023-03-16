import os
import shutil
import sys

IMAGE = ('jpeg', 'png', 'jpg', 'svg')
VIDEOS = ('avi', 'mp4', 'mov', 'mkv')
DOCS = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
MUSIC = ('mp3', 'ogg', 'wav', 'amr')
ARCHIVE = ('zip', 'gz', 'tar')
CORRECT_DIRS = ('images', 'documents', 'audio', 'video', 'archive', 'unknown_formats')
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(file_name):
    point_index = file_name.index('.')
    prefix = file_name[:point_index]
    suffix = file_name[point_index:]
    result = ''
    for i in prefix:
        if i in CYRILLIC_SYMBOLS:
            i = i.translate(TRANS)
            result += i
        elif i in NUMBERS:
            result += i
        elif i in TRANSLATION:
            result += i
        else:
            i = '_'
            result += i
    return result + suffix


def delete_dirs(path):
    for element in os.scandir(path):
        if element.name not in CORRECT_DIRS:
            shutil.rmtree(element)


def make_correct_dirs(path):
    os.makedirs(path + '/images')
    os.makedirs(path + '/documents')
    os.makedirs(path + '/audio')
    os.makedirs(path + '/video')
    os.makedirs(path + '/archive')
    os.makedirs(path + '/unknown_formats')


def sort_dir(path):
    for adress, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(DOCS):
                os.rename(os.path.join(adress, file), f'{path}/documents/{normalize(file)}')
                continue
            if file.endswith(IMAGE):
                os.rename(os.path.join(adress, file), f'{path}/images/{normalize(file)}')
                continue
            if file.endswith(MUSIC):
                os.rename(os.path.join(adress, file), f'{path}/audio/{normalize(file)}')
                continue
            if file.endswith(VIDEOS):
                os.rename(os.path.join(adress, file), f'{path}/video/{normalize(file)}')
                continue
            if file.endswith(ARCHIVE):
                shutil.unpack_archive(os.path.join(adress, file), f'{path}/archive')
                continue
            else:
                os.rename(os.path.join(adress, file), f'{path}/unknown_formats/{normalize(file)}')
                continue


def show_result(path):
    for adr, dirs, file in os.walk(path):
        print(f'{adr[len(path) + 1:]}: {file}')


def main():
    path = sys.argv[1]
    make_correct_dirs(path)
    sort_dir(path)
    delete_dirs(path)
    show_result(path)


if __name__ == "__main__":
    main()
