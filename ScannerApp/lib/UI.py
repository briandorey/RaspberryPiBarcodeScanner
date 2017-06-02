# Threading library for timer events
import time, threading

# OS library for accessing os functions
import os

# tkinter GUI library
import tkinter as tk
from tkinter import messagebox

# date time library used for clock and time durations
from datetime import datetime, timedelta

# Python Imaging Library
from PIL import ImageTk, Image

# Hardware library for accessing scanner hardware
from lib import Hardware

# NetworkComms library for all network communications

from lib import NetworkComms

# UI functions common across all libraries
from lib import UICommon

# Functions related to orders
from lib import Orders

# Functions related to Products
from lib import Products

# Functions related to Parts
from lib import Parts

# Config global variables
from lib import Config


class UI():


    #region Variable and Object decloration

    root = tk.Tk()
    system_path = ""
       
    # UI component objects  

    # titlebar objects
    title_frame = tk.Frame()
    clock_label = tk.Label()
    power_label = tk.Label()
    power_icon = tk.Label()
    wifi_icon = tk.Label()
    
    wifi_status = 0 
    wifi_image = ImageTk.PhotoImage(Image.new("RGB", (25, 25), "black"))
    battery_status = 0
    battery_image = ImageTk.PhotoImage(Image.new("RGB", (25, 25), "black"))
    
    #tab bar objects
    tabbar_frame = tk.Frame()
    orders_button = tk.Label()
    products_button = tk.Label()
    parts_button = tk.Label()
    power_button = tk.Label()
    power_dialog = tk.Frame()
    ordersicon = ImageTk.PhotoImage(Image.new("RGB", (90, 50), "black"))
    productsicon = ImageTk.PhotoImage(Image.new("RGB", (90, 50), "black"))
    partsicon = ImageTk.PhotoImage(Image.new("RGB", (90, 50), "black"))

    #content objects
    content_frame = tk.Frame()
    content_scroll_frame = tk.Frame()
    
    #content variables
    cursor_start_position = 0    
    frame_start_position = 0

    frame_end_position = 0
    scroll_enabled = False
    is_scrolling = False

    current_tab = "orders"

    #footer objects
    footer_frame = tk.Frame()

    # object initialisation

    hardware = Hardware.Hardware()
    uicommon = UICommon.UICommon(root)
    communication = NetworkComms.Communication()
    orders = Orders.Orders(root, content_scroll_frame)
    products = Products.Products(root, content_scroll_frame)
    parts = Parts.Parts(root, content_scroll_frame)


    def __init__(self):
        #
        # UI Class initialisation
        #
       
        # set the root frame to open full screen with cursor disabled
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.config(cursor='none')

        # start timer to update the titlebar
        self.root.after(1000, self.__titlebar_update_event)       
        
        # initialse the UI
        self.__init_ui()

        # check if there is a network connection

        if (self.communication.ping("google.com")):
            Config.network_status = True            
        else:
            self.uicommon.message_box(self.root, "Communication Error", "No network connection")
        

        # set the orders tab to be active and get the latest orders
        self.__orders_tab_clicked()

        # run the main UI loop
        self.root.mainloop()

    #endregion

    #region UI initialisation

    def __init_ui(self):
        #
        # initialise the primary UI elements
        #

        self.system_path = os.path.dirname(os.path.abspath(__file__)).replace("lib", "") + "graphics/"
        #self.root.pack(fill=tk.BOTH, expand=1)

        # initialise the title bar objects
        self.title_frame = tk.Frame(self.root, height=25, width=320, background="black" )
        self.title_frame.pack_propagate(0)
        self.title_frame.pack(fill=tk.X)

        self.clock_label = tk.Label(self.title_frame, text="00:00 01:01:2000", background="black", foreground="white")
        self.clock_label.place(x=3, y=3)

        self.wifi_icon = tk.Label(self.title_frame, image=self.wifi_image, borderwidth=0)
        self.wifi_icon.place(x=200, y=0)
       
        self.power_icon = tk.Label(self.title_frame, image=self.battery_image, borderwidth=0)
        self.power_icon.place(x=255, y=0)
        
        self.power_label = tk.Label(self.title_frame, text="", background="black", foreground="white")
        self.power_label.place(x=280, y=3)

        # initialise the tab bar objects
        self.tabbar_frame = tk.Frame(self.root, height=50, width=320, background="grey" )   
        self.tabbar_frame.pack_propagate(0)     
        self.tabbar_frame.pack(fill=tk.X)
        
        # initialise the orders tab button
        self.ordersicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-orders.bmp"))
        self.orders_button = tk.Button(self.tabbar_frame, width=88, height=50, image=self.ordersicon,borderwidth=0, highlightthickness=0, command=self.__orders_tab_clicked)
        self.orders_button.image = self.ordersicon
        self.orders_button.grid(row=0, column=0)
        
        # initialise the products tab button
        self.productsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-products.bmp"))
        self.products_button = tk.Button(self.tabbar_frame, width=88, height=50, image=self.productsicon,borderwidth=0, highlightthickness=0, command=self.__products_tab_clicked)
        self.products_button.image = self.productsicon
        self.products_button.grid(row=0, column=1)

        # initialise the parts tab button
        self.partsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-parts.bmp"))
        self.parts_button = tk.Button(self.tabbar_frame, width=88, height=50, image=self.partsicon,borderwidth=0, highlightthickness=0, command=self.__parts_tab_clicked)
        self.parts_button.image = self.partsicon
        self.parts_button.grid(row=0, column=2)
        
        # initialise the power tab button
        power_icon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-power.bmp"))
        self.power_button = tk.Button(self.tabbar_frame, width=50, height=50, image=power_icon,borderwidth=0, highlightthickness=0, command=self.__power_tab_clicked)
        self.power_button.image = power_icon
        self.power_button.grid(row=0, column=3)

        # initialise the content frame objects
        self.content_frame = tk.Frame(self.root, height=330, width=320, background="white" )  
        self.content_frame.pack_propagate(0)      
        self.content_frame.pack(fill=tk.X)

        # initialise the content scroll frame
        self.content_scroll_frame = tk.Frame(self.content_frame)
        self.content_scroll_frame.place(x=0, y=0, width=320)
        #self.orders.orders_list(self.content_scroll_frame)
    
        # initialise the footer bar objects
        self.footer_frame = tk.Frame(self.root, height=75, width=320, background="green" )  
        self.footer_frame.pack_propagate(0)      
        self.footer_frame.pack(fill=tk.X)

        self.scan_button = tk.Button(self.footer_frame,  height=75, width=320, font="DejaVuSans 36 normal", foreground="white", activeforeground="white", background="#7cbc0a",activebackground="#7cbc0a", text="SCAN", command=self.__scan_barcode)
        self.scan_button.pack(fill=tk.BOTH, expand=True) 

        # add the button events for content scrolling
        self.root.bind('<ButtonPress-1>', self.__scroll_start) 
        self.root.bind('<ButtonRelease-1>', self.__scroll_end)

        #endregion

    #region primary UI events

    def __scan_barcode(self):
        #
        #   Calls the barcode scanner hardware and processes the returned barcode
        #
        print("scanning")
        barcode = self.hardware.scan()
        print(barcode)
        code_type = self.uicommon.barcode_type(barcode)
        print(code_type)

        # Parse barcode
        if (Config.scanning_mode == 0): # default mode
            if (code_type == "order"):
                self.__select_tab_from_barcode("orders")
                self.orders.process_barcode(barcode, frame=self.content_scroll_frame)
            elif (code_type == "product"):
                self.__select_tab_from_barcode("products")
                self.products.process_barcode(barcode, frame=self.content_scroll_frame)
            else:
                self.parts.process_barcode(barcode)

        elif (Config.scanning_mode == 1): # orders mode
            if (code_type == "order"):
                self.__select_tab_from_barcode("orders")
                self.orders.process_barcode(barcode, frame=self.content_scroll_frame)
            elif (code_type == "product"):
                self.__select_tab_from_barcode("orders")
                self.orders.process_product_barcode(barcode, frame=self.content_scroll_frame)
            else:
                self.uicommon.message_box(self.root, "Error", "Unknown Barcode")

        elif (Config.scanning_mode == 2): # product mode
            if (code_type == "order"):
                self.uicommon.message_box(self.root, "Error", "Not a product barcode")
            elif (code_type == "product"):
                self.__select_tab_from_barcode("products")
                self.products.process_barcode(barcode, frame=self.content_scroll_frame)
            else:
                self.uicommon.message_box(self.root, "Error", "Unknown Barcode")

        elif (Config.scanning_mode == 3): # parts mode
            if (code_type == "order"):
                self.uicommon.message_box(self.root, "Error", "Not a parts barcode")
            elif (code_type == "product"):
                self.uicommon.message_box(self.root, "Error", "Not a parts barcode")
            else:
                self.__select_tab_from_barcode("parts")
                self.parts.process_barcode(barcode, frame=self.content_scroll_frame)
        else: # orders mode
            self.uicommon.message_box(self.root, "Error", "Unknown System Mode")

    def __titlebar_update_event(self):
        #
        #   Update the UI elements in the title bar
        #

        # update titlebar clock
        self.clock_label.config(text=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        # get the wifi status
        wifi_strength = int(self.hardware.get_wifi_strength())

        # update the wifi icon if the value has changed beyond the current range
        if (wifi_strength == 0) and (self.wifi_status != 0):
            self.wifi_status = 0
            self.wifi_image = ImageTk.PhotoImage(Image.open(self.system_path + "wifi0.bmp"))
            self.wifi_icon.config(image = self.wifi_image)
        elif (wifi_strength > 0) and (wifi_strength < 17) and (self.wifi_status != 1):
            self.wifi_status = 1
            self.wifi_image = ImageTk.PhotoImage(Image.open(self.system_path + "wifi1.bmp"))
            self.wifi_icon.config(image = self.wifi_image)
        elif (wifi_strength >= 17) and (wifi_strength < 35) and (self.wifi_status != 2):
            self.wifi_status = 2
            self.wifi_image = ImageTk.PhotoImage(Image.open(self.system_path + "wifi2.bmp"))
            self.wifi_icon.config(image = self.wifi_image)
        elif (wifi_strength >= 35) and (wifi_strength < 52) and (self.wifi_status != 3):
            self.wifi_status = 3
            self.wifi_image = ImageTk.PhotoImage(Image.open(self.system_path + "wifi3.bmp"))
            self.wifi_icon.config(image = self.wifi_image)
        elif (wifi_strength >= 52) and (self.wifi_status != 4):
            self.wifi_status = 4
            self.wifi_image = ImageTk.PhotoImage(Image.open(self.system_path + "wifi4.bmp"))
            self.wifi_icon.config(image = self.wifi_image)

        # get the power status
        current_power_level = self.hardware.get_battery_level()
        s = str(current_power_level) + "%"
        self.power_label.config(text=s)
        int_current_power_level = int(int(current_power_level) / 10)
        if self.battery_status != int_current_power_level:
            self.battery_status = int_current_power_level
            self.battery_image = ImageTk.PhotoImage(Image.open(self.system_path + "battery" + str(self.battery_status) + ".bmp"))
            self.power_icon.config(image = self.battery_image)

        # reset the timer to trigger in 1 second
        self.root.after(1000, self.__titlebar_update_event)

    #region touch scroll functions

    def __scroll_start(self, event):
        #
        #   Start the scroll event
        #
        self.is_scrolling = True
        self.cursor_start_position = self.root.winfo_pointery()
        self.frame_start_position = self.content_scroll_frame.winfo_y()
        self.click_start_time = datetime.now()
        threading.Timer(0.01, self.__scroll_event).start()
        return

    def __scroll_end(self, event):
        #
        #   End the scroll event
        #        
        self.is_scrolling = False

    def __scroll_event(self):
        #
        #   Update the scroll frame position based on the touch location
        #
        if (self.is_scrolling):               
            ypos = (self.root.winfo_pointery() - self.cursor_start_position) + self.frame_start_position
            max = 0 - self.content_scroll_frame.winfo_height() + self.content_frame.winfo_height()
            if (ypos < 0) and (ypos > max):
                self.content_scroll_frame.place(y = ypos)
            if (ypos > 0):
                self.content_scroll_frame.place(y = 0)
            threading.Timer(0.03, self.__scroll_event).start()

    

    #endregion

    #region tab bar events

    def __select_tab_from_barcode(self, section):
        #
        # Updates the tab bar from the barcode scan function
        #

        if (section == "orders") and (self.current_tab != "orders"):
            self.__orders_tab_clicked(from_barcode = True)
        elif (section == "products") and (self.current_tab != "products"):
            self.__products_tab_clicked(from_barcode = True)
        elif (section == "parts") and (self.current_tab != "parts"):
            self.__parts_tab_clicked(from_barcode = True)


    def __orders_tab_clicked(self, from_barcode = False):
        #
        # Orders tab click event
        #

        self.current_tab = "orders"

        # update the images in the tab bar to show the selected tab
        self.ordersicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-orders-selected.bmp"))
        self.orders_button.config(image = self.ordersicon)

        self.productsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-products.bmp"))
        self.products_button.config(image = self.productsicon)

        self.partsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-parts.bmp"))
        self.parts_button.config(image = self.partsicon)
       
        # clear any content from the content_scroll_frame and get a list of the current orders
        self.uicommon.clear_frame(self.content_scroll_frame)
        if (not from_barcode):
            self.orders.orders_list(self.content_scroll_frame)
         
        return()
 
    
    def __products_tab_clicked(self, from_barcode = False):
        #
        # Products tab click events
        #

        self.current_tab = "products"

        # update the images in the tab bar to show the selected tab
        self.ordersicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-orders.bmp"))
        self.orders_button.config(image = self.ordersicon)

        self.productsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-products-selected.bmp"))
        self.products_button.config(image = self.productsicon)

        self.partsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-parts.bmp"))
        self.parts_button.config(image = self.partsicon)

        # clear any content from the content_scroll_frame and get a list of the products
        self.uicommon.clear_frame(self.content_scroll_frame)
        if (not from_barcode):
            self.products.products_list(self.content_scroll_frame)
        
        return()


    def __parts_tab_clicked(self, from_barcode = False):
        #
        # Parts tab click event
        #

        self.current_tab = "parts"

        # update the images in the tab bar to show the selected tab
        self.ordersicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-orders.bmp"))
        self.orders_button.config(image = self.ordersicon)

        self.productsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-products.bmp"))
        self.products_button.config(image = self.productsicon)

        self.partsicon = ImageTk.PhotoImage(Image.open(self.system_path + "tabbar-parts-selected.bmp"))
        self.parts_button.config(image = self.partsicon)

        # clear any content from the content_scroll_frame and get a list of the parts
        self.uicommon.clear_frame(self.content_scroll_frame)
        if (not from_barcode):
            self.parts.parts_list(self.content_scroll_frame)
        
        return()


    def __power_tab_clicked(self):
        #
        # Power tab click events: show the overlay for shutdown, restart, exit...
        #

        # create overlay frame
        self.power_dialog = tk.Frame(self.root, width=320, height=480, background="grey")
        self.power_dialog.place(x=0, y=0, width=320, height=480)

        # title
        power_title = tk.Label(self.power_dialog, text="Options", font="DejaVuSans 36 normal", background="grey", foreground="white")
        power_title.pack(fill=tk.X, expand=1)
        
        # shutdown button
        power_shutdown_button = tk.Button(self.power_dialog, text="Shutdown", height=2, font="DejaVuSans 32 normal", command=self.hardware.shutdown)
        power_shutdown_button.pack(fill=tk.X)
        
        # restart button
        power_restart_button = tk.Button(self.power_dialog, text="Restart", height=2,font="DejaVuSans 32 normal", command=self.hardware.restart)
        power_restart_button.pack(fill=tk.X)
        # exit application button
        power_exit_button = tk.Button(self.power_dialog, text="Exit Application", height=2,font="DejaVuSans 32 normal", command=exit)
        power_exit_button.pack(fill=tk.X)
        # cancel button
        power_cancel_button = tk.Button(self.power_dialog, text="Cancel", height=2,font="DejaVuSans 32 normal", command=self.close_power_dialog)
        power_cancel_button.pack(fill=tk.BOTH)

        return()

    def close_power_dialog(self):
        self.power_dialog.place_forget()
        self.power_dialog.destroy()

    #endregion

    
