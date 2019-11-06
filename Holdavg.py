from backtesting import evaluateTick
from strategy import Strategy
from order import Order
from event import Event
import numpy as np



class HoldAVG(Strategy):

    def __init__(self):
        self.signal = 0
        self.prices = []
        self.size = 800
        self.std = 0
        self.pastprice=0
        self.count=0
        self.canTrade=False
        self.mavg=0
        self.std=0


    def push(self, event):

        diff=self.pastprice-event.price
        self.pastprice=event.price
        #print(self.canTrade)

        if event.type == Event.TRADE:
            price = event.price
            self.prices.append(price)
            orders = []
            self.count=self.count+1
            #print(len(self.prices))

            if self.count==self.size:
                self.canTrade=not(self.canTrade)
                self.std = np.array(self.prices).std()
                self.mavg = sum(self.prices)/self.size
                self.count=0
                self.prices.clear()

            if self.canTrade:
                #print(price,self.mavg + self.std)
                if (price >= self.mavg + self.std):
                    if self.signal == 1:
                        orders.append(Order(event.instrument, -100, 0))
                    if self.signal == 0:
                        orders.append(Order(event.instrument, -100, 0))
                    self.signal = -1
                elif (price <= self.mavg - self.std):
                    if self.signal == -1:
                        orders.append(Order(event.instrument, 100, 0))
                    if self.signal == 0:
                        orders.append(Order(event.instrument, 100, 0))
                    self.signal = 1

                #del self.prices[0]

            return orders
        return []

print(evaluateTick(HoldAVG(), {'P0':'2018-08-01.csv','P1':'2018-08-02.csv','P2':'2018-08-03.csv','P3':'2018-03-07.csv'}))
