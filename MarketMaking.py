from backtesting import evaluateIntr
from strategy import Strategy
from order import Order
import numpy as np

class MarketMaker(Strategy):
    def __init__(self):
        self.pricePETR3=0
        self.priceUSD=0
        self.spread=0.15
        self.compraId=None
        self.vendeId=None
        self.pbr=[]
        

    def push(self,event):
        orders=[]
      
        if (event.instrument=="PETR3"):
            self.pricePETR3=event.price[3]
            self.pbr.append(self.pricePETR3)

        if (event.instrument=="USDBRL"):
            self.priceUSD=event.price[3]
            self.pbr.append(self.priceUSD)

        if len(self.pbr)==2:

            if(self.priceUSD!=0 and self.pricePETR3!=0):

                if self.compraId!=None and self.vendeId != None:
                    self.cancel(self.id,self.compraId)
                    self.cancel(self.id,self.vendeId)


                pbr=(self.pricePETR3/self.priceUSD)*2

                orderCompra=(Order(event.instrument,1,pbr-self.spread))
                self.compraId=orderCompra.id
                orders.append(orderCompra)

                orderVenda=(Order(event.instrument,-1,pbr+self.spread))
                self.vendeId=orderVenda.id
                orders.append(orderVenda)



            return orders
        



 
    def fill(self,id,instrument,price,quantity,status):
        super().fill(id,instrument,price,quantity,status)
        Orders=[]
        if instrument=="PBR":
            if quantity!=0:
                if quantity>0:
                    vendePetra = Order("PETR3",-2*quantity,0)
                    compraDolar = Order("USDBRL",1*quantity,0)
                    Orders.append(compraDolar)
                    Orders.append(vendePetra)
                    self.submit(self.id,Orders)
                else:
                    compraPetra = Order("PETR3",2*quantity,0)
                    vendeDolar = Order("USDBRL",-1*quantity,0)
                    Orders.append(vendeDolar)
                    Orders.append(compraPetra)
                    self.submit(self.id,Orders)
        
        if quantity!=0:
            print(instrument,price,quantity)




 
print(evaluateIntr(MarketMaker(), {'USDBRL': 'USDBRL.csv', 'PETR3': 'PETR3.csv','pbr':'pbr.csv'}))