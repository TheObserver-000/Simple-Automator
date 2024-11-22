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

-Number of Loops: Number of times the operations will be executed. Must be above 0.

-Start/Stop: Self explanatory.

On the buttom:

-Number of loops and operations will be shown when the program executes operations.""") == True:

        if messagebox.askokcancel(title="Help", icon= "question",message="""2/6

Mouse Operations:

-Move: Moves the cursor relative to its current position. Accepts positive and negative values.

-Move to: Moves the cursor to the given position.

-Click/Double Click/Right Click/Middle Click: Does the thing it says in given position. Leaving x and y empty will execute the operation in the current cursor position.

-Drag: Holds the left muse button and moves relative to its current position. Accepts positive and negative values.
                                  
-Drag to: Holds the left muse button and moves the cursor to the given position.

-X/Y Cordinate: Self explanatory.

-Move Duration: The time it takes for the cursor to move to the given position. 0 is instant. Supports float numbers.

-Pick Position: Starts getting the position of the cursor. Left/Right click to confirm.
                                  
WARNING: Do not use Mouse Operations around the screen edges. There is a great chance that program stops working.""") == True:
            if messagebox.askokcancel(title="Help", icon= "question",message="""3/6

Keyboard Operations:

-Press: Presses the given key.

-Hold/Release: Holds/Releases the given key.

WARNING: Don't forget to release the held keys (The program will try to release all held keys at the end of each loop, but do it yourself for safety).

-Hotkey: Presses given keys like hotkey.

-Write (Paste): Copies and pastes the given text (Recommended method).

-Write (Type): Actually types the text. Has more limitations. Only use if Paste method doesn't work.

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

-Operation Index: Where to add the operation on Blue List. Index starts from 1.

-Add Operation: Self explanatory. Will add the operation at given index. Leaving Operation Index empty will add the operation to the end of the list.

-Confirm: Apears in edit mode, instead of Add Operation.""") == True:
                        messagebox.showinfo(title="Help", icon= "question",message="""6/6

Settings:

-Sound: Self explanatory.

-Main window always on top: Main window stays above all programs.

-Secondary window always on top: Secondary windows (operation menus) stay above all programs.

-Hotkey: The key that starts and stops executing operations. User must choose between f1 to f12. This option can't be disabled (Because Why).

-Delay: Time between each operation. 0.1 or 0.5 seconds is recommended. 0 is instant.

WARNING: No delay means the program will execute around 70-80 operations per second. This will probably cause issues! Do at your own risk.
""")