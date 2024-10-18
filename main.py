import pyautogui
#import pynput
from pynput.keyboard import Listener as KListener
from pynput.mouse import Listener as MListener
import threading
#import time
from time import strftime, sleep
from playsound import playsound
#import re
from re import search
#import os
from os import path
#import pyperclip
from pyperclip import copy
import json
from PIL import Image
import customtkinter as ctk
import CTkListbox as ctkl
from Resources import helpdialogue
#--------------------------------------------------------------------------------------------------------------
class Operation:

    def __init__(self, action, condition_type = None, condition = None):
        self.action = action
        self.condition_type = condition_type
        self.condition = condition
        
class Mouse(Operation):
    def __init__(self, action, x, y, duration = 0, condition_type = None, condition = None):
        super().__init__(action, condition_type, condition)
        self.x = x
        self.y = y
        self.duration = duration

class Keyboard(Operation):
    def __init__(self, action, key1 = None, key2 = None, key3 = None, write = None, condition_type = None, condition = None):
        super().__init__(action, condition_type, condition)
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3
        self.write = write

class Time(Operation):
    def __init__(self, action, seconds, condition_type = None, condition = None):
        super().__init__(action, condition_type, condition)
        self.seconds = seconds
#--------------------------------------------------------------------------------------------------------------
base_dir = path.dirname(path.abspath(__file__))
iconpic = path.join(base_dir, "app_icon.ico")

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Simple Automator")
root.config(background = "#1e1e21")
root.iconbitmap(path.join(base_dir, iconpic)) 
root.geometry(f"704x218+{int(pyautogui.size().width / 2) - int(704/2)}+{int(pyautogui.size().height / 2) - int(249/2)}")
root.resizable(False, False)
customfont = ctk.CTkFont("Calibri", 14)
#--------------------------------------------------------------------------------------------------------------










#--------------------------------------------------------------------------------------------------------------
def edit_blink_color():
    editbutton.configure(border_color= "#ee0000")
    editbutton.after(200, lambda: editbutton.configure(border_color= "#ff6600"))

def delete_blink_color():
    deletebutton.configure(border_color= "#ee0000")
    deletebutton.after(200, lambda: deletebutton.configure(border_color= "#ff6600"))

def on_destroy(event):
    global close
    if event.widget != root:
        return
    close = 1 

def delete_operation():
    try:
        i = listbox.curselection()
        listbox.delete(i)
        orderlist.pop(i)
    except:
        delete_blink_color()

def edit_operation():
    try:
        i = listbox.curselection()
        order = orderlist[i]
        if   order.action == "Delay":
            time_window(order = order, edit_mode = 1, index = i)
        elif order.action == "Move" or order.action == "Move to" or order.action == "Click" or order.action == "Double Click" or order.action == "Right Click":
            mouse_window(order = order, edit_mode = 1, index = i)
        elif order.action == "Press" or order.action == "Hotkey" or order.action == "Write":
            keyboard_window(order = order, edit_mode = 1, index = i)
    except:
        edit_blink_color()

def play_sound(option):
    global base_dir
    global sound_setting
    if sound_setting == 0:
        return
    
    if option == 1:
        playsound(path.join(base_dir, "Sounds", "click.mp3"))
    if option == 2:
        playsound(path.join(base_dir, "Sounds", "double_click.mp3"))
    if option == 3:
        playsound(path.join(base_dir, "Sounds", "press.mp3"))
    if option == 4:
        playsound(path.join(base_dir, "Sounds", "type.mp3"))
    if option == 5:
        playsound(path.join(base_dir, "Sounds", "tick.mp3"))
    if option == 6:
        playsound(path.join(base_dir, "Sounds", "finish.mp3"))

def make_sound_thread(option):
    soundthread = threading.Thread(target = lambda: play_sound(option))
    soundthreadslist.append(soundthread)
    soundthread.start()


def get_time():
    time_string = strftime("%H:%M:%S")
    time_list = time_string.split(":")
    return time_list

def check_condition(condition_type ,condition):
    global run
    global close
    if condition_type == "Clock":
        condition_list = condition.split(":")
        while close == 0:

            if run == 0:
                break

            time_list= get_time()
            if int(time_list[0]) == int(condition_list[0]) and int(time_list[1]) == int(condition_list[1]) and int(time_list[2]) == int(condition_list[2]):
                return True
            sleep(0.15)

def re_search(text):
    conditionform = search(r"(^0{1,2}|^[0-9]{1}|^0[0-9]{1}|^1[0-9]{1}|^2[0-3]{1}):([0-5]?[0-9]):([0-5]?[0-9]$)", text)
    if conditionform:
        return True
    return False

def perform_operation(order):
    global run
    global close
    if   (order.action) == "Delay":
        seconds = order.seconds
        while seconds != 0:
            if run == 0 or close == 1:
                break
            if seconds < 1:
                sleep(seconds)
                seconds =0
            else:
                if seconds != order.seconds:
                    make_sound_thread(5)
                sleep(1)
                seconds -=1

    elif order.action == "Move":
        xmove = order.x
        ymove = order.y
        
        if xmove < 0:
            if (xmove*-1) >= int(pyautogui.position().x):
                xmove = -int(pyautogui.position().x) + 1
        elif (xmove + int(pyautogui.position().x)) >= int(pyautogui.size().width) - 1:
            xmove = int(pyautogui.size().width) - int(pyautogui.position().x) - 2
     
        if ymove < 0:
            if (ymove*-1) >= int(pyautogui.position().y):
                ymove = -int(pyautogui.position().y) + 1
        elif (ymove + int(pyautogui.position().y)) >= int(pyautogui.size().height) - 1:
            ymove = int(pyautogui.size().height) - int(pyautogui.position().y) - 2

        if (int(pyautogui.position().x) <= 0) or (int(pyautogui.position().x) >= int(pyautogui.size().width) - 1) or (int(pyautogui.position().y) <= 0) or (int(pyautogui.position().y) == int(pyautogui.size().height) -1):
            return
        pyautogui.moveRel(xOffset= xmove, yOffset= ymove, duration= order.duration)

    elif order.action == "Move to":
        pyautogui.moveTo(x= order.x, y= order.y, duration= order.duration)
    elif order.action == "Click":
        if order.x == None and order.y == None:
            pyautogui.click(clicks=1, button='left')
        else:
            pyautogui.click(x= order.x, y= order.y, duration= order.duration, clicks=1, button='left')
        make_sound_thread(1)
    elif order.action == "Double Click":
        if order.x == None and order.y == None:
            pyautogui.click(clicks=2, interval=0.15, button='left') 
        else:
            pyautogui.click(x= order.x, y= order.y, duration= order.duration, clicks=2, interval=0.15, button='left') 
        make_sound_thread(2)  
    elif order.action == "Right Click":
        if order.x == None and order.y == None:
            pyautogui.click(clicks=1, button='right') 
        else:
            pyautogui.click(x= order.x, y= order.y, duration= order.duration, clicks=1, button='right') 
        make_sound_thread(1)
    elif order.action == "Press":
        pyautogui.press(order.key1)
        make_sound_thread(3)
    elif order.action == "Hotkey":
        if order.key3 == None:
            pyautogui.hotkey(order.key1, order.key2)
        else:
            pyautogui.hotkey(order.key1, order.key2, order.key3)
        make_sound_thread(3)
    elif order.action == "Write":
        copy(order.write)
        pyautogui.hotkey('ctrl', 'v')
        make_sound_thread(4)
    
def startloop_set():
    global run
    global trigger_wait
    if run == 1:
        try:
            startbutton.configure(text = "Stopping", state = "disabled", border_color= "#808080")
        except:
            pass
        trigger_wait = 1
        run = 0
    elif run == 0 and trigger_wait== 0:
        for thread in startthreadslist:
            try:
                thread.join()
            except:
                pass
        run = 1
        startloop_thread = threading.Thread(target= startloop)
        startloop_thread.start()
        threadslist.append(startloop_thread)
    
