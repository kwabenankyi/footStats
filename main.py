from understat_player_seasons import *
from time import time
LATESTSEASON = "2023/2024"
#main
db = Database('info.db')
fp = webdriver.FirefoxProfile()
opts = webdriver.FirefoxOptions()
opts.add_argument("--headless")
opts.add_argument("--width=2560")
opts.add_argument("--height=1440")
driver = webdriver.Firefox(options=opts)
starttime = time() 
START=6695
start=START
#START=(db.getLatestPlayerRecorded())
END=12300 #as of 22.12.2023
#get all players seasons stats

i=start
newDriver=True
while i<END:
    statsSelectedOnStart=recordPosition(db,driver,i,start,LATESTSEASON)
    i+=1
    if statsSelectedOnStart==False and newDriver==True:
        start=i
        continue
    newDriver=False
    if time()-starttime>290:
        print("---------Restarting driver...---------")
        driver.quit()
        driver = webdriver.Firefox(options=opts)
        starttime = time()
        start=i  
        sleep(1)
        newDriver=True

driver.quit()
print("---------Finished---------")