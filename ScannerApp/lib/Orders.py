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

class Orders():
    
    comms = NetworkComms.Communication()
    uicommon = UICommon.UICommon()    

    click_start_time = datetime.now() # used for detecting a click or scroll
    cursor_start_position = 0

    order_array = [] # stores the list of orders
    items_array = [] # stores the items within a single order

    current_order = Objects.objOrder()
    current_item = Objects.objOrderItem()

    root_frame = None
    parent_frame = None # the scroll frame
    itemlist_frame = None # used within the order details frame to list items

    true_image = None # used for the item pick status
    false_image = None # used for the item pick status

    

    def __init__(self, root, master):
        #
        # Initialise the orders class
        #
        self.root_frame = root
        self.parent_frame = master
        self.uicommon.root_frame = self.root_frame

        self.true_image = ImageTk.PhotoImage(Image.open(self.uicommon.system_path + "true.bmp"))
        self.false_image = ImageTk.PhotoImage(Image.open(self.uicommon.system_path + "false.bmp"))

    def process_barcode(self, barcode, frame=None):
        #
        # trim the first two numbers and the last number from the order barcode and convert it into an integer
        #

        if (frame != None):
            self.parent_frame = frame

        code = barcode[2:]
        order_id = int(code[:-1])

        # get the order details
        self.__order_details(order_id)

        return

    def process_product_barcode(self, barcode, frame=None):
        #
        # search the items array for the product barcode
        #

        if (frame != None):
            self.parent_frame = frame

        found = False
        for i in self.items_array:
            if (i.barcode == barcode):
                self.current_item = i
                self.__item_quantity_changed(i.picked + 1)
                found = True
                break

        if (found == False):
            self.uicommon.message_box(self.root_frame, "Not Found", "The barcode does not\n match any of the\n ordered items.")
        return

    def orders_list(self, frame):
        #
        # Fetches and displays a list of the current orders
        #

        self.parent_frame = frame

        # set the scanning mode to default
        Config.scanning_mode = 0

        # clear the contents of the parent frame
        self.uicommon.clear_frame(self.parent_frame)

        # get the xml order list from the server and check that xml data was received
        order_data = self.comms.get_order_list()
        if (order_data != None):
            # parse the xml string and get a list of the orders
            xml_doc = ElementTree.fromstring(order_data)
            xml_orders_list = xml_doc.findall("order")
            print(str(len(xml_orders_list)) + " orders")

            self.order_array.clear()

            # loop through the orders
            for s in xml_orders_list:
                obj = Objects.objOrder()
                obj.id = int(s.find("id").text)
                obj.date = datetime.strptime(s.find("date").text, '%Y-%m-%dT%H:%M:%S')
                obj.country = s.find("country").text
                obj.name = s.find("name").text
                obj.status = s.find("status").text
                obj.total = float(s.find("total").text)
                self.order_array.append(obj)

            # build the table

            index = 0
            for i in self.order_array: #Rows

                # set the colour for the first cell to show the status of the order
                colour = "#ffffff"

                if (str(i.status) == "Quotation"):
                    colour = "#b4c6e7"
                elif (str(i.status) == "Payment Error"):
                    colour = "#8497b0"
                elif (str(i.status) == "Order Saved"):
                    colour = "#fff600"
                elif (str(i.status) == "Payment Pending"):
                    colour = "#00b0f0"
                elif (str(i.status) == "Card Payment Pending"):
                    colour = "#00b0f0"
                elif (str(i.status) == "Account Pending"):
                    colour = "#00b0f0"
                elif (str(i.status) == "Cheque Pending"):
                    colour = "#00b0f0"
                elif (str(i.status) == "Payment Received"):
                    colour = "#00cc00"
                elif (str(i.status) == "Below Min Qty"):
                    colour = "#9bc2e6"
                elif (str(i.status) == "Age Verification"):
                    colour = "#ff0000"
                elif (str(i.status) == "Awaiting Stock"):
                    colour = "#bf8f00"
                elif (str(i.status) == "Being Processed"):
                    colour = "#ffc000"
                elif (str(i.status) == "Awaiting Dispatch"):
                    colour = "#57006d"

                ordercolourcell = tk.Label(frame, text=" ", background=colour, padx=5, pady=10)
                ordercolourcell.grid(row=index, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

                orderidcell = self.uicommon.table_cell(frame, str(i.id), justify=tk.CENTER, row=index, column=1)
                self.uicommon.bind_children(orderidcell, '<ButtonPress-1>', self.__row_pressed)
                self.uicommon.bind_children(orderidcell, '<ButtonRelease-1>', lambda event, arg1=i.id: self.__orders_list_click(event, arg1))                 

                t = datetime.strftime(i.date, "%d/%m/%y")
                orderdatecell = self.uicommon.table_cell(frame, t, row=index, column=2)       
                self.uicommon.bind_children(orderdatecell, '<ButtonPress-1>', self.__row_pressed)  
                self.uicommon.bind_children(orderdatecell, '<ButtonRelease-1>', lambda event, arg1=i.id: self.__orders_list_click(arg1))                 
            
                ordertextcell = self.uicommon.table_cell(frame, str(i.name) + "\n" + str(i.country), row=index, column=3)          
                self.uicommon.bind_children(ordertextcell, '<ButtonPress-1>', self.__row_pressed)  
                self.uicommon.bind_children(ordertextcell, '<ButtonRelease-1>', lambda event, arg1=i.id: self.__orders_list_click(arg1))                 

                ordertotalcell = self.uicommon.table_cell(frame, str(i.total), justify=tk.RIGHT, row=index, column=4)          
                self.uicommon.bind_children(ordertotalcell, '<ButtonPress-1>', self.__row_pressed)  
                self.uicommon.bind_children(ordertotalcell, '<ButtonRelease-1>', lambda event, arg1=i.id: self.__orders_list_click(arg1))                 

                index+=1

            # configure the column weights
            self.uicommon.table_column_weighs(frame, [5, 4, 2, 1, 3], [5,60,80,120,60])

        else:
            # Data could not be retrieved from the server so show an error message
            self.uicommon.message_box(self.root_frame, "Communication Error", "The order list could not be retrieved from the server")

        return    


    def __orders_list_click(self, selected_id):
        #
        # check if the mouse has been moved more than 5 pixels
        #

        x = self.root_frame.winfo_pointery() - self.cursor_start_position
        if (x > -5) and (x < 5): # mouse has moved less than 5 pixels so detect it as a click
            # check the amount of time that has passed since the press started
            duration = datetime.now() - self.click_start_time
            if (duration < timedelta(seconds=1)): # less than 1 second has passed so detect as click instead of hold
                self.__order_details(selected_id)     
        return


    def __order_details(self, order_id):
        #
        # set the scanning mode to be 1: Orders
        #        

        Config.scanning_mode = 1 # orders mode

        # get the xml order list from the server
        order_data = self.comms.get_order_details(order_id)
         # parse the xml string and get a list of the orders
        xml_doc = ElementTree.fromstring(order_data)
        xml_order_overview = xml_doc.findall("order")
        xml_item_list = xml_doc.findall("item")
        print(str(len(xml_item_list)) + " items")

        self.items_array.clear()
        
        # get the order overview information
        for s in xml_order_overview:
            self.current_order.id = int(s.find("id").text)
            self.current_order.date = datetime.strptime(s.find("date").text, '%Y-%m-%dT%H:%M:%S')
            self.current_order.country = s.find("country").text
            self.current_order.name = s.find("name").text
            self.current_order.status = s.find("status").text
            self.current_order.total = float(s.find("total").text)

        print("Current Order: " + str(self.current_order.id))

        # loop through the order items
        for s in xml_item_list:
            obj = Objects.objOrderItem()
            obj.orderid = self.current_order.id
            obj.productref = s.find("productref").text
            obj.productname = s.find("productname").text
            obj.quantity = int(s.find("quantity").text)
            obj.unitprice = float(s.find("unitprice").text)
            obj.barcode = s.find("barcode").text

            print(obj.productname)
            self.items_array.append(obj)

        # clear any existing elements from the parent frame
        self.uicommon.clear_frame(self.parent_frame)

        # build the overview frame
        overview_frame = tk.Frame(self.parent_frame, width=320)
        overview_frame.pack()
        
        id_title_label = self.uicommon.table_title(overview_frame, "Order ID:", row=0, column=0) 
        id_label = self.uicommon.table_cell(overview_frame, str(self.current_order.id), row=0, column=1) 

        date_title_label = self.uicommon.table_title(overview_frame, "Date:", row=1, column=0) 
        date_label = self.uicommon.table_cell(overview_frame, str(self.current_order.date), row=1, column=1, columnspan=2) 

        name_title_label = self.uicommon.table_title(overview_frame, "Name:", row=2, column=0) 
        name_label = self.uicommon.table_cell(overview_frame, str(self.current_order.name), row=2, column=1, columnspan=2) 

        country_title_label = self.uicommon.table_title(overview_frame, "Country:", row=3, column=0) 
        country_label = self.uicommon.table_cell(overview_frame, str(self.current_order.country), row=3, column=1, columnspan=2) 

        status_title_label = self.uicommon.table_title(overview_frame, "Status:", row=4, column=0) 
        status_label = self.uicommon.table_cell(overview_frame, str(self.current_order.status), row=4, column=1, columnspan=2)

        # save button
        save_button = tk.Button(overview_frame, width=120, font="DejaVuSans 30 normal", foreground="white",pady=5, activeforeground="white", background="#588706",activebackground="#4b7206", text="Save", command=self.__save_order)
        save_button.grid(row=0, column=2)

        # set the column weights and widths
        self.uicommon.table_column_weighs(overview_frame, [3, 1, 2], [80, 120, 120])

        self.itemlist_frame = tk.Frame(self.parent_frame, width=320)
        self.itemlist_frame.pack()

        # build the table frame
        self.__item_list_table()

        
        return
    

    def __item_list_table(self):
        #
        # clear the contents of the item list table
        #
        self.uicommon.clear_frame(self.itemlist_frame)

        index = 1

        # add the titles
        product_title = self.uicommon.table_title(self.itemlist_frame, "Product ID/Name", row=0, column=0) 
        quantity_title = self.uicommon.table_title(self.itemlist_frame, "Qty", row=0, column=1)
        picked_title = self.uicommon.table_title(self.itemlist_frame, "Picked", row=0, column=2)

        # add the contents of the items_array to the table
        for i in self.items_array:
            product_cell = self.uicommon.table_cell(self.itemlist_frame, i.productref + "\n" + i.productname, row=index, column=0)

            quanitity_cell = self.uicommon.table_cell(self.itemlist_frame, i.quantity, row=index, column=1)

            if (i.picked == 0):
                picked_cell = self.uicommon.table_cell(self.itemlist_frame, image=self.false_image, row=index, column=2)
            elif(i.picked == i.quantity):
                picked_cell = self.uicommon.table_cell(self.itemlist_frame, image=self.true_image, row=index, column=2)
            else:
                picked_cell = self.uicommon.table_cell(self.itemlist_frame, image=None, celltext=str(i.picked), row=index, column=2)
            self.uicommon.bind_children(picked_cell, '<ButtonPress-1>', self.__row_pressed)  
            self.uicommon.bind_children(picked_cell, '<ButtonRelease-1>', lambda event, arg1=i: self.__item_click(arg1))

            index+= 1

        self.uicommon.table_column_weighs(self.itemlist_frame, [1, 2], [210, 40, 40])


    def __item_click(self, selected_item):
        #
        #  Checks if a click is valid and then updates the picked quanitity
        #

        # check if the mouse has been moved more than 5 pixels
        x = self.root_frame.winfo_pointery() - self.cursor_start_position
        if (x > -5) and (x < 5): # mouse has moved less than 5 pixels so detect it as a click
            # check the amount of time that has passed since the press started
            duration = datetime.now() - self.click_start_time
            if (duration < timedelta(seconds=1)): # less than 1 second has passed so detect as click instead of hold
                self.current_item = selected_item

                # if selected item has already been picked reset it to be unpicked
                if (selected_item.picked == selected_item.quantity):
                    selected_item.picked = 0                    
                    self.__items_array_update(selected_item)
                    self.__item_list_table()
                elif(selected_item.quantity == 1):
                    # get the quantity for the selected item.  If the quanitity is 1 update the picked status to be 1 else show the numeric keypad
                    selected_item.picked = 1
                    self.__items_array_update(selected_item)
                    self.__item_list_table()
                else:    
                    self.uicommon.numeric_keypad(self.root_frame, self.__item_quantity_changed, "Quantity Picked: " + str(selected_item.quantity) + " required")

                
        return

    def __items_array_update(self, selected_item):
        #
        # update the picked status for the selected item
        #
        index = 0

        for i in self.items_array:
            if (i.productref == selected_item.productref):
                self.items_array[index] = selected_item
                break
            else:
                index+=1

        return
            


    def __item_quantity_changed(self, value):
        #
        #  Callback for the numeric keypad
        #

        if (self.current_item!= None) and (value != None):
            self.current_item.picked = int(value)
            self.__items_array_update(self.current_item)
            self.__item_list_table()                   

   

    def __save_order(self):
        #
        # Saves the status of the order onto the server
        #

        # check if all of the items in the items_array have been picked
        all_picked = True
        for i in self.items_array:
            if (i.picked < i.quantity):
                all_picked = False

        # if all picked then send the response to the server otherwise show a message
        if (all_picked):
            status = self.comms.set_order_status(self.current_order.id)

            if (status == 200):
                self.uicommon.message_box(self.root_frame, "Order Saved", "The order status\n has been updated", target=self.orders_list(self.parent_frame))
                return
            else:
                self.uicommon.message_box(self.root_frame, "Communication Error", "The order could\n not be saved.\nError Code:" + str(status))
                return
        else:
            self.uicommon.message_box(self.root_frame, "Order Not Complete", "There are items which\n have not been picked.")
            
        return

    def __row_pressed(self, event):
        self.click_start_time = datetime.now()
        self.cursor_start_position = self.root_frame.winfo_pointery()


