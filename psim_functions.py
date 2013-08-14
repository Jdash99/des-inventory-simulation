import sys
import numpy as np
from pandas import DataFrame
import pdb


class Product(object):

    def __init__(self, name, demand_dist,
                 lead_time_dist, initial_inventory, price):
        self.name = name
        self.demand_dist = demand_dist
        self.lead_time_dist = lead_time_dist
        self.initial_inventory = initial_inventory
        self.price = price

    def __repr__(self):
        return self.name

    def demand(self):
        return self.demand_dist()

    def lead_time(self):
        return self.lead_time_dist()


class Supplier(object):

    def __init__(self, name):
        self.name = name
        self.product_list = []

    def __repr__(self):
        return self.name

    def add_product(self, product):
        if product not in self.product_list:
            self.product_list.append(product)
        else:
            print("product already in list")


class Order(object):

    """Object that stores basic data of an order"""

    def __init__(self, quantity, lead_time, sent):
        self.quantity = quantity
        self.lead_time = lead_time
        self.sent = sent  # True if the order is already sent


def make_data(product,
              policy={'method': 'Qs', 'arguments': {'Q': 3, 's': 5}},
              periods=52
              ):
    """ Return a Pandas dataFrame that contains the details of the inventory simulation.

    Keyword arguments:
    product           -- Product object
    policy            -- dict that contains the policy specs (default = {'method':'Qs', 'arguments': {'Q':3,'s':5}})
    periods           -- numbers of periods of the simulation (default 52 weeks)
    """

    # Create zero-filled Dataframe
    period_lst = np.arange(periods)  # index
    header = ['initial_inv_pos', 'initial_net_inv', 'demand', 'final_inv_pos',
              'final_net_inv', 'lost_sales', 'avg_inv', 'order', 'lead_time']  # columns
    df = DataFrame(index=period_lst, columns=header).fillna(0)

    # Create a list that will store each period order
    order_list = [Order(quantity=0, lead_time=0, sent=False)
                  for x in range(periods)]

    # Fill DataFrame
    for period in period_lst:
        if period == 0:
            df['initial_inv_pos'][period] = product.initial_inventory
            df['initial_net_inv'][period] = product.initial_inventory
        else:
            df['initial_inv_pos'][period] = df['final_inv_pos'][
                period - 1] + order_list[period - 1].quantity
            df['initial_net_inv'][period] = df['final_net_inv'][
                period - 1] + pending_order(order_list, period)
        
        demand = int(product.demand())
        if  demand > 0:
            df['demand'][period] = demand
        else:
            df['demand'][period] = 0


        if df['initial_inv_pos'][period] - df['demand'][period] < 0:
            df['final_inv_pos'][period] = 0
        else:
            df['final_inv_pos'][period] = df[
                'initial_inv_pos'][period] - df['demand'][period]

        order_list[period].quantity, order_list[period].lead_time, order_list[
            period].sent = placeorder(product, df['final_inv_pos'][period], policy, period)
        df['final_net_inv'][period] = df[
            'initial_net_inv'][period] - df['demand'][period]
        if df['final_net_inv'][period] < 0:
            df['lost_sales'][period] = abs(df['final_net_inv'][period])
            df['final_net_inv'][period] = 0
        else:
            df['lost_sales'][period] = 0
        df['avg_inv'][period] = (
            df['initial_net_inv'][period] + df['final_net_inv'][period]) / 2.0
        df['order'][period] = order_list[period].quantity
        df['lead_time'][period] = order_list[period].lead_time

    return df


def make_distribution(function, *pars):
    """ The distribution factory"""
    def distribution():
        return function(*pars)
    return distribution


def pending_order(order_list, period):
    """Return the order that arrives in actual period"""
    indices = [i for i, order in enumerate(order_list) if order.sent]
    sum = 0
    for i in indices:
        if period - (i + order_list[i].lead_time + 1) == 0:
            sum += order_list[i].quantity
    return sum


def placeorder(product, final_inv_pos, policy, period):
    """Place the order acording the inventory policy:

       Keywords arguments:
       product          -- object Product
       final_inv_pos    -- final inventory position of period
       policy           -- chosen policy Reorder point (Qs, Ss) or Periodic Review (RS, Rss)
       period           -- actual period
    """

    lead_time = int(product.lead_time())

    # Qs = if we hit the reorder point s, order Q units
    if policy['method'] == 'Qs' and \
            final_inv_pos <= policy['arguments']['s']:
        return policy['arguments']['Q'], lead_time, True
    # Ss = if we hit the reorder point s, order S - final inventory pos
    elif policy['method'] == 'Ss' and \
            final_inv_pos <= policy['arguments']['s']:
        return policy['arguments']['S'] - final_inv_pos, lead_time, True
    # RS = if we hit the review period R and the reorder point S, order: (S -
    # final inventory pos)
    elif policy['method'] == 'RS' and \
        period % policy['arguments']['R'] == 0 and \
            final_inv_pos <= policy['arguments']['S']:
        return policy['arguments']['S'] - final_inv_pos, lead_time, True
    # RSs = if we hit the review period and the reorder point s, order: (S -
    # final inventory pos)
    elif policy['method'] == 'RSs' and \
        period % policy['arguments']['R'] == 0 and \
            final_inv_pos <= policy['arguments']['s']:
        return policy['arguments']['S'] - final_inv_pos, lead_time, True
    # If the conditions arent satisfied, do not order
    else:
        return 0, 0, False