def startloop():
    global close
    global run
    global trigger_wait
    global repeatcount
    try:
        if loopcountentry.get().isdigit() == False or int(loopcountentry.get()) == 0:
            repeatcount = 1
            loopcountentry.delete(0, ctk.END)
            loopcountentry.insert(0, 1)
        else:
            repeatcount = int(loopcountentry.get())

        if int(len(orderlist)) == 0:
            run = 0
            trigger_wait = 0
            return

        addbutton.configure(state = "disabled", border_color= "#808080")
        editbutton.configure(state = "disabled", border_color= "#808080")
        deletebutton.configure(state = "disabled", border_color= "#808080")
        loopcountentry.configure(state = "disabled", border_color= "#808080")
        startbutton.configure(text = "Stop")
            

        numberofrounds = repeatcount
        roundcounter = 1
        numberoforders = int(len(orderlist))
        ordercounter = 1

        for round in range(repeatcount):

            labelround.configure(text = f"{roundcounter}/{numberofrounds}")

            if run == 0:
                break

            for order in orderlist:

                labelorder.configure(text = f"{ordercounter}/{numberoforders}")

                if run == 0:
                    break
                
                if order.condition_type != "No Condition":
                    if check_condition(order.condition_type ,order.condition) == True:
                        perform_operation(order) 
                else:
                    perform_operation(order) 
                
                ordercounter += 1

            ordercounter = 1
            roundcounter += 1

        addbutton.configure(state = "normal", border_color= "#ff6600")
        editbutton.configure(state = "normal", border_color= "#ff6600")
        deletebutton.configure(state = "normal", border_color= "#ff6600")
        loopcountentry.configure(state = "normal", border_color= "#eec643")
        startbutton.configure(text = "Start", state = "normal", border_color= "#eec643")
        labelround.configure(text = "")
        labelorder.configure(text = "")

        for thread in soundthreadslist:
            try:
                thread.join()
            except:
                pass
        
        make_sound_thread(6)

        startbutton.configure(text = "Start", state = "normal", border_color= "#eec643")
        
        trigger_wait = 0
        run = 0 
    except:
        pass          

def start_stop_hotkey():
    global close
    global trigger_key_pynput
    while close == 0:

        def on_press(key):
            if str(key) == trigger_key_pynput:
                startloop_set()
                return False
        
        try:
            global triggerlistener
            triggerlistener = KListener(on_press=on_press)

            triggerlistener.start()
            triggerlistener.join()
        except:
            return
        
        sleep(0.05)   
#--------------------------------------------------------------------------------------------------------------
            









#--------------------------------------------------------------------------------------------------------------
def mouse_window(edit_mode = 0, order = None, index = None):
#--------------------------------------------------------------------------------------------------------------
    def mw_position_blink_color():
        mw_pick_position.configure(border_color= "#00dd00")
        mw_pick_position.after(200, lambda: mw_pick_position.configure(border_color= "#5a64a0"))

    def mw_blink_color():
        mw_add.configure(border_color= "#00dd00")
        mw_add.after(200, lambda: mw_add.configure(border_color= "#ff6600"))
    
    def mw_condition_placeholder(*arg):
        if mw_condition_optionmenu.get() == "No Condition":
            mw_condition.delete(0, ctk.END)
            mw_condition.configure(placeholder_text = "Condition")
            mw_condition.after(5, lambda: mw_condition.configure(state = "disabled", border_color= "#808080"))    
        elif mw_condition_optionmenu.get() == "Clock":
            mw_condition.configure(state = "normal", border_color= "#eec643")
            mw_condition.delete(0, ctk.END)
            mw_condition.after(5, lambda: mw_condition.configure(placeholder_text = "e.g. 23:59:59"))
        mousewindow.focus_set()
#--------------------------------------------------------------------------------------------------------------
    def mw_set_operation(edit_mode = 0, order = None, index = None):

        if mw_x.get() == "" and mw_y.get() == "":
            if mw_action_optionmenu.get() == "Move" or mw_action_optionmenu.get() == "Move to":
                mw_x.configure(border_color= "#ee0000")
                mw_y.configure(border_color= "#ee0000")
                mousewindow.focus_set()
                return
            mw_x.configure(border_color= "#ff6600")
            mw_y.configure(border_color= "#ff6600")
            
        else:

            if mw_action_optionmenu.get() == "Move":
                try:
                    int(mw_x.get())
                except:
                    mw_x.delete(0, ctk.END)
                    mw_x.configure(placeholder_text = "x position")
                    mw_x.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_x.configure(border_color= "#ff6600")

                try:
                    int(mw_y.get())
                except:
                    mw_y.delete(0, ctk.END)
                    mw_y.configure(placeholder_text = "y position")
                    mw_y.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_y.configure(border_color= "#ff6600")

            else:
                if mw_x.get().isdigit() == False:
                    mw_x.delete(0, ctk.END)
                    mw_x.configure(placeholder_text = "x position")
                    mw_x.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_x.configure(border_color= "#ff6600")

                if int(mw_x.get()) >= int(pyautogui.size().width):
                    mw_x.delete(0, ctk.END)
                    mw_x.configure(placeholder_text = "x position")
                    mw_x.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_x.configure(border_color= "#ff6600")

                if mw_y.get().isdigit() == False:
                    mw_y.delete(0, ctk.END)
                    mw_y.configure(placeholder_text = "y position")
                    mw_y.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_y.configure(border_color= "#ff6600")

                if int(mw_y.get()) >= int(pyautogui.size().height):
                    mw_y.delete(0, ctk.END)
                    mw_y.configure(placeholder_text = "y position")
                    mw_y.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                mw_y.configure(border_color= "#ff6600")

        if mw_duration.get() == "":
            mw_duration.delete(0, ctk.END)
            mw_duration.insert(0, 0.0)
        try:
            float(mw_duration.get())
            if float(mw_duration.get()) < 0:
                raise Exception
        except:
            mw_duration.delete(0, ctk.END)
            mw_duration.insert(0, 0.0)
            mw_duration.configure(border_color= "#ee0000")
            mousewindow.focus_set()
            return
        mw_duration.configure(border_color= "#ff6600")
        

        if edit_mode == 0:
            if mw_addindex.get() != "":
                if mw_addindex.get().isdigit() == False:
                    mw_addindex.delete(0, ctk.END)
                    mw_addindex.configure(placeholder_text = "Where to Add")
                    mw_addindex.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
                if int(mw_addindex.get()) == 0 or int(mw_addindex.get()) > (int(len(orderlist)) + 1):
                    mw_addindex.delete(0, ctk.END)
                    mw_addindex.configure(placeholder_text = "Where to Add")
                    mw_addindex.configure(border_color= "#ee0000")
                    mousewindow.focus_set()
                    return
            mw_addindex.configure(border_color= "#ff6600")
        
        if   mw_condition_optionmenu.get() == "No Condition":
            mw_condition.delete(0, ctk.END)
            mw_condition_placeholder()
            mousewindow.focus_set()
        elif mw_condition_optionmenu.get() == "Clock":
            if re_search(mw_condition.get()) is True:
                pass
            else:
                mw_condition.delete(0, ctk.END)
                mw_condition_placeholder()
                mw_condition.configure(border_color= "#ee0000")
                mousewindow.focus_set()
                return
        mw_condition.configure(border_color= "#eec643")

        if edit_mode == 1:
            order.action = mw_action_optionmenu.get()
            if mw_x.get() == "" and mw_y.get() == "":
                order.x = None
                order.y = None
                order.duration = 0
            else:
                order.x = int(mw_x.get())
                order.y = int(mw_y.get())
                order.duration = float(mw_duration.get())
            order.condition_type = mw_condition_optionmenu.get()
            order.condition = mw_condition.get()

            orderlist.pop(index)
            orderlist.insert(index, order)

            info = []
            for i in range (index + 1, listbox.size()):
                info.append(listbox.get(i))

            for i in range (listbox.size()-1, index-1, -1):
                listbox.delete(i)
            
            if order.x == None and order.y == None:
                listbox.insert("END", f"{order.action}, {order.condition_type} {order.condition}")
            else:
                listbox.insert("END", f"{order.action}, {order.x}x{order.y}, D={order.duration}, {order.condition_type} {order.condition}")

            for i in info:
                listbox.insert("END", i)

        else:
            order = Mouse(action = mw_action_optionmenu.get(), x= mw_x.get(), y= mw_y.get(), duration= float(mw_duration.get()), condition_type= mw_condition_optionmenu.get(), condition= mw_condition.get())
            
            if mw_x.get() == "" and mw_y.get() == "":
                order.x = None
                order.y = None
                order.duration = 0.0
            else:
                order.x= int(mw_x.get())
                order.y= int(mw_y.get())

            if mw_addindex.get() == "" or int(mw_addindex.get()) == int(len(orderlist)) + 1:
                orderlist.append(order)
                if mw_x.get() == "" and mw_y.get() == "":
                    listbox.insert("END", f"{order.action}, {order.condition_type} {order.condition}")
                else:
                    listbox.insert("END", f"{order.action}, {order.x}x{order.y}, D={order.duration}, {order.condition_type} {order.condition}")
            
            else:
                index = int(mw_addindex.get()) - 1
                orderlist.insert(index, order)

                info = []
                for i in range (index, listbox.size()):
                    info.append(listbox.get(i))

                for i in range (listbox.size()-1, index-1, -1):
                    listbox.delete(i)
                
                if order.x == None and order.y == None:
                    listbox.insert("END", f"{order.action}, {order.condition_type} {order.condition}")
                else:
                    listbox.insert("END", f"{order.action}, {order.x}x{order.y}, D={order.duration}, {order.condition_type} {order.condition}")

                for i in info:
                    listbox.insert("END", i)
            
        mw_x.delete(0, ctk.END)
        mw_x.configure(placeholder_text = "x position")
        mw_y.delete(0, ctk.END)
        mw_y.configure(placeholder_text = "y position")
        if order.x == None and order.y == None:
            mw_duration.delete(0, ctk.END)
            mw_duration.insert(0, 0.0)
        mw_condition_optionmenu.set("No Condition")
        mw_condition.delete(0, ctk.END)
        mw_condition_placeholder()
        if edit_mode == 0:
            mw_addindex.delete(0, ctk.END)
            mw_addindex.configure(placeholder_text = "Where to Add")
        mousewindow.focus_set()

        if edit_mode == 1:
            mousewindow.destroy()
        else:
            mw_blink_color()
