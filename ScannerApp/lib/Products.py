# tkinter GUI library
import tkinter as tk

# date time library used for clock and time durations
from datetime import datetime, timedelta

# xml parser

from xml.dom import minidom
from xml.etree import ElementTree

# Python Imaging Library
from PIL import ImageTk, Image

# communication library used for all network activity

from lib import NetworkComms

# common ui elements

from lib import UICommon

# Config global variables
from lib import Config

# object classes
from lib import Objects

class Products():
    
    comms = NetworkComms.Communication()
    uicommon = UICommon.UICommon()    

    click_start_time = datetime.now() # used for detecting a click or scroll
    cursor_start_position = 0

    products_array = [] # stores the list of products
    options_array = [] # stores the options within a single product

    current_product = Objects.objProduct()
    current_option = Objects.objProductOption()

    selected_option = None

    root_frame = None
    parent_frame = None # the scroll frame
    optionlist_frame = None # used within the order details frame to list items

    def __init__(self, root, master):
        #
        # Initialise the products class
        #
        self.root_frame = root
        self.parent_frame = master
        self.uicommon.root_frame = self.root_frame


    def process_barcode(self, barcode, frame=None):
        #
        # get the product details from the barcode
        #

        if (frame != None):
            self.parent_frame = frame

        self.__product_details(barcode = barcode)
       
        return

    def products_list(self, frame):
        #
        # Fetches and displays a list of the active products
        #

        self.parent_frame = frame

        # set the scanning mode to default
        Config.scanning_mode = 0

        # clear the contents of the parent frame
        self.uicommon.clear_frame(self.parent_frame)

        # get the xml product list from the server and check that xml data was received
        product_data = self.comms.get_product_list()
        if (product_data != None):
            # parse the xml string and get a list of the orders
            xml_doc = ElementTree.fromstring(product_data)
            xml_products_list = xml_doc.findall("product")
            print(str(len(xml_products_list)) + " products")

            self.products_array.clear()

            # loop through the products
            for s in xml_products_list:
                obj = Objects.objProduct()
                obj.name = s.find("name").text
                obj.productid = int(s.find("productid").text)
                obj.refid = s.find("refid").text
                self.products_array.append(obj)

            # build the table

            index = 0

            for i in self.products_array: #Rows
                refidcell = self.uicommon.table_cell(frame, str(i.refid), justify=tk.CENTER, row=index, column=0)
                self.uicommon.bind_children(refidcell, '<ButtonPress-1>', self.__row_pressed)
                self.uicommon.bind_children(refidcell, '<ButtonRelease-1>', lambda event, arg1=i.productid: self.__product_list_click(arg1))  

                namecell = self.uicommon.table_cell(frame, str(i.name), justify=tk.CENTER, row=index, column=1)
                self.uicommon.bind_children(namecell, '<ButtonPress-1>', self.__row_pressed)
                self.uicommon.bind_children(namecell, '<ButtonRelease-1>', lambda event, arg1=i.productid: self.__product_list_click(arg1))

                index+=1

             # configure the column weights
            self.uicommon.table_column_weighs(frame, [1, 2], [100,220])

        else:
            # Data could not be retrieved from the server so show an error message
            self.uicommon.message_box(self.root_frame, "Communication Error", "The order list could not be retrieved from the server")

        return

    def __product_list_click(self, product_id):
        #
        # check if the mouse has been moved more than 5 pixels
        #

        x = self.root_frame.winfo_pointery() - self.cursor_start_position
        if (x > -5) and (x < 5): # mouse has moved less than 5 pixels so detect it as a click
            # check the amount of time that has passed since the press started
            duration = datetime.now() - self.click_start_time
            if (duration < timedelta(seconds=1)): # less than 1 second has passed so detect as click instead of hold
                self.__product_details(product_id)     
        return

    def __product_details(self, product_id = None, barcode = None):
        #
        # set the scanning mode to be 2: Products
        #

        Config.scanning_mode = 2 # products mode

        # clear the contents of the parent frame
        self.uicommon.clear_frame(self.parent_frame)

        # get the xml product list from the server and check that xml data was received

        product_data = None
       
        if (product_id != None):
            print("selected product id:" + str(product_id))
            product_data = self.comms.get_product_details(product_id = product_id)
        elif(barcode != None):
            print("selected barcode:" + str(barcode))
            product_data = self.comms.get_product_details(barcode = barcode)
        else:
            # No product id or barcode found so show an error message
            self.uicommon.message_box(self.root_frame, "Product Details Error", "Product details could not be retrieved from the server")

        if (product_data != None):

            # parse the xml string and get a list of the orders
            xml_doc = ElementTree.fromstring(product_data)
            xml_products_list = xml_doc.findall("product")
            print(str(len(xml_products_list)) + " products")

            self.products_array.clear()

            # get the products details
            s = xml_products_list[0]
            self.current_product = Objects.objProduct()
            self.current_product.name = s.find("name").text
            self.current_product.productid = int(s.find("productid").text)
            self.current_product.refid = s.find("refid").text

            # get the product options
            xml_options_list = s.findall(".//option")

            self.options_array.clear()

            for s in xml_options_list:
                obj = Objects.objProductOption()
                obj.optionid = int(s.find("optionid").text)
                obj.productid = int(s.find("productid").text)
                obj.name = s.find("name").text
                obj.stocklevel = int(s.find("stocklevel").text)
                obj.price = float(s.find("price").text)
                obj.barcode = s.find("barcode").text
                self.options_array.append(obj)

        # Build the Product Details Page
        overview_frame = tk.Frame(self.parent_frame, width=320)
        overview_frame.pack()

        id_title_label = self.uicommon.table_title(overview_frame, "ID:", row=0, column=0) 
        id_label = self.uicommon.table_cell(overview_frame, str(self.current_product.refid), row=0, column=1)

        name_title_label = self.uicommon.table_title(overview_frame, "Name:", row=1, column=0) 
        name_label = self.uicommon.table_cell(overview_frame, str(self.current_product.name), row=1, column=1)

        # set the column weights and widths
        self.uicommon.table_column_weighs(overview_frame, [1, 2], [80, 240])

        self.optionlist_frame = tk.Frame(self.parent_frame, width=320)
        self.optionlist_frame.pack()


        self.__options_list_table()

        return

    def __options_list_table(self):
        #
        # clear the contents of the options list table
        #
        self.uicommon.clear_frame(self.optionlist_frame)

        index = 1

        # add the titles
        product_title = self.uicommon.table_title(self.optionlist_frame, "Product ID/Name", row=0, column=0) 
        quantity_title = self.uicommon.table_title(self.optionlist_frame, "Stock", row=0, column=1)
        picked_title = self.uicommon.table_title(self.optionlist_frame, "Update", row=0, column=2)

        # add the contents of the options_array to the table
        for i in self.options_array:
            product_cell = self.uicommon.table_cell(self.optionlist_frame, i.name, row=index, column=0)
            quanitity_cell = self.uicommon.table_cell(self.optionlist_frame, i.stocklevel, row=index, column=1)
            self.uicommon.bind_children(quanitity_cell, '<ButtonPress-1>', self.__row_pressed)  
            self.uicommon.bind_children(quanitity_cell, '<ButtonRelease-1>', lambda event, arg1=i: self.__option_click(arg1))

            # add stock button
            add_stock_button = tk.Button(self.optionlist_frame, font="DejaVuSans 22 normal", foreground="white",pady=10, padx=15, activeforeground="white", background="#588706",activebackground="#4b7206", text="Add", command=lambda arg1=i: self.__add_stock_clicked(arg1))
            add_stock_button.grid(row=index, column=2)

        self.uicommon.table_column_weighs(self.optionlist_frame, [1, 2, 3], [190, 60, 70])
            
        return

    def __option_click(self, option):
        #
        # click event from the option stock level cell
        #
        self.selected_option = option
        self.uicommon.numeric_keypad(self.root_frame, self.__option_stock_level_changed, "Update Stock Level", value = self.selected_option.stocklevel)
        return

    def __add_stock_clicked(self, option):
        #
        # click event from the option add stock button
        #
        self.selected_option = option
        self.uicommon.numeric_keypad(self.root_frame, self.__option_stock_level_add, "Add Stock")
        return

    def __option_stock_level_changed(self, value):
        #
        #  Callback for the numeric keypad from __option_click
        #
        if (self.selected_option!= None) and (value != None):
            self.selected_option.stocklevel = int(value)
            self.__options_array_update(self.selected_option)
            self.__options_list_table()

            #send the new stock level to the server
            status = self.comms.set_product_quantity(self.selected_option.optionid, self.selected_option.stocklevel)

            if (status == 200):
                self.uicommon.message_box(self.root_frame, "Stock Updated", "The stock level\n has been updated")
                return
            else:
                self.uicommon.message_box(self.root_frame, "Communication Error", "The stock level could\n not be saved.\nError Code:" + str(status))
                return
        return

    def __option_stock_level_add(self, value):
        #
        #  Callback for the numeric keypad from __add_stock_clicked
        #
        if (self.selected_option!= None) and (value != None):
            self.selected_option.stocklevel += int(value)
            self.__options_array_update(self.selected_option)
            self.__options_list_table()

            #send the new stock level to the server
            status = self.comms.set_product_quantity(self.selected_option.optionid, self.selected_option.stocklevel)

            if (status == 200):
                self.uicommon.message_box(self.root_frame, "Stock Updated", "The stock level\n has been updated")
                return
            else:
                self.uicommon.message_box(self.root_frame, "Communication Error", "The stock level could\n not be saved.\nError Code:" + str(status))
                return
        return

    def __options_array_update(self, selected_item):
        #
        # update the picked status for the selected item
        #
        index = 0

        for i in self.options_array:
            if (i.optionid== selected_item.optionid):
                self.options_array[index] = selected_item
                break
            else:
                index+=1

        return

    def __row_pressed(self, event):
        self.click_start_time = datetime.now()
        self.cursor_start_position = self.root_frame.winfo_pointery()
