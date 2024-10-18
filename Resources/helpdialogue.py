from tkinter import messagebox 

def help_window():
    if messagebox.askokcancel(title="Help", icon= "question",message= """Quick guide:

1/6

On the top:

-Settings: Opens settings window.

-Help: The reason you are here.

On the right:

-Blue List: Operations are shown here.

On the left:

-Add Operation: Opens a secondary window related to the current choice from the option menu next to it.

-Edit: Opens a secondary window related to the choosen operation from Blue List.

-Delete: Deletes the choosen operation from Blue List.

-Number of Loop: Number of times the operations will be executed. Must be above 0.

-Start/Stop: Self explanatory.

On the buttom:

-Number of loops and operations will be shown when the program executes operations.""") == True:

        if messagebox.askokcancel(title="Help", icon= "question",message="""2/6

Mouse Operations:

-Move: Moves cursor relative to its current position. Accepts positive and negative values.

-Move to: Moves the cursor to the given position.

-Click, Double Click, Right Click: Does the thing it says in given position. Leaving x and y empty will execute the operation in the current cursor position.

-x,y: Self explanatory.

-Duration: The time it takes for the cursor to move to the given position. 0 is instant.

-Pick Position: Starts getting the position of the cursor. Left/Right click to confirm.
                                  
WARNING: Do not use Mouse Operations around the screen edges. There is a great chance that program stops working.""") == True:
            if messagebox.askokcancel(title="Help", icon= "question",message="""3/6

Keyboard Operations:

-Press: Presses the given key.

-Hotkey: Presses given keys like hotkey.

-Write: Writes the given text. (Actually it doesn't write. It's a "copy and paste".)

-1st Key, 2nd Key, 3rd Key, Text: Entries for selected operation.

-Valid Keys: Shows a list of valid keys.""") == True:
                if messagebox.askokcancel(title="Help", icon= "question",message="""4/6

Time Operations:

-Delay: Waits for the amount of seconds it was given.

-Seconds: Self explanatory. Supports float numbers.""") == True:
                    if messagebox.askokcancel(title="Help", icon= "question",message="""5/6

Conditions:

-Clock: Executes the operation at the given time.

Add:

-Where to Add: Where to add the operation on Blue List. Leaving it empty will add the operation to the end of the list.

-Add Operation: Self explanatory.

-Confirm: Apears in edit mode.""") == True:
                        messagebox.showinfo(title="Help", icon= "question",message="""6/6

Settings:

-Sound: Self explanatory.

-Main window always on top: Main window stays above all programs.

-Secondary window always on top: Secondary window (settings and operation menus) stays above all programs.

-Hotkey: The key that can start and stop executing operations.
""")