#--------------------------------------------------------------------------------------------------------------    
    def set_position():
        global getpos
        if   getpos == 0:
            getpos = 1
        elif getpos == 1:
            getpos = 0
    
    def get_position():
        global close
        global getpos
        global click_detected

        while close == 0:

            if getpos == 1:
                def pos(*arg):
                        if not click_detected:
                            try:
                                x,y= pyautogui.position()
                                mw_x.delete(0, ctk.END)
                                mw_y.delete(0, ctk.END)
                                mw_x.insert(0, x)
                                mw_y.insert(0, y)
                            except:
                                pass
                        else:
                            return False

                def click(x,y,button,pressed):
                            global click_detected
                            if pressed:
                                click_detected = True
                                mw_position_blink_color()
                                return False
                try:
                    global child_window_ontop
                    if child_window_ontop == 0:
                        mousewindow.attributes("-topmost", True)

                    mouselistener = MListener(on_move=pos)
                    clicklistener = MListener(on_click=click)

                    clicklistener.start()
                    mouselistener.start()

                    clicklistener.join()
                    mouselistener.join()

                    getpos = 0
                    click_detected= False
                    if child_window_ontop == 0:
                        mousewindow.attributes("-topmost", False)
                except:
                    return

            sleep(0.05)
#--------------------------------------------------------------------------------------------------------------   
    mousewindow = ctk.CTkToplevel(root)
    mousewindow.title("Add Mouse Operation")
    mousewindow.config(background = "#1e1e21")
    mousewindow.iconbitmap(path.join(base_dir, "app_icon.ico"))
    mousewindow.geometry(f"760x86+{int(pyautogui.size().width / 2) - int(760/2)}+{int(pyautogui.size().height / 2) - int(117/2)}")
    mousewindow.resizable(False, False)
    mousewindow.grab_set()
    
    mf1 = ctk.CTkFrame(mousewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    mf1.grid(column = 0, row = 0, rowspan = 3, sticky= "nsew")

    mf2 = ctk.CTkFrame(mousewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    mf2.grid(column = 1, row = 0, sticky= "nsew")

    mf3 = ctk.CTkFrame(mousewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
    mf3.grid(column = 1, row = 1, sticky= "nsew")

    mf4 = ctk.CTkFrame(mousewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    mf4.grid(column = 1, row = 2, sticky= "ew")

    mf5 = ctk.CTkFrame(mousewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    mf5.grid(column = 2, row = 0, rowspan = 3, sticky= "nsew")

    global child_window_ontop
    if child_window_ontop == 1:
        mousewindow.attributes("-topmost", True)
    else:
        mousewindow.attributes("-topmost", False)
    
    global get_position_thread
    get_position_thread = threading.Thread(target=get_position)
    get_position_thread.start()
    threadslist.append(get_position_thread)

    mw_actions = ["Move", "Move to", "Click", "Double Click", "Right Click"]
    mw_action_optionmenu = ctk.CTkOptionMenu(mf3, values= mw_actions, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#ff6600", button_color= "#ff6600", button_hover_color= "#b34700", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#ff6600", font= customfont, dropdown_font= customfont)
    mw_action_optionmenu.set("Move")
    mw_action_optionmenu.grid(column = 0, row = 0, padx = 5, pady = 5)

    mw_x = ctk.CTkEntry(mf3, placeholder_text="x position",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    mw_x.grid(column = 1, row = 0, padx = 5, pady = 5)
    
    mw_y = ctk.CTkEntry(mf3, placeholder_text="y position", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    mw_y.grid(column = 2, row = 0, padx = 5, pady = 5)

    mw_duration = ctk.CTkEntry(mf3, placeholder_text="Move duration", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    mw_duration.grid(column = 3, row = 0, padx = 5, pady = 5)
    mw_duration.insert(0, 0.0)

    mw_condition_options = ["No Condition", "Clock"]
    mw_condition_optionmenu = ctk.CTkOptionMenu(mf3, values= mw_condition_options,command= mw_condition_placeholder, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#eec643", button_color= "#eec643", button_hover_color= "#a3800f", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#eec643", font= customfont, dropdown_font= customfont)
    mw_condition_optionmenu.set("No Condition")
    mw_condition_optionmenu.grid(column = 0, row = 1, padx = 5, pady = 5)

    mw_condition = ctk.CTkEntry(mf3, placeholder_text="Condition", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", justify="center", font= customfont)
    mw_condition.grid(column = 1, row = 1, padx = 5, pady = 5)
    if edit_mode == 0:
        mw_condition_placeholder()

    if edit_mode == 0:
        mw_addindex = ctk.CTkEntry(mf3, placeholder_text="Where to Add", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
        mw_addindex.grid(column = 2, row = 1, padx = 5, pady = 5)

    mw_add = ctk.CTkButton(mf3, command= lambda: mw_set_operation(edit_mode = edit_mode, order = order, index = index), text="Add Operation", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", font= customfont)
    mw_add.grid(column = 4, row = 0, padx = 5, pady = 5)

    mw_pick_position = ctk.CTkButton(mf3, command= set_position, text="Pick Position", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#2d3746", hover_color= "#192332", border_width= 2, border_color= "#5a64a0", text_color= "#e8e6e5", font= customfont)
    mw_pick_position.grid(column = 4, row = 1, padx = 5, pady = 5)

    if edit_mode == 1:
        mousewindow.title("Modify Mouse Operation")
        mw_action_optionmenu.set(order.action)
        if (order.x) != None and (order.y) != None:
            mw_x.insert(0,order.x)
            mw_y.insert(0,order.y)
        mw_duration.delete(0, ctk.END)
        mw_duration.insert(0,order.duration)
        mw_condition_optionmenu.set(order.condition_type)
        mw_condition.insert(0,order.condition)
        if mw_condition_optionmenu.get() == "No Condition":
            mw_condition.delete(0, ctk.END)
        mw_condition_placeholder()
        mw_add.configure(text="Confirm")

    mousewindow.after(200, lambda: mousewindow.iconbitmap(iconpic))
#--------------------------------------------------------------------------------------------------------------










#--------------------------------------------------------------------------------------------------------------
def keyboard_window(edit_mode = 0, order = None, index = None):
#--------------------------------------------------------------------------------------------------------------
    def kw_blink_color():
        kw_add.configure(border_color= "#00dd00")
        kw_add.after(200, lambda: kw_add.configure(border_color= "#ff6600"))

    def kw_action_configuration(*arg):
        if kw_action_optionmenu.get() == "Press":

            kw_key1.configure(state = "normal", border_color= "#ff6600")
            kw_key1.after(5, lambda: kw_key1.configure(placeholder_text = "1st Key"))

            kw_key2.delete(0, ctk.END)
            kw_key2.configure(placeholder_text = "2nd Key")
            kw_key2.after(5, lambda: kw_key2.configure(state = "disabled", border_color= "#808080"))

            kw_key3.delete(0, ctk.END)
            kw_key3.configure(placeholder_text = "3rd Key (Optional)")
            kw_key3.after(5, lambda: kw_key3.configure(state = "disabled", border_color= "#808080"))

            kw_textentry.delete(0, ctk.END)
            kw_textentry.configure(placeholder_text = "Text")
            kw_textentry.after(5, lambda: kw_textentry.configure(state = "disabled", border_color= "#808080"))
            
        elif kw_action_optionmenu.get() == "Hotkey":

            kw_key1.configure(placeholder_text = "1st Key")
            kw_key1.after(5, lambda: kw_key1.configure(state = "normal", border_color= "#ff6600"))

            kw_key2.configure(state = "normal", border_color= "#ff6600")
            kw_key2.after(5, lambda: kw_key2.configure(placeholder_text = "2nd Key"))

            kw_key3.configure(state = "normal", border_color= "#ff6600")
            kw_key3.after(5, lambda: kw_key3.configure(placeholder_text = "3rd Key (Optional)"))
            
            kw_textentry.configure(placeholder_text = "Text")
            kw_textentry.after(5, lambda: kw_textentry.configure(state = "disabled", border_color= "#808080"))

        elif kw_action_optionmenu.get() == "Write":

            kw_key1.delete(0, ctk.END)
            kw_key1.configure(placeholder_text = "1st Key")
            kw_key1.after(5, lambda: kw_key1.configure(state = "disabled", border_color= "#808080"))

            kw_key2.delete(0, ctk.END)
            kw_key2.configure(placeholder_text = "2nd Key")
            kw_key2.after(5, lambda: kw_key2.configure(state = "disabled", border_color= "#808080"))

            kw_key3.delete(0, ctk.END)
            kw_key3.configure(placeholder_text = "3rd Key (Optional)")
            kw_key3.after(5, lambda: kw_key3.configure(state = "disabled", border_color= "#808080"))

            kw_textentry.configure(state = "normal", border_color= "#ff6600")
            kw_textentry.after(5, lambda: kw_textentry.configure(placeholder_text = "Text"))

        keyboardwindow.focus_set()
        
    def show_valid_keys():
        validkeyswindow = ctk.CTkToplevel(keyboardwindow)
        validkeyswindow.title("Valid Keys")
        validkeyswindow.config(background = "#1e1e21")
        validkeyswindow.iconbitmap(path.join(base_dir, "app_icon.ico"))
        validkeyswindow.geometry(f"200x400+{int(pyautogui.size().width / 2) - int(200/2) - 500}+{int(pyautogui.size().height / 2) - int(431/2)}")
        validkeyswindow.resizable(False, False)

        global child_window_ontop
        if child_window_ontop == 1:
            validkeyswindow.attributes("-topmost", True)
        else:
            validkeyswindow.attributes("-topmost", False)
        
        showvalidkeys = ctk.CTkTextbox(validkeyswindow, width= 200, height= 400, corner_radius= 0, border_width = 2, border_color= "#5a64a0",scrollbar_button_color= "#5a64a0", scrollbar_button_hover_color= "#5a64a0", text_color= "#e8e6e5")
        showvalidkeys.grid(column = 0, row = 0, sticky= "nsew")

        global keys
        for key in keys:
            showvalidkeys.insert(ctk.END, (key + "\n"))
        showvalidkeys.configure(state= "disabled")

    def kw_condition_placeholder(*arg):
        if kw_condition_optionmenu.get() == "No Condition":
            kw_condition.delete(0, ctk.END)
            kw_condition.configure(placeholder_text = "Condition")
            kw_condition.after(5, lambda: kw_condition.configure(state = "disabled", border_color= "#808080"))
        elif kw_condition_optionmenu.get() == "Clock":
            kw_condition.configure(state = "normal", border_color= "#eec643")
            kw_condition.delete(0, ctk.END)
            kw_condition.after(5, lambda: kw_condition.configure(placeholder_text = "e.g. 23:59:59"))
        keyboardwindow.focus_set()
#--------------------------------------------------------------------------------------------------------------
    def kw_set_operation(edit_mode = 0, order = None, index = None):

        if kw_action_optionmenu.get() == "Press" or kw_action_optionmenu.get() == "Hotkey":
            if kw_key1.get().lower() not in keys:
                kw_key1.delete(0, ctk.END)
                kw_key1.configure(placeholder_text = "1st Key")
                kw_key1.configure(border_color= "#ee0000")
                keyboardwindow.focus_set()
                return
            kw_key1.configure(border_color= "#ff6600")
        
        if kw_action_optionmenu.get() == "Hotkey":
            hotkey_count = 3
            if kw_key2.get().lower() not in keys:
                kw_key2.delete(0, ctk.END)
                kw_key2.configure(placeholder_text = "2nd Key")
                kw_key2.configure(border_color= "#ee0000")
                keyboardwindow.focus_set()
                return
            kw_key2.configure(border_color= "#ff6600")
        
        if kw_action_optionmenu.get() == "Hotkey":
            if kw_key3.get().lower() not in keys:
                if kw_key3.get() == "" or kw_key3.get() == None:
                    kw_key3.delete(0, ctk.END)
                    kw_key3.configure(placeholder_text = "3rd Key (Optional)")
                    hotkey_count = 2
                else:
                    kw_key3.delete(0, ctk.END)
                    kw_key3.configure(placeholder_text = "3rd Key (Optional)")
                    kw_key3.configure(border_color= "#ee0000")
                    keyboardwindow.focus_set()
                    return
            keyboardwindow.focus_set()
            kw_key3.configure(border_color= "#ff6600")
        
        if kw_action_optionmenu.get() == "Write":
            if kw_textentry.get() == "" or kw_textentry.get() == None:
                kw_textentry.delete(0, ctk.END)
                kw_textentry.configure(placeholder_text = "Text")
                kw_textentry.configure(border_color= "#ee0000")
                keyboardwindow.focus_set()
                return
            kw_textentry.configure(border_color= "#ff6600")

        if edit_mode == 0:
            if kw_addindex.get() != "":
                if kw_addindex.get().isdigit() == False:
                    kw_addindex.delete(0, ctk.END)
                    kw_addindex.configure(placeholder_text = "Where to Add")
                    kw_addindex.configure(border_color= "#ee0000")
                    keyboardwindow.focus_set()
                    return
                if int(kw_addindex.get()) == 0 or int(kw_addindex.get()) > (int(len(orderlist)) + 1):
                    kw_addindex.delete(0, ctk.END)
                    kw_addindex.configure(placeholder_text = "Where to Add")
                    kw_addindex.configure(border_color= "#ee0000")
                    keyboardwindow.focus_set()
                    return
            kw_addindex.configure(border_color= "#ff6600")

        if   kw_condition_optionmenu.get() == "No Condition":
            kw_condition.delete(0, ctk.END)
            kw_condition_placeholder()
            keyboardwindow.focus_set()
        elif kw_condition_optionmenu.get() == "Clock":
            if re_search(kw_condition.get()) is True:
                pass
            else:
                kw_condition.delete(0, ctk.END)
                kw_condition_placeholder()
                kw_condition.configure(border_color= "#ee0000")
                keyboardwindow.focus_set()
                return
        kw_condition.configure(border_color= "#eec643")

        if edit_mode == 1:
            if kw_action_optionmenu.get() == "Press":
                order.action= kw_action_optionmenu.get()
                order.key1 = kw_key1.get()
                order.key2 = None
                order.key3 = None
                order.write = None
            
            elif kw_action_optionmenu.get() == "Hotkey":
                if   hotkey_count == 2:
                    order.action= kw_action_optionmenu.get()
                    order.key1 = kw_key1.get()
                    order.key2 = kw_key2.get()
                    order.key3 = None
                    order.write = None
                elif hotkey_count == 3:
                    order.action= kw_action_optionmenu.get()
                    order.key1 = kw_key1.get()
                    order.key2 = kw_key2.get()
                    order.key3 = kw_key3.get()
                    order.write = None

            elif kw_action_optionmenu.get() == "Write":
                order.action= kw_action_optionmenu.get()
                order.key1 = None
                order.key2 = None
                order.key3 = None
                order.write = kw_textentry.get()
            
            order.condition_type = kw_condition_optionmenu.get()
            order.condition = kw_condition.get()
                
            orderlist.pop(index)
            orderlist.insert(index, order)
                
            info = []
            for i in range (index + 1, listbox.size()):
                info.append(listbox.get(i))

            for i in range (listbox.size()-1, index-1, -1):
                listbox.delete(i)

            if kw_action_optionmenu.get() == "Press":
                listbox.insert("END", f"{order.action}, {order.key1}, {order.condition_type} {order.condition}")
            
            elif kw_action_optionmenu.get() == "Hotkey":

                if   hotkey_count == 2:
                    listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}, {order.condition_type} {order.condition}")
                elif hotkey_count == 3:
                    listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}+{order.key3}, {order.condition_type} {order.condition}")

            elif kw_action_optionmenu.get() == "Write":
                if len(order.write) > 20:
                    txt = order.write[0:20] + "..."
                    listbox.insert("END", f'{order.action}, "{txt}", {order.condition_type} {order.condition}')
                else:
                    listbox.insert("END", f'{order.action}, "{order.write}", {order.condition_type} {order.condition}')    

            for i in info:
                listbox.insert("END", i)

        else:

            if kw_action_optionmenu.get() == "Press":
                order = Keyboard(action= kw_action_optionmenu.get(), key1 = kw_key1.get(), key2 = None, key3 = None, write = None, condition_type = kw_condition_optionmenu.get(), condition = kw_condition.get())
            elif kw_action_optionmenu.get() == "Hotkey":
                if   hotkey_count == 2:
                    order = Keyboard(action= kw_action_optionmenu.get(), key1 = kw_key1.get(), key2 = kw_key2.get(), key3 = None, write = None, condition_type = kw_condition_optionmenu.get(), condition = kw_condition.get())
                elif hotkey_count == 3:
                    order = Keyboard(action= kw_action_optionmenu.get(), key1 = kw_key1.get(), key2 = kw_key2.get(), key3 = kw_key3.get(), write = None, condition_type = kw_condition_optionmenu.get(), condition = kw_condition.get())
            elif kw_action_optionmenu.get() == "Write":
                order = Keyboard(action= kw_action_optionmenu.get(), key1 = None, key2 = None, key3 = None, write = kw_textentry.get(), condition_type = kw_condition_optionmenu.get(), condition = kw_condition.get())
            
            if kw_addindex.get() == "" or int(kw_addindex.get()) == int(len(orderlist)) + 1:
                orderlist.append(order)

                if kw_action_optionmenu.get() == "Press":
                    listbox.insert("END", f"{order.action}, {order.key1}, {order.condition_type} {order.condition}")
                elif kw_action_optionmenu.get() == "Hotkey":
                    if   hotkey_count == 2:
                        listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}, {order.condition_type} {order.condition}")
                    elif hotkey_count == 3:
                        listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}+{order.key3}, {order.condition_type} {order.condition}")
                elif kw_action_optionmenu.get() == "Write":
                    if len(order.write) > 20:
                        txt = order.write[0:20] + "..."
                        listbox.insert("END", f'{order.action}, "{txt}", {order.condition_type} {order.condition}')
                    else:
                        listbox.insert("END", f'{order.action}, "{order.write}", {order.condition_type} {order.condition}')    
            
            else:  
                index = int(kw_addindex.get()) - 1
                orderlist.insert(index, order)

                info = []
                for i in range (index, listbox.size()):
                    info.append(listbox.get(i))

                for i in range (listbox.size()-1, index-1, -1):
                    listbox.delete(i)

                if kw_action_optionmenu.get() == "Press":
                    listbox.insert("END", f"{order.action}, {order.key1}, {order.condition_type} {order.condition}")
                elif kw_action_optionmenu.get() == "Hotkey":
                    if   hotkey_count == 2:
                        listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}, {order.condition_type} {order.condition}")
                    elif hotkey_count == 3:
                        listbox.insert("END", f"{order.action}, {order.key1}+{order.key2}+{order.key3}, {order.condition_type} {order.condition}")
                elif kw_action_optionmenu.get() == "Write":
                    if len(order.write) > 20:
                        txt = order.write[0:20] + "..."
                        listbox.insert("END", f'{order.action}, "{txt}", {order.condition_type} {order.condition}')
                    else:
                        listbox.insert("END", f'{order.action}, "{order.write}", {order.condition_type} {order.condition}')    

                for i in info:
                    listbox.insert("END", i)         

        kw_key1.delete(0, ctk.END)
        kw_key1.configure(placeholder_text = "1st Key")
        kw_key2.delete(0, ctk.END)
        kw_key2.configure(placeholder_text = "2nd Key")
        kw_key3.delete(0, ctk.END)
        kw_key3.configure(placeholder_text = "3rd Key (Optional)")
        kw_textentry.delete(0, ctk.END)
        kw_textentry.configure(placeholder_text = "Text")
        kw_condition_optionmenu.set("No Condition")
        kw_condition.delete(0, ctk.END)
        kw_condition_placeholder()
        if edit_mode == 0:
            kw_addindex.delete(0, ctk.END)
            kw_addindex.configure(placeholder_text = "Where to Add")
        keyboardwindow.focus_set()

        if edit_mode == 1:
            keyboardwindow.destroy()
        else:
            kw_blink_color()

#--------------------------------------------------------------------------------------------------------------
    keyboardwindow = ctk.CTkToplevel(root)
    keyboardwindow.title("Add Keyboard Operation")
    keyboardwindow.config(background = "#1e1e21")
    keyboardwindow.iconbitmap(path.join(base_dir, "app_icon.ico"))
    keyboardwindow.geometry(f"760x124+{int(pyautogui.size().width / 2) - int(760/2)}+{int(pyautogui.size().height / 2) - int(155/2)}")
    keyboardwindow.resizable(False, False)
    keyboardwindow.grab_set()


    kf1 = ctk.CTkFrame(keyboardwindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    kf1.grid(column = 0, row = 0, rowspan = 3, sticky= "nsew")

    kf2 = ctk.CTkFrame(keyboardwindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    kf2.grid(column = 1, row = 0, sticky= "nsew")

    kf3 = ctk.CTkFrame(keyboardwindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
    kf3.grid(column = 1, row = 1, sticky= "nsew")

    kf4 = ctk.CTkFrame(keyboardwindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    kf4.grid(column = 1, row = 2, sticky= "ew")

    kf5 = ctk.CTkFrame(keyboardwindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    kf5.grid(column = 2, row = 0, rowspan = 3, sticky= "nsew")

    global child_window_ontop
    if child_window_ontop == 1:
        keyboardwindow.attributes("-topmost", True)
    else:
        keyboardwindow.attributes("-topmost", False)

    kw_actions = ["Press", "Hotkey", "Write"]
    kw_action_optionmenu = ctk.CTkOptionMenu(kf3, values= kw_actions, command= kw_action_configuration, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#ff6600", button_color= "#ff6600", button_hover_color= "#b34700", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#ff6600", font= customfont, dropdown_font= customfont)
    kw_action_optionmenu.set("Press")
    kw_action_optionmenu.grid(column = 0, row = 0, padx = 5, pady = 5)

    kw_key1 = ctk.CTkEntry(kf3, placeholder_text="1st Key",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    kw_key1.grid(column = 1, row = 0, padx = 5, pady = 5)
    
    kw_key2 = ctk.CTkEntry(kf3, placeholder_text="2nd Key",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    kw_key2.grid(column = 2, row = 0, padx = 5, pady = 5)

    kw_key3 = ctk.CTkEntry(kf3, placeholder_text="3rd Key (Optional)",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    kw_key3.grid(column = 3, row = 0, padx = 5, pady = 5)

    kw_textentry = ctk.CTkEntry(kf3, placeholder_text="Text",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="left", font= customfont)
    kw_textentry.grid(column = 0, row = 1,columnspan = 4, padx = 5, pady = 5, sticky= "ew")
    if edit_mode == 0:
        kw_action_configuration()

    kw_condition_options = ["No Condition", "Clock"]
    kw_condition_optionmenu = ctk.CTkOptionMenu(kf3, values= kw_condition_options, command= kw_condition_placeholder, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#eec643", button_color= "#eec643", button_hover_color= "#a3800f", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#eec643", font= customfont, dropdown_font= customfont)
    kw_condition_optionmenu.set("No Condition")
    kw_condition_optionmenu.grid(column = 0, row = 2, padx = 5, pady = 5)

    kw_condition = ctk.CTkEntry(kf3, placeholder_text="Condition",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", justify="center", font= customfont)
    kw_condition.grid(column = 1, row = 2, padx = 5, pady = 5)
    if edit_mode == 0:
        kw_condition_placeholder()

    if edit_mode == 0:
        kw_addindex = ctk.CTkEntry(kf3, placeholder_text="Where to Add", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
        kw_addindex.grid(column = 2, row = 2, padx = 5, pady = 5)

    kw_add = ctk.CTkButton(kf3, command= lambda: kw_set_operation(edit_mode = edit_mode, order = order, index = index), text="Add Operation", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", font= customfont)
    kw_add.grid(column = 4, row = 0, padx = 5, pady = 5)

    kw_validkeys = ctk.CTkButton(kf3, command= show_valid_keys, text="Valid Keys", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#2d3746", hover_color= "#192332", border_width= 2, border_color= "#5a64a0", text_color= "#e8e6e5", font= customfont)
    kw_validkeys.grid(column = 4, row = 1, padx = 5, pady = 5)

    
    if edit_mode == 1:
        keyboardwindow.title("Modify Mouse Operation")
        kw_action_optionmenu.set(order.action)
        kw_action_configuration()
        if kw_action_optionmenu.get() == "Press":
            kw_key1.insert(0,order.key1)
        elif kw_action_optionmenu.get() == "Hotkey":
            kw_key1.insert(0,order.key1)
            kw_key2.insert(0,order.key2)
            if order.key3 != None:
                kw_key3.insert(0,order.key3)
        elif kw_action_optionmenu.get() == "Write":
            kw_textentry.insert(0,order.write)
        kw_condition_optionmenu.set(order.condition_type)
        kw_condition.insert(0,order.condition)
        if kw_condition_optionmenu.get() == "No Condition":
            kw_condition.delete(0, ctk.END)
        kw_condition_placeholder()
        kw_add.configure(text="Confirm")
        
    keyboardwindow.after(200, lambda: keyboardwindow.iconbitmap(iconpic))
#--------------------------------------------------------------------------------------------------------------
def choose_window():
    if   operationmenu.get() == "Mouse":
        mouse_window()
    elif   operationmenu.get() == "Keyboard":
        keyboard_window()
    elif operationmenu.get() == "Time":
        time_window()
#--------------------------------------------------------------------------------------------------------------
        








#--------------------------------------------------------------------------------------------------------------
def time_window(edit_mode = 0, order = None, index = None):

    def tw_blink_color():
        tw_add.configure(border_color= "#00dd00")
        tw_add.after(200, lambda: tw_add.configure(border_color= "#ff6600"))

    def tw_condition_placeholder(*arg):
        if tw_condition_optionmenu.get() == "No Condition":
            tw_condition.delete(0, ctk.END)
            tw_condition.configure(placeholder_text = "Condition")
            tw_condition.after(5, lambda: tw_condition.configure(state = "disabled", border_color= "#808080"))
        elif tw_condition_optionmenu.get() == "Clock":
            tw_condition.configure(state = "normal", border_color= "#eec643")
            tw_condition.delete(0, ctk.END)
            tw_condition.after(5, lambda: tw_condition.configure(placeholder_text = "e.g. 23:59:59"))             
        timewindow.focus_set()
#--------------------------------------------------------------------------------------------------------------
    def tw_set_operation(edit_mode = 0, order = None, index = None):

        try:
            float(tw_seconds.get())
            if float(tw_seconds.get()) < 0:
                raise Exception
        except:
            tw_seconds.delete(0, ctk.END)
            tw_seconds.configure(placeholder_text = "Seconds")
            tw_seconds.configure(border_color= "#ee0000")
            timewindow.focus_set()
            return
        tw_seconds.configure(border_color= "#ff6600")

        if edit_mode == 0:
            if tw_addindex.get() != "":
                if tw_addindex.get().isdigit() == False:
                    tw_addindex.delete(0, ctk.END)
                    tw_addindex.configure(placeholder_text = "Where to Add")
                    tw_addindex.configure(border_color= "#ee0000")
                    timewindow.focus_set()
                    return
                if int(tw_addindex.get()) == 0 or int(tw_addindex.get()) > (int(len(orderlist)) + 1):
                    tw_addindex.delete(0, ctk.END)
                    tw_addindex.configure(placeholder_text = "Where to Add")
                    tw_addindex.configure(border_color= "#ee0000")
                    timewindow.focus_set()
                    return
            tw_addindex.configure(border_color= "#ff6600")

        if   tw_condition_optionmenu.get() == "No Condition":
            tw_condition.delete(0, ctk.END)
            tw_condition_placeholder()
            timewindow.focus_set()
        elif tw_condition_optionmenu.get() == "Clock":
            if re_search(tw_condition.get()) is True:
                pass
            else:
                tw_condition.delete(0, ctk.END)
                tw_condition_placeholder()
                tw_condition.configure(border_color= "#ee0000")
                timewindow.focus_set()
                return
        tw_condition.configure(border_color= "#eec643")

        if edit_mode == 1:
                       
            order.action = tw_action_optionmenu.get()
            order.seconds = float(tw_seconds.get())
            order.condition_type = tw_condition_optionmenu.get()
            order.condition = tw_condition.get()

            orderlist.pop(index)
            orderlist.insert(index, order)

            info = []
            for i in range (index + 1, listbox.size()):
                info.append(listbox.get(i))

            for i in range (listbox.size()-1, index-1, -1):
                listbox.delete(i)

            listbox.insert(index, f"{order.action}, {order.seconds} Second(s), {order.condition_type} {order.condition}")
            
            for i in info:
                listbox.insert("END", i)

        else:
            order = Time(action= tw_action_optionmenu.get() ,seconds= float(tw_seconds.get()), condition_type= tw_condition_optionmenu.get() ,condition= tw_condition.get())
            if tw_addindex.get() == "" or int(tw_addindex.get()) == len(orderlist) + 1:
                orderlist.append(order)
                listbox.insert("END", f"{order.action}, {order.seconds} Second(s), {order.condition_type} {order.condition}")
            else:
                index = int(tw_addindex.get()) - 1
                orderlist.insert(index, order)

                info = []
                for i in range (index, listbox.size()):
                    info.append(listbox.get(i))

                for i in range (listbox.size()-1, index-1, -1):
                    listbox.delete(i)

                listbox.insert("END", f"{order.action}, {order.seconds} Second(s), {order.condition_type} {order.condition}")
                
                for i in info:
                    listbox.insert("END", i)
           
        tw_seconds.delete(0, ctk.END)
        tw_seconds.configure(placeholder_text = "Seconds")
        tw_condition_optionmenu.set("No Condition")
        tw_condition.delete(0, ctk.END)
        tw_condition.configure(placeholder_text = "Condition")
        tw_condition_placeholder()
        timewindow.focus_set()

        if edit_mode == 1:
            timewindow.destroy()
        else:
            tw_blink_color()
#--------------------------------------------------------------------------------------------------------------
    timewindow = ctk.CTkToplevel(root)
    timewindow.title("Add Time Operation")
    timewindow.config(background = "#1e1e21")
    timewindow.iconbitmap(path.join(base_dir, "app_icon.ico"))
    timewindow.geometry(f"460x86+{int(pyautogui.size().width / 2) - int(460/2)}+{int(pyautogui.size().height / 2) - int(117/2)}")
    timewindow.resizable(False, False)
    timewindow.grab_set()

    tf1 = ctk.CTkFrame(timewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    tf1.grid(column = 0, row = 0, rowspan = 3, sticky= "nsew")

    tf2 = ctk.CTkFrame(timewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    tf2.grid(column = 1, row = 0, sticky= "nsew")

    tf3 = ctk.CTkFrame(timewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
    tf3.grid(column = 1, row = 1, sticky= "nsew")

    tf4 = ctk.CTkFrame(timewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    tf4.grid(column = 1, row = 2, sticky= "ew")

    tf5 = ctk.CTkFrame(timewindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    tf5.grid(column = 2, row = 0, rowspan = 3, sticky= "nsew")

    global child_window_ontop
    if child_window_ontop == 1:
        timewindow.attributes("-topmost", True)
    else:
        timewindow.attributes("-topmost", False)

    tw_actions = ["Delay"]
    tw_action_optionmenu = ctk.CTkOptionMenu(tf3, values= tw_actions, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#ff6600", button_color= "#ff6600", button_hover_color= "#b34700", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#ff6600", font= customfont, dropdown_font= customfont)
    tw_action_optionmenu.set("Delay")
    tw_action_optionmenu.grid(column = 0, row = 0, padx = 5, pady = 5)

    tw_seconds = ctk.CTkEntry(tf3, placeholder_text="Seconds",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
    tw_seconds.grid(column = 1, row = 0, padx = 5, pady = 5)

    tw_condition_options = ["No Condition", "Clock"]
    tw_condition_optionmenu = ctk.CTkOptionMenu(tf3, values= tw_condition_options, command= tw_condition_placeholder, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#eec643", button_color= "#eec643", button_hover_color= "#a3800f", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#eec643", font= customfont, dropdown_font= customfont)
    tw_condition_optionmenu.set("No Condition")
    tw_condition_optionmenu.grid(column = 0, row = 1, padx = 5, pady = 5)

    tw_condition = ctk.CTkEntry(tf3, placeholder_text="Condition",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", justify="center", font= customfont)
    tw_condition.grid(column = 1, row = 1, padx = 5, pady = 5)
    if edit_mode == 0:
        tw_condition_placeholder()

    if edit_mode == 0:
        tw_addindex = ctk.CTkEntry(tf3, placeholder_text="Where to Add", placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", justify="center", font= customfont)
        tw_addindex.grid(column = 2, row = 1, padx = 5, pady = 5)
    
    tw_add = ctk.CTkButton(tf3,command= lambda: tw_set_operation(edit_mode = edit_mode, order = order, index = index), text="Add Operation", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", font= customfont)
    tw_add.grid(column = 2, row = 0, padx = 5, pady = 5)

    if edit_mode == 1:
        timewindow.title("Modify Time Operation")
        tw_action_optionmenu.set(order.action)
        tw_seconds.insert(0,order.seconds)
        tw_condition_optionmenu.set(order.condition_type)
        tw_condition.insert(0, order.condition)
        if tw_condition_optionmenu.get() == "No Condition":
            tw_condition.delete(0, ctk.END)
        tw_condition_placeholder()
        tw_add.configure(text="Confirm")
    
    timewindow.after(200, lambda: timewindow.iconbitmap(iconpic))
#--------------------------------------------------------------------------------------------------------------










#--------------------------------------------------------------------------------------------------------------
def settings_window():
#--------------------------------------------------------------------------------------------------------------
    def sound_setting_set():
        global sound_setting
        sound_setting = soundswitch_var.get()

    def parent_window_ontop_set():
        global parent_window_ontop
        parent_window_ontop = parentontopwitch_var.get()

        if   parent_window_ontop == 1:
            root.attributes("-topmost", True)

        elif parent_window_ontop == 0:
            root.attributes("-topmost", False)
    
    def child_window_ontop_set():
        global child_window_ontop
        child_window_ontop = childontopwitch_var.get()
    
    def check_hotkey(*args):
        global trigger_key
        global trigger_key_pynput

        if triggerkeyentry.get() in valid_trigger_keys:
            trigger_key = triggerkeyentry.get()
            trigger_key_pynput = "Key." + triggerkeyentry.get()
            triggerkeyentry.configure(border_color= "#eec643")
        else:
            triggerkeyentry.configure(border_color= "#ee0000")
#--------------------------------------------------------------------------------------------------------------
    settingswindow = ctk.CTkToplevel(root)
    settingswindow.title("Settings")
    settingswindow.config(background = "#1e1e21")
    settingswindow.geometry(f"250x150+{int(pyautogui.size().width / 2) - int(250/2)}+{int(pyautogui.size().height / 2) - int(181/2)}")
    settingswindow.resizable(False, False)
    settingswindow.grab_set()

    sf1 = ctk.CTkFrame(settingswindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    sf1.grid(column = 0, row = 0, rowspan = 3, sticky= "nsew")

    sf2 = ctk.CTkFrame(settingswindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    sf2.grid(column = 1, row = 0, sticky= "nsew")

    sf3 = ctk.CTkFrame(settingswindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
    sf3.grid(column = 1, row = 1, sticky= "nsew")

    sf4 = ctk.CTkFrame(settingswindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
    sf4.grid(column = 1, row = 2, sticky= "ew")

    sf5 = ctk.CTkFrame(settingswindow, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5,  height= 50)
    sf5.grid(column = 2, row = 0, rowspan = 3, sticky= "nsew")

    global child_window_ontop
    if child_window_ontop == 1:
        settingswindow.attributes("-topmost", True)
    else:
        settingswindow.attributes("-topmost", False)

    soundswitch_var = ctk.IntVar(value= sound_setting)
    soundswitch = ctk.CTkSwitch(sf3, command= sound_setting_set, variable= soundswitch_var, onvalue= 1, offvalue= 0, text= "Sound", bg_color = "#1e1e21", fg_color = "#808080" , progress_color= "#ff6600", button_color= "#e8e6e5", button_hover_color= "#e8e6e5", font= customfont)
    soundswitch.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= "w")
    sound_setting_set()

    parentontopwitch_var = ctk.IntVar(value= parent_window_ontop)
    parentontopwitch = ctk.CTkSwitch(sf3, command= parent_window_ontop_set, variable= parentontopwitch_var, onvalue= 1, offvalue= 0, text= "Main window always on top", bg_color = "#1e1e21", fg_color = "#808080" , progress_color= "#ff6600", button_color= "#e8e6e5", button_hover_color= "#e8e6e5", font= customfont)
    parentontopwitch.grid(column = 0, row = 1, padx = 5, pady = 5, sticky= "w")
    parent_window_ontop_set()

    childontopwitch_var = ctk.IntVar(value= child_window_ontop)
    childontopwitch = ctk.CTkSwitch(sf3, command= child_window_ontop_set, variable= childontopwitch_var, onvalue= 1, offvalue= 0, text= "Secondary window always on top", bg_color = "#1e1e21", fg_color = "#808080" , progress_color= "#ff6600", button_color= "#e8e6e5", button_hover_color= "#e8e6e5", font= customfont)
    childontopwitch.grid(column = 0, row = 2, padx = 5, pady = 5, sticky= "w")
    child_window_ontop_set()

    triggerkeyentry = ctk.CTkEntry(sf3, placeholder_text="Hotkey",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", justify="center", font= customfont)
    triggerkeyentry.grid(column = 0, row = 3, padx = 5, pady = 5, sticky= "w")
    triggerkeyentry.bind("<KeyRelease>", check_hotkey)
    triggerkeyentry.insert(0, trigger_key)

    infolabel = ctk.CTkLabel(sf3, text= "Hotkey (f1-f12)", bg_color= "#1e1e21", fg_color = "#1e1e21", text_color= "#eec643", font= customfont)
    infolabel.grid(column = 0, row = 3, padx = 5, pady = 5, sticky= "e")

    #checkforkey = threading.Thread(target = check_hotkey)
    #threadslist.append(checkforkey)
    #checkforkey.start()

    settingswindow.after(200, lambda: settingswindow.iconbitmap(iconpic))
#--------------------------------------------------------------------------------------------------------------





#--------------------------------------------------------------------------------------------------------------
close = 0
orderlist=[]
threadslist = []
soundthreadslist = []
startthreadslist = []
keys = pyautogui.KEYBOARD_KEYS
for i in range (4):
    keys.pop(0)

getpos = 0
click_detected = False
repeatcount = 1
run = 0
trigger_wait = 0

valid_trigger_keys = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"]

try:
    with open((path.join(base_dir, "Settings", "settings.json")), "r") as file:
        settingsdict = json.load(file)
    trigger_key = settingsdict["trigger_key"]
    if trigger_key not in valid_trigger_keys:
        raise Exception
    trigger_key_pynput = settingsdict["trigger_key_pynput"]
    if trigger_key_pynput != ("Key."+trigger_key):
        raise Exception
    sound_setting = int(settingsdict["sound_setting"])
    if sound_setting != 0 and sound_setting != 1:
        raise Exception
    parent_window_ontop = int(settingsdict["parent_window_ontop"])
    if parent_window_ontop != 0 and parent_window_ontop != 1:
        raise Exception
    child_window_ontop = int(settingsdict["child_window_ontop"])
    if child_window_ontop != 0 and child_window_ontop != 1:
        raise Exception
except:
    trigger_key = "f8"
    trigger_key_pynput = "Key.f8"
    sound_setting = 1
    parent_window_ontop = 1
    child_window_ontop = 1

if parent_window_ontop == 1:
    root.attributes("-topmost", True)
#--------------------------------------------------------------------------------------------------------------
f1 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5)
f1.grid(column = 0, row = 0, rowspan = 2, sticky= "nsew")

f2 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77",height = 60)
f2.grid(column = 1, row = 0, sticky= "nsew")

f3 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
f3.grid(column = 1, row = 1, sticky= "nsew")

f4 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77")
f4.grid(column = 2, row = 0, rowspan = 2, sticky= "nsew")

f5 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", width = 5)
f5.grid(column = 3, row = 0, rowspan = 2, sticky= "nsew")

f6 = ctk.CTkFrame(root, corner_radius= 0, bg_color= "#1e1e21", fg_color= "#1e1e21", border_width = 0, border_color= "#00ff77", height = 5)
f6.grid(column = 0, row = 2, columnspan = 4, sticky= "nsew")
#--------------------------------------------------------------------------------------------------------------
listbox = ctkl.CTkListbox(f4, width= 350, height = 170, bg_color= "#1e1e21", fg_color = "#1e1e21", hover_color= "#606060", text_color= "#e8e6e5", button_color= "#323235", highlight_color= "#5a64a0", border_width= 2, border_color= "#5a64a0", corner_radius= 14, scrollbar_button_color= "#5a64a0", scrollbar_button_hover_color = "#5a64a0", font= customfont)
listbox.grid(column = 2, row = 0,rowspan= 4, padx = 5, pady = 5, sticky= "nsew")

logopic = ctk.CTkImage(Image.open(path.join(base_dir, "Assets", "simpleautomator.png")), size=(210, 50))
labellogo = ctk.CTkLabel(master=f2, image = logopic, text= None, width= 230, height= 60, bg_color= "#1e1e21", fg_color = "#1e1e21")
labellogo.grid(column = 1, row = 0, padx = 0, pady = 0, sticky= "e")

settingbuttom_icon = ctk.CTkImage(Image.open(path.join(base_dir, "Assets", "settings.png")), size=(17, 17))
settingbuttom = ctk.CTkButton(master=f2, command= settings_window, image= settingbuttom_icon, text= None, bg_color= "#1e1e21", fg_color = "#1e1e21", hover_color= "#323235", width= 8, height= 8, font= customfont)
settingbuttom.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= "nw")

helpbuttom_icon = ctk.CTkImage(Image.open(path.join(base_dir, "Assets", "help.png")), size=(17, 17))
helpbuttom = ctk.CTkButton(master=f2, command= helpdialogue.help_window, image= helpbuttom_icon, text= None, bg_color= "#1e1e21", fg_color = "#1e1e21", hover_color= "#323235", width= 8, height= 8, font= customfont)
helpbuttom.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= "sw")

operationmenu_options = ["Mouse", "Keyboard", "Time"]
operationmenu = ctk.CTkOptionMenu(f3, values= operationmenu_options, corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#ff6600", button_color= "#ff6600", button_hover_color= "#b34700", text_color= "#1e1e21", dropdown_fg_color= "#1e1e21", dropdown_hover_color="#323235", dropdown_text_color="#ff6600", text_color_disabled= "#3c3c35", font= customfont, dropdown_font= customfont)
operationmenu.set("Mouse")
operationmenu.grid(column = 0, row = 0, padx = 5, pady = 5)

addbutton = ctk.CTkButton(f3, command= choose_window, text= "Add Operation", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", text_color_disabled= "#808080", font= customfont)
addbutton.grid(column = 1, row = 0, padx = 5, pady = 5)

editbutton = ctk.CTkButton(f3, command= edit_operation, text= "Edit", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", text_color_disabled= "#808080", font= customfont)
editbutton.grid(column = 0, row = 1, padx = 5, pady = 5)

deletebutton = ctk.CTkButton(f3, command= delete_operation, text= "Delete", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#463735", hover_color= "#322321", border_width= 2, border_color= "#ff6600", text_color= "#e8e6e5", text_color_disabled= "#808080", font= customfont)
deletebutton.grid(column = 1, row = 1, padx = 5, pady = 5)

loopcountentry = ctk.CTkEntry(f3, placeholder_text="Number of Loops",placeholder_text_color= "#808080", corner_radius= 30, bg_color= "#1e1e21", fg_color = "#323235", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", justify="center", font= customfont)
loopcountentry.grid(column = 0, row = 2, padx = 5, pady = 5)
loopcountentry.insert(0, 1)

startbutton = ctk.CTkButton(f3,command= startloop_set, text= "Start", corner_radius= 30, anchor="center", bg_color= "#1e1e21", fg_color = "#3c3c35", hover_color= "#2b2b21", border_width= 2, border_color= "#eec643", text_color= "#e8e6e5", text_color_disabled= "#808080", font= customfont)
startbutton.grid(column = 1, row = 2, padx = 5, pady = 5)

labelround = ctk.CTkLabel(f3, text= "", bg_color= "#1e1e21", fg_color = "#1e1e21", text_color= "#eec643", font= customfont)
labelround.grid(column = 0, row = 3, padx = 5, pady = 5)

labelorder = ctk.CTkLabel(f3, text= "", bg_color= "#1e1e21", fg_color = "#1e1e21", text_color= "#ff6600", font= customfont)
labelorder.grid(column = 1, row = 3, padx = 5, pady = 5)
#--------------------------------------------------------------------------------------------------------------
start_stop_listener = threading.Thread(target=start_stop_hotkey)
start_stop_listener.start()
threadslist.append(start_stop_listener)
#--------------------------------------------------------------------------------------------------------------





#--------------------------------------------------------------------------------------------------------------
root.bind("<Destroy>", on_destroy)
root.mainloop()

pyautogui.press(trigger_key)

settingsdict = {"trigger_key": trigger_key,
    "trigger_key_pynput": trigger_key_pynput,
    "sound_setting": str(sound_setting),
    "parent_window_ontop": str(parent_window_ontop),
    "child_window_ontop": str(child_window_ontop)}

with open((path.join(base_dir, "Settings", "settings.json")), "w") as file:
    json.dump(settingsdict, file, indent= 4)

for thread in threadslist:
    try:
        thread.join()
    except:
        pass

for thread in soundthreadslist:
    try:
        thread.join()
    except:
        pass

for thread in startthreadslist:
    try:
        thread.join()
    except:
        pass