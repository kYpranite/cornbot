import sqlite3
import data.scripts.contract as contract
import datetime
import os

conn = sqlite3.connect(str(os.getcwd()) + '\\data\\scripts\\options.db')
cursor = conn.cursor()


# cursor.execute("""CREATE TABLE options(
#                     symbol text,
#                     strike real,
#                     indicator text,
#                     ogPrice real,
#                     price real,
#                     expDate text,
#                     href text,
#                     percentage real,
#                     alert integer)""")


def insertOption(option):
    with conn:
        print("Inserting option: " + str(option.symbol))
        cursor.execute(
            "INSERT INTO options VALUES (:symbol, :strike, :indicator, :ogPrice, :price, :expDate, :href, :percentage, :alert)",
            {'symbol': option.symbol, 'strike': option.strike, 'indicator': option.indicator,
             'ogPrice': option.ogPrice, 'price': option.price, 'expDate': option.expDate, 'href': option.href,
             'percentage': option.percentage, 'alert': option.alert})


def deleteOption(href):
    with conn:
        cursor.execute("DELETE from options WHERE href = :href",
                       {'href': href})


def deleteDuplicates():
    with conn:
        cursor.execute("CREATE TABLE tempTable as SELECT DISTINCT * FROM options")
        cursor.execute("DELETE FROM options")
        cursor.execute("INSERT INTO options SELECT * FROM tempTable")
        cursor.execute("DROP TABLE tempTable")


def searchOptionByHref(href):
    with conn:
        cursor.execute("SELECT * FROM options WHERE href=:href", {'href': href})
        return cursor.fetchall()


def printAllRecords():
    with conn:
        cursor.execute("SELECT * FROM options")
        print("=======================")
        print(cursor.fetchall())
        print("\n\n\n")


def getLength():
    with conn:
        cursor.execute("SELECT * FROM options")
        length = len(cursor.fetchall())
        return length


def updatePrice(href, price):
    with conn:
        cursor.execute("""UPDATE options SET price = :price WHERE href = :href""",
                       {'href': href, 'price': float(price)})


def updatePercentage(href, percentage):
    with conn:
        cursor.execute("""UPDATE options SET percentage = :percentage WHERE href = :href""",
                       {'href': href, 'percentage': float(percentage)})


def updateAlert(href):
    with conn:
        cursor.execute("""UPDATE options SET alert = :alert WHERE href = :href""",
                       {'href': href, 'alert': 1})


def findAllUpdates():
    with conn:
        updates = dict()
        cursor.execute("SELECT * FROM options")
        for result in cursor.fetchall():
            price = result[4]
            parsedDate = result[5].split('-')
            currentPrice = contract.getLastPrice(result[0], parsedDate, result[1], result[2])
            expireDate = datetime.date(int(parsedDate[0]), int(parsedDate[1]), int(parsedDate[2]))
            expireDate = expireDate - datetime.date.today()
            if expireDate.days <= 0:
                print("Deleted option: " + result[0] + " because it expired")
                deleteOption(result[6])
            if float(price) != float(currentPrice):
                percentage = contract.calculatePercentage(currentPrice, result[3])
                updates[result[6]] = [currentPrice, percentage, result[8]]
        return updates

#
# toUpdate = findAllUpdates()
# for i in toUpdate:
#     updatePrice(i, toUpdate[i])
#
# cursor.execute("SELECT * FROM options")
# print(cursor.fetchall())
#
