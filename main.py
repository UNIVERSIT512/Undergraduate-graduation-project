import dector
from Read import readCard
import threading
import time

while True:
    hasperson = dector.measure()
    time.sleep(1)
    if hasperson < 35:
        print("please start shuaka")
        while True:
            cardID = readCard()
            if cardID != "":
                print(cardID)
                time.sleep(1)
                break


 
 


        

