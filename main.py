import data.scripts.webscraping as webscraping
import data.scripts.managedb as managedb
import time
import datetime
import traceback


from plyer import notification
from playsound import playsound



if __name__ == '__main__':
    # x = contract.Option(127.00, "AAPL", "put", 1.09, "2020-12-31", "https://google.com")
    # y = contract.Option(187.00, "IWM", "put", 1.91, "2020-12-18", "https://booble.com")
    # z = contract.Option(670.00, "TSLA", "put", 174, "2020-12-04", "https://dooble.com")
    website = ""
    counter = 0
    webscraping.init()
    while True:
        length = managedb.getLength()
        if length < 5000:
            print("Removing duplicates")
            managedb.deleteDuplicates()
            print("Creating objects")
            objects = webscraping.createObjects(counter)
            counter += 1
            for i in objects:
                i.expDate = str(i.expDate[0]) + "-" + str(i.expDate[1]) + "-" + str(i.expDate[2])
                managedb.insertOption(i)
        try:
            print("Finding updates")
            updates = managedb.findAllUpdates()
        except:
            updates = []
            with open("log.txt", "a") as logfile:
                traceback.print_exc(file=logfile)
            print("EXCEPTION PLEASE RESTART")
        for i in updates:
            managedb.updatePrice(i, updates[i][0])
            managedb.updatePercentage(i, updates[i][1])
            website = i
            symbol = managedb.searchOptionByHref(i)
            if 15 < float(updates[i][1]) < 25:
                if updates[i][2] == 0:
                    notifTxt = open("notifications.txt", "a")
                    print("Profit over 15% detected for " + str(managedb.searchOptionByHref(i)[0]))
                    notification.notify(title="Possible Option!", message=str(symbol[0][0]) + "has a possible play!", app_name="CornBot", app_icon="data//icon.ico", timeout=10, toast=False)
                    notifTxt.write(
                        str(symbol[0]) + " - " + str(symbol[0][0]) + " has a " + str(updates[i][1]) + "% increase - " + str() + "(" + str(
                            datetime.datetime.now()) + ")" + "\n")
                    notifTxt.close()
                    playsound("data\\notification.mp3")
                    managedb.updateAlert(i)
                time.sleep(6)
        print("\n=====================================\n")
        time.sleep(20)
