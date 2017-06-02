# Variables accessable from any class

# tkinter GUI library
import tkinter.ttk as ttk

# scanning mode: Used to determin which mode the barcode scanner is operating in.
# 0 = default mode
# 1 = orders mode
# 2 = products mode
# 3 = parts mode
scanning_mode = 0


# network status: Used to determin if there is a working internet connection
network_status = False

# use https: Determins whether the application uses http or https.  http is used for local debugging

use_https = True

# scanner id:  Used to identify the device to the data server

scanner_id = ""

# server url

server_url = ""

# order list path

order_list_url = ""

# order details path
order_details_path = ""

# order save path
order_save_path = ""

# products list path

product_list_url = ""

# products details path

product_details_url = ""

# product quantity path
product_quantity_path = ""


# table styles
style_header_background_colour = "#dddddd"
style_header_foreground_colour = "#000000"
style_header_border_colour = "#aaaaaa"
style_header_border_width = 1
style_header_font = "DejaVuSans 17 bold"

style_row_background_colour = "#ffffff"
style_row_foreground_colour = "#000000"
style_row_border_colour = "#cccccc"
style_row_border_width = 1
style_row_font = "DejaVuSans 17 normal"



