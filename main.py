from understat_player_seasons import *

#main
db = Database('info.db')
fp = webdriver.FirefoxProfile()
fp.set_preference("dom.max_script_run_time", 99999)
driver = webdriver.Firefox()
driver.set_script_timeout(36000)
#START=5890
START=(db.getLatestPlayerRecorded())
END=17000
#get all players seasons stats
for i in range (START,END):
    recordSeason(db,driver,i,START)
    sleep(0.5)
driver.quit()
