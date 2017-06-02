# tkinter GUI library

import tkinter as tk
from tkinter import font

# date time library used for clock and time durations
from datetime import datetime, timedelta

# OS library for accessing os functions
import os

# Config global variables
from lib import Config

class UICommon():
    # common images used with the application

    system_path = ""

    # Common functions related to the UI

    click_start_time = datetime.now()
    cursor_start_position = 0
    root_frame = None
    numeric_keypad_frame = None
    numeric_keypad_value = ""
    numeric_keypad_display = None
    numeric_keypad_target = None


    def __init__(self, root = None):
        self.root_frame = root
        self.system_path = os.path.dirname(os.path.abspath(__file__)).replace("lib", "") + "graphics/"



    def clear_frame(self, frame):
        #
        # clears all of the children from a frame
        #
        for widget in frame.winfo_children():
            widget.destroy()

    def table(self, master, title, content, target=None, backgroundcolour="White", foregroundcolour="black", bordercolour="grey", borderwidth=1, fontstyle="DejaVuSans 18 normal"):
        # creates a table from a 2 dimensional array.  
        # master: = this represents the parent window
        # content: a 2 dimensional array containing the table contents
        # First column in the array must be the row id which is returned on a click event.  This will not be displayed in the table
        index = 0
        for i in range(len(content)): #Rows
            for j in range(len(content[i])):
                if j==0: 
                    index = content[i][j]
                else:
                    b = tk.Label(master, text=str(content[i][j]), background=backgroundcolour, foreground=foregroundcolour,padx=5, pady=10, highlightthickness=borderwidth, highlightbackground=bordercolour, font=fontstyle)
                    if (target is not None):
                        b.bind('<ButtonPress-1>', self.__row_pressed)  
                        b.bind('<ButtonRelease-1>', lambda event, arg1=index, arg2=target: self.__row_released(event, arg1, arg2))                 
                    b.grid(row=i, column=j-1, sticky=tk.N+tk.S+tk.E+tk.W)
        return

    def __row_pressed(self, event):
        #
        # detects a press event by starting a timer and saving the current position
        #
        self.click_start_time = datetime.now()
        self.cursor_start_position = self.root_frame.winfo_pointery()
    
    def __row_released(self, event, index, target):
        #
        # check if the mouse has been moved more than 5 pixels
        #
        x = self.root_frame.winfo_pointery() - self.cursor_start_position
        if (x > -5) and (x < 5): # mouse has moved less than 5 pixels so detect it as a click
            # check the amount of time that has passed since the press started
            duration = datetime.now() - self.click_start_time
            if (duration < timedelta(seconds=1)): # less than 1 second has passed so detect as click instead of hold
                target(index)

    def table_column_weighs(self, target, columns, minsize=None):
        #
        # set the column weights and minimum size for a grid
        #
        for i in range(len(columns)):
            if (minsize == None):
                target.columnconfigure(i, weight= columns[i])
            else:
                target.columnconfigure(i, weight= columns[i], minsize=minsize[i])

    def table_cell(self, cellframe = None, celltext = None, image=None, wraplength=0, justify=tk.LEFT, row=0, column=0, rowspan=1, columnspan=1, sticky=tk.N+tk.S+tk.E+tk.W):
        #
        # create a table cell frame and label and add it to a grid
        #
        cell = tk.Frame(cellframe, bg=Config.style_row_background_colour, highlightthickness=Config.style_row_border_width, highlightbackground=Config.style_row_border_colour)
        label = tk.Label(cell, text=celltext,wraplength=wraplength, image=image, justify=justify,background=Config.style_row_background_colour, foreground=Config.style_row_foreground_colour, padx=5, pady=10,  font=Config.style_row_font)
        label.pack(side=tk.LEFT, fill=tk.Y)
        cell.grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan)
        return cell

    def table_title(self, cellframe, celltext, wraplength=0, justify=tk.LEFT, row=0, column=0, rowspan=1, columnspan=1, sticky=tk.N+tk.S+tk.E+tk.W):
        #
        # create a table title frame and label and add it to a grid
        #
        cell = tk.Frame(cellframe, bg=Config.style_header_background_colour, highlightthickness=Config.style_header_border_width, highlightbackground=Config.style_header_border_colour)
        label = tk.Label(cell, text=celltext,wraplength=wraplength, justify=justify,background=Config.style_header_background_colour, foreground=Config.style_header_foreground_colour, padx=5, pady=10,  font=Config.style_row_font)
        label.pack(side=tk.LEFT, fill=tk.Y)
        cell.grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan)
        return cell

    def bind_children(self, widget, event, callback, add=""):
        #
        # bind the event to a widget and all of its children
        #
        widget.bind(event, callback, add)

        for child in widget.children.values():
            self.bind_children(child, event, callback)

    def barcode_type(self, barcode):
        #
        # parse the barcode to check whether it is an order, product or unknown part  
        #       
        if (str(barcode).startswith("99")): # barcode is an order
            return("order")
        elif (str(barcode).startswith("742678787")): # barcode is a product
            return("product")
        else:  # barcode is not an internal code.
            return("unknown")

    def message_box(self, master, title, content, target=None):
        #
        # replaces the standard tkinter message box
        #
        box = tk.Frame(master, highlightbackground="grey", highlightcolor="grey", highlightthickness=1, background="#FFFFFF")
        tk.Label(box, text=title, font="DejaVuSans 22 bold", background="#FFFFFF", pady=20).pack()
        tk.Label(box, text=content, font="DejaVuSans 22 normal", background="#FFFFFF", pady=30).pack()
        tk.Button(box, text="Close", font="DejaVuSans 28 normal",pady=20, command=lambda arg1=box, arg2=target: self.__message_box_close(arg1, arg2)).pack(side = tk.BOTTOM, fill=tk.X)
        box.place(x = 20, y=100, width=280)

    def __message_box_close(self, master, target):
        #
        # Closes and destroys the message box frame and calls a target function if there is one
        #
        master.place_forget()
        master.destroy()
        if (target != None):
            target()

    def numeric_keypad(self, master=None, target=None, title="Quanitity", value=None):
        #
        # draws a numeric keypad on the display
        #        

        # save the return target
        self.numeric_keypad_target = target

        if (value == None):
            self.numeric_keypad_value = ""
        else:
            self.numeric_keypad_value = str(value)
        
        # master frame
        self.numeric_keypad_frame = tk.Frame(master, width=320, height=480, background="#000000")
        self.numeric_keypad_frame.place(x=0, y=0, width=320, height=480)
        # title
        tk.Label(self.numeric_keypad_frame, text=title, font="DejaVuSans 22 normal", background="#000000", foreground="#FFFFFF", pady=5).pack(side = tk.TOP,fill=tk.X)
        # display label
        self.numeric_keypad_display = tk.Label(self.numeric_keypad_frame, text=self.numeric_keypad_value, font="DejaVuSans 50 normal", background="#FFFFFF", pady=10)
        self.numeric_keypad_display.pack(side = tk.TOP,fill=tk.X)
        # number grid
        numbergrid = tk.Frame(self.numeric_keypad_frame, width=320, height=320)
        x = 0
        y = 0

        for i in range(1, 10):
            label = tk.Label(numbergrid, text=str(10-i), font="DejaVuSans 50 normal", background="#333333", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000", pady=20)
            self.bind_children(label, '<ButtonRelease-1>', lambda event, arg1=10-i: self.__numeric_keypad_update(arg1))
            label.grid(row=y, column=x, sticky=tk.N+tk.S+tk.E+tk.W)
            x+=1
            if (x >= 3):
                y+=1
                x=0        

        number0 = tk.Label(numbergrid, text="0", font="DejaVuSans 50 normal", background="#333333", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000")
        self.bind_children(number0, '<ButtonRelease-1>', lambda event, arg1=0: self.__numeric_keypad_update(arg1))
        number0.grid(row=3, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        delete = tk.Label(numbergrid, text="<", font="DejaVuSans 50 normal", background="#333333", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000", pady=20)
        self.bind_children(delete, '<ButtonRelease-1>', self.__numeric_keypad_delete)
        delete.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        decimal = tk.Label(numbergrid, text=".", font="DejaVuSans 50 normal", background="#333333", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000")
        self.bind_children(decimal, '<ButtonRelease-1>', lambda event, arg1=".": self.__numeric_keypad_update(arg1))
        decimal.grid(row=3, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        save = tk.Label(numbergrid, text="Enter", font="DejaVuSans 20 normal", background="#29a329", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000")
        self.bind_children(save, '<ButtonRelease-1>', lambda event, arg1=0: self.__numeric_keypad_save(arg1))
        save.grid(row=1, column=3, sticky=tk.N+tk.S+tk.E+tk.W, rowspan=3)

        cancel = tk.Label(numbergrid, text="Cancel", font="DejaVuSans 20 normal", background="#b30000", foreground="#FFFFFF", highlightthickness=1, highlightbackground="#000000")
        self.bind_children(cancel, '<ButtonRelease-1>', lambda event, arg1=0: self.__numeric_keypad_cancel(arg1))
        cancel.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        numbergrid.place(x=0, y=110, width=320, height=370)
        self.table_column_weighs(numbergrid, [1,1,1,1], minsize=[78,78,78,78])


    def __numeric_keypad_update(self, value):
        #
        # append the selelected number or character to the keypad string
        #
        if (value == "."): # check if a decimal point already exists before adding one
            if (self.numeric_keypad_value.find(".")==-1):
                self.numeric_keypad_value += "."
        else:
            if (self.numeric_keypad_value == ""):
                if (value > 0):
                    self.numeric_keypad_value = str(value)
                    
            else:
                self.numeric_keypad_value += str(value)
        self.numeric_keypad_display.configure(text=str(self.numeric_keypad_value))

    def __numeric_keypad_delete(self, value):
        #
        # remove the last character from the keypad value
        #
        if (len(self.numeric_keypad_value) > 0):
            self.numeric_keypad_value = self.numeric_keypad_value[:-1]
            self.numeric_keypad_display.configure(text=str(self.numeric_keypad_value))
        return

    def __numeric_keypad_save(self, value):
        #
        # call the target function and return the value in float or int depending on a decimal point
        #

        # clear the frame
        if (self.numeric_keypad_frame != None):
            self.numeric_keypad_frame.destroy()


        if (self.numeric_keypad_target != None):
            # convert into an int or float and return the value
            if (self.numeric_keypad_value.find(".")==-1):
                self.numeric_keypad_target(int(self.numeric_keypad_value))
            else:
                self.numeric_keypad_target(float(self.numeric_keypad_value))

        return


    def __numeric_keypad_cancel(self, value):
        #
        # clear the contents of numeric_keypad_value and remove the frame
        #
        self.numeric_keypad_value = ""
        if (self.numeric_keypad_frame != None):
            self.numeric_keypad_frame.destroy()

        if (self.numeric_keypad_target != None):
            self.numeric_keypad_target(None)

        return
