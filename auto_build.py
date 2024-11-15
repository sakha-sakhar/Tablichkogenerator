import os

command = 'pyinstaller --noconfirm --onefile --windowed --icon "' + \
          os.path.abspath("images\icon100.ico") + \
          '" --hidden-import "pygame" --hidden-import "pygame_textinput" --hidden-import "tkinter" --hidden-import "PIL"  "' + \
          os.path.abspath("main.py") + '"'
print(command)

os.system(command)