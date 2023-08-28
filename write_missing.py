from understat_player_seasons import *
import csv

db = Database('info.db')
MAX=db.getLatestPlayerRecorded()
driver = webdriver.Firefox()

for i in range (1,MAX+1):
    playExists=db.checkPlayerID(i)
    if playExists == None:
        link='https://understat.com/player/'+str(i)
        driver.get(link)
        with open("noinfo.csv","a") as f:
            f.write(str(i)+","+getName(driver)+'\n')
        print(i,"has been added")      