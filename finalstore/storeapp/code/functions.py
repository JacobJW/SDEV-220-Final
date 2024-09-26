# This file will contain function definitions for app use
import math
import datetime
from ..models import *

def CalculatePrice(order_id:int,tip_amount:float):
    order = Order.objects.get(order_id=order_id) # Get the order
    items_in_order = OrderItem.objects.filter(order_id=order.order_id) # Gather all items in order
    total_price = 0.0 # set the price at zero to start

    # iterate over each item to find its price
    for item in items_in_order:
        item_product = Product.objects.get(product_id=item.product_id) # find the product
        item_price = item_product.price * item.quantity # multiply product cost by quantity
        total_price += item_price # add price to total
    
    # calculate the tax (8% sales rate)
    tax_amount = round(number=total_price * 0.08,ndigits=2)
    # add all components together to get the final price
    final_price = total_price + tax_amount + tip_amount

    # update the Order object with price info
    order.item_total = total_price
    order.tax = tax_amount
    order.tip = tip_amount
    order.final_total = final_price
    # finish by returning final price
    return final_price

def ModifyBalance(user_id:int,operation:str,value:float):
    user = User.objects.get(user_id=user_id)

    if operation == 'Add':
        user.card_balance += abs(value)
    elif operation == 'Charge':
        user.card_balance -= abs(value)

    return str(user.card_balance)

def UserPlaceOrder(user_id:int,loc_id:int,item_tuple:tuple,q_tuple:tuple):
    user = User.objects.get(user_id=user_id)
    location = Location.objects.get(loc_id=loc_id)
    # Creates a new order object
    order = Order(
        user_id=user.user_id,
        loc_id=location.loc_id,
        order_date = datetime.datetime.now()
        )
    order.save()

    # Create new items in the order, based off the dictionary items
    for item in item_tuple:
        product_type = item_tuple[item] # this tuple holds the names of products
        item_quantity = q_tuple[item] # this tuple holds count of each product, matching the order of the above tuple

        order_item = OrderItem(
            order_id = order.order_id,
            item_no = item+1,
            product_id = product_type,
            quantity = item_quantity
        )
        order_item.save()

    # Get the order price
