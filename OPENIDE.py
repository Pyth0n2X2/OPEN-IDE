from tkinter import *
import ctypes
import re
import os
import time
from tklinenums import TkLineNumbers
from tkinter import filedialog as fd
from tkinter import simpledialog
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter.messagebox
# Increas Dots Per inch so it looks sharper

# Setup Tkinter
root = Tk()
root.geometry('1920x768')


# Execute the Programm
def execute(event=None):

    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    # Start the File in a new CMD Window
    os.system('python run.py')

# Register Changes made to the Editor Content
def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        return

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i+=1

    previousText = editArea.get('1.0', END) 


def new_file():
    root.title("Untitled")
    editArea.delete(1.0, END)

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches
def open_file():
    filetypes = (
        ('All files', '*.*')
    )

    file = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
 
    if file is None:
        return

    else:
        try:
            root.title(os.path.basename(file))
            editArea.delete(1.0, END)

            file = open(file, "r")

            editArea.insert(1.0, file.read())

        except Exception:
            print("couldn't read file")

def save_file():
    file = fd.asksaveasfilename(initialfile='untitled.py',
                                        defaultextension=".OPEN",
                                        filetypes=[("Python file", "*.py*"),
                                                   ("All Files", "*.*")])

    if file is None:
        return

    else:
        try:
            root.title(os.path.basename(file))
            file = open(file, "w")

            file.write(editArea.get(1.0, END))

        except Exception:
            print("ERROR: Failed to save file")

        finally:
            file.close()
def quit():
    answer = askyesno(title="Quit", message ="Would you like to quit")
    save_file()
    if answer:  
        root.destroy()

def rgb(rgb):
    return "#%02x%02x%02x" % rgb
def create_sticky():
       #Create a Toplevel window
   top= Toplevel(root)
   top.title("Sticky note")
   top.geometry("480x240")
   top.config(background= rgb((42, 42, 42)))
   #Create an Entry Widget in the Toplevel window
   entry= Text(top, height=480, width=240)

   entry.pack()
def cut():
    editArea.event_generate("<<Cut>>")

def copy():
    editArea.event_generate("<<Copy>>")

def paste():
    editArea.event_generate("<<Paste>>")
previousText = ''

def replace():
    to_replace = simpledialog.askstring(title="Replace", prompt="Enter text to be replaced") 
    with_what_to_replace = simpledialog.askstring(title="Replace", prompt="Enter what to replace it with")
    # get content of text box
    text = editArea.get("1.0", "end-1c")
# clear text box
    editArea.delete("1.0", "end")
# insert the replace result back to text box
    editArea.insert("end", text.replace(to_replace, with_what_to_replace))


# Define colors for the variouse types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
font = 'monospace 18'


# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],  
    ['\'.*?\'', string],
    ['#.*?$', comments],
]
def update_line_numbers(event=None):
    line_numbers.config(state=tkinter.NORMAL)
    line_numbers.delete(1.0, tkinter.END)

    # Count the number of lines in the text widget
    num_lines = int(editArea.index('end-1c').split('.')[0])

    # Insert line numbers into the line_numbers Text widget
    for i in range(1, num_lines + 1):
        line_numbers.insert(tkinter.END, f"{i}\n")

    line_numbers.config(state=tkinter.DISABLED)
# Make the Text Widget
# Add a hefty border width so we can achieve a little bit of padding
editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    borderwidth=30,
    font=font
)

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    side="right",
    expand=1
)
line_numbers = tkinter.Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=tkinter.FLAT,
    borderwidth=30,
    width=5,  # Adjust the width as needed
    font=font
)

# Place the Line Numbers widget with the pack method
line_numbers.pack(side="left", fill="y")
line_numbers.config(background=background,foreground="white")

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)
editArea.bind('Control-s', save_file)

editArea.bind('<KeyRelease>', update_line_numbers)
editArea.bind('<Return>', update_line_numbers)
editArea.bind('<Shift-Up>', update_line_numbers)
editArea.bind('<Shift-Down>', update_line_numbers)

# Add some sample text to the text widget

# Initial update of line numbers
update_line_numbers()
# ... (your existing code)

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)
editArea.bind('Control-s', save_file)

# ... (your existing code)

# Start the Tkinter event loop
# Bind Control + R to the exec function
root.bind('<Control-r>', execute)
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Create sticky note", command=create_sticky)
file_menu.add_command(label="Exit", command=quit)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_command(label="Search & Replace", command=replace)
run_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_command(label="Run", command=execute)
root.title("OPEN IDE")
changes()
root.mainloop()