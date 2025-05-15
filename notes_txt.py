#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QTextEdit,QInputDialog
import json
#показать нотис текстис
def show_note_text():
    key = list_notes.selectedItems()[0].text()
    name = list_notes.selectedItems()[0].text()
    for notes_list_txt in notes:
        if notes_list_txt[0] == key:
            main_edit_edit.setText(notes_list_txt[1])
            list_tags.clear()
            list_tags.addItems(notes_list_txt[2])
#создаем ноту 
def create_note():
    note_name, ok = QInputDialog.getText(main_win,'Доавить заметку','Название заметки')
    if note_name != '' and ok != '':
        notes_list_txt = list()
        notes_list_txt = [note_name,'',[]]
        notes.append(notes_list_txt)
        list_notes.addItem(notes_list_txt[0])
        list_tags.addItems(notes_list_txt[2])
        with open(str(len(notes)-1)+'.txt','w',encoding='utf-8') as file:
            file.write(notes_list_txt[0]+'\n')
#сохрание ноты
def safe_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for notes_list_txt in notes:
            if notes_list_txt[0] == key:
                notes_list_txt[1] = main_edit_edit.toPlainText()
                with open (str(index)+'.txt','w',encoding='utf-8') as file:
                    file.write(notes_list_txt[0]+'\n')
                    file.write(notes_list_txt[1]+'\n')
                    for tag in notes_list_txt[2]:
                        file.write(tag+' ')    
                    file.write('\n')   
            index += 1
def remove_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        main_edit_edit.clear()
        list_notes.addItems(notes)
        with open('f.json','w',encoding='utf-8') as file:
            json.dump(notes,file)
    else:
        print('заметка для удаления не бывбрана')

def add_tagx2():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag not in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('f.json','w',encoding='utf-8') as file:
            json.dump(notes,file)

def remove_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
    with open('f.json','w',encoding='utf-8') as file:
            json.dump(notes,file)

def search_tag():
    tag = field_tag.text()
    if search_note.text() == 'Искать заметку по тегу' and tag:
        filter_tags = dict()
        for note in notes:
            if tag in notes[note]['теги']:
                filter_tags[note] = notes[note]
        search_note.setText('сбросить поиск')
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(filter_tags)
    if search_note.text() == 'сбросить поиск':
        list_tags.clear()
        list_notes.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        search_note.setText('сбросить поиск')

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
#создание и удаление заметки
def add_note():
    #считывание названия заметки note_name
    if ok and note_name != "":
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        filename = str(len(notes)-1)+".txt"
        with open(filename, "w") as file:
            file.write(note[0]+'\n')


# Widgetы 
welcom = QLabel('Добро пожаловать!')
spisok_zametok = QLabel('Список заметок')
spisok_tegov = QLabel('Список тегов')
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...............')
main_edit_edit = QTextEdit()
list_tags = QListWidget()
list_notes = QListWidget()

save_tag = QPushButton('Сохранить заметку')
add_tag = QPushButton('Добавить заметку')
delete_tag = QPushButton('Удалить заметку')
add_note = QPushButton('Добавить к заметке')
replace_note = QPushButton('Открепить от заметки')
search_note = QPushButton('Искать заметку по тегу')


#подключение - ЧАСТЬ ласт
list_notes.itemClicked.connect(show_note_text)
#соеденение
add_tag.clicked.connect(create_note)
delete_tag.clicked.connect(remove_note)
save_tag.clicked.connect(safe_note)
search_note.clicked.connect(search_tag)
add_note.clicked.connect(add_tagx2)
replace_note.clicked.connect(remove_tag)


#Main layout
layout_main = QHBoxLayout()

#Left layout
layout_left = QVBoxLayout()
layout_left.addWidget(main_edit_edit)

#Right layout
layout_right = QVBoxLayout()

#Notes/spisok zametok 
layout_notes = QVBoxLayout()
layout_notes.addWidget(spisok_zametok)
layout_notes.addWidget(list_notes)
#buttons
notes_buttons_layout = QHBoxLayout()
notes_buttons_layout.addWidget(add_tag)
notes_buttons_layout.addWidget(delete_tag)
layout_notes.addLayout(notes_buttons_layout)

layout_notes.addWidget(save_tag)

# Tags section
layout_tags = QVBoxLayout()
layout_tags.addWidget(spisok_tegov)
layout_tags.addWidget(list_tags)
layout_tags.addWidget(field_tag)

tags_buttons_layout = QHBoxLayout()
tags_buttons_layout.addWidget(add_note)
tags_buttons_layout.addWidget(replace_note)
layout_tags.addLayout(tags_buttons_layout)

layout_tags.addWidget(search_note)

# Add sections to right layout
layout_right.addLayout(layout_notes)
layout_right.addLayout(layout_tags)

#e left and right layouts
layout_main.addLayout(layout_left)
layout_main.addLayout(layout_right)

#Список для заметок
notes = list()
notes_list_txt = list()
number_name = 0
while True:
    file_name = str(number_name)+'.txt'
    try:
        with open(file_name,'r',encoding = 'utf-8') as file:
            for line in file:
                line = line.replace('\n','')
                notes_list_txt.append(line)
        tag_txt = notes_list_txt[2].split(' ')
        notes_list_txt[2] = tag_txt
        notes.append(notes_list_txt)
        notes_list_txt = list()
        number_name += 1
    except IOError:
        break
for notes_list_txt in notes:
    list_notes.addItem(notes_list_txt[0])


main_win.setLayout(layout_main)
main_win.show()
app.exec()
