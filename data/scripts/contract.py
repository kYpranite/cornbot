import wallstreet


class Option:
    def __init__(self, strike, symbol, indicator, ogPrice, expDate, href):
        self.strike = strike
        self.symbol = symbol
        self.indicator = indicator
        self.percentage = 0
        self.ogPrice = ogPrice
        self.expDate = expDate
        self.price = 0
        self.href = href
        self.alert = 0

    def printAll(self):
        print("==================================\n\n")
        print("Strike: " + str(self.strike))
        print("Symbol: " + str(self.symbol))
        print("Indicator: " + str(self.indicator))
        print("Percentage Increase: " + str(self.percentage))
        print("Original Price: " + str(self.ogPrice))
        print("Expiration Date: " + str(self.expDate))
        print("Last Price: " + str(self.price))
        print("Link: " + str(self.href))
        print("Alerted: " + str(self.alert))


def calculatePercentage(lastPrice, originalPrice):  # finds percentage between last and original price
    increase = float(lastPrice) - float(originalPrice)
    percentage = (increase / float(originalPrice)) * 100
    percentage = str(round(percentage, 2))
    return percentage


def getLastPrice(symbol, expDate, strike, indicator):  # gets last price by inputting exp date, strike, and symbol
    if indicator == "put":
        stock = wallstreet.Put(symbol, d=int(expDate[2]), m=int(expDate[1]), y=int(expDate[0]),
                               strike=float(strike))
        lastPrice = stock.price
    else:
        stock = wallstreet.Call(symbol, d=int(expDate[2]), m=int(expDate[1]), y=int(expDate[0]),
                                strike=float(strike))
        lastPrice = stock.price
    return lastPrice


# stock = wallstreet.Call("IWM", d=31, m=12, y=2020, strike=200.0)
# j = 0
# for i in range(2000):
#     print(stock.price)
#     j+=1
#     print(j)

