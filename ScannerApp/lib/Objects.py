# Objects accessable from any class

# Order Objects

class objOrder(object):
    def __init__(self, id = None, date = None, status = None, name = None, country = None, total = None, items = None):
        self.id = id
        self.date = date
        self.status = status
        self.name = name
        self.country = country
        self.total = total
        self.items = items

class objOrderItem(object):
    def __init__(self, orderid=None, productref=None, productname=None, quantity=None,unitprice=None,barcode=None, picked=0):
        self.orderid = orderid
        self.productref = productref
        self.productname = productname
        self.quantity = quantity
        self.unitprice = unitprice
        self.barcode = barcode
        self.picked = picked


# Products Objects

class objProduct(object):
    def __init__(self, productid = None, refid = None, name = None):
        self.productid = productid
        self.refid = refid
        self.name = name

class objProductOption(object):
    def __init__(self,optionid = None, productid = None, name = None, stocklevel = None, price = None, barcode = None):
        self.optionid = optionid
        self.productid = productid
        self.name = name
        self.stocklevel = stocklevel
        self.price = price
        self.barcode = barcode

# Parts Objects
