# OS library for accessing os functions
import os

# HTTP and URL libraries
import http.client, urllib.parse

# Config global variables
from lib import Config


class Communication:
    """All classes related to network communication and data transfers"""


    def ping(self, url):
        #
        # ping a url to check if there is a working internet connection
        #
        Hostname = url
        Response = os.system("ping -c 1 " + Hostname)

        if Response == 0:
            return (True)
        else:
            return (False)


    def get_order_list(self):
        #
        #  Request an xml dataset for the outstanding orders
        #
        params = urllib.parse.urlencode({'unitid': Config.scanner_id})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None
        try:
            if (Config.use_https):
                conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
            else:
                conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        
            conn.request("POST", Config.order_list_url, params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as ex:
            print(ex.args[0])            
            pass

        return data

    def get_order_details(self, orderid):
        #
        # Request an xml dataset for the details and items of an individual order
        #
        params = urllib.parse.urlencode({'unitid': Config.scanner_id, 'orderid': str(orderid)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None
        if (Config.use_https):
            conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
        else:
            conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        try:
            conn.request("POST", Config.order_details_path, params, headers)
            response = conn.getresponse()
            data = response.read()
        except Exception as ex:
            print(ex)
            pass
        
        conn.close()

        return data

    def set_order_status(self, orderid):
        #
        # Send a request to the server to set an order status as Awaiting Dispatch
        #
        params = urllib.parse.urlencode({'unitid': Config.scanner_id, 'orderid': str(orderid)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None

        if (Config.use_https):
            conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
        else:
            conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        try:
            conn.request("POST", Config.order_save_path, params, headers)
            response = conn.getresponse()
            data = response.getcode()
            conn.close()
        except Exception as ex:
            print(ex)
            pass

        return data

    def get_product_list(self):
        #
        # Request an xml dataset containing a list of products
        #
        params = urllib.parse.urlencode({'unitid': Config.scanner_id})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None
        try:
            if (Config.use_https):
                conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
            else:
                conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        
            conn.request("POST", Config.product_list_url, params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as ex:
            print(ex.args[0])            
            pass

        return data

    def get_product_details(self, product_id = None, barcode = None):
        #
        # Request an xml dataset containing the details of a product based on its id or barcode
        #

        if (product_id != None):
            params = urllib.parse.urlencode({'unitid': Config.scanner_id, 'productid': str(product_id)})
        elif (barcode != None):
            params = urllib.parse.urlencode({'unitid': Config.scanner_id, 'barcode': str(barcode)})
        else:
            return None

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None
        if (Config.use_https):
            conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
        else:
            conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        try:
            conn.request("POST", Config.product_details_url, params, headers)
            response = conn.getresponse()
            data = response.read()
        except Exception as ex:
            print(ex)
            pass
        
        conn.close()

        return data

    def set_product_quantity(self, optionid, stocklevel):
        #
        # Send a ID and quantity to be added to the stock level for a product
        #
        params = urllib.parse.urlencode({'unitid': Config.scanner_id, 'optionid': str(optionid), 'stocklevel': str(stocklevel)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        data = None

        if (Config.use_https):
            conn = http.client.HTTPSConnection(Config.server_url, timeout=5)
        else:
            conn = http.client.HTTPConnection(Config.server_url, timeout=5)
        try:
            conn.request("POST", Config.product_quantity_path, params, headers)
            response = conn.getresponse()
            data = response.getcode()
            conn.close()
        except Exception as ex:
            print(ex)
            pass

        return data

    def get_part_list(self):
        #
        # Request an xml dataset containing a list of parts
        #
        return

    def get_part_details(self, partid):
        #
        # Request an xml dataset containing the details for a part
        #
        return

