from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from findNameLength import *
import sqlite3
import csv

class Database():
    def __init__(self, conn):
        self.__conn = sqlite3.connect(conn)
        self.__cursor = self.__conn.cursor()
        self.__returnedResult = []
    
    def select(self, command:str):
        self.__result=self.__cursor.execute("SELECT "+command)
        self.__conn.commit()
        for row in self.__result:
            self.__returnedResult.append(row)
        return self.__returnedResult
    
    def addClub(self, name, league):
        self.__cursor.execute(f'INSERT INTO Clubs(name, division) VALUES("{name}","{league}")')
        self.__conn.commit()
    
    def getLatestPlayerRecorded(self):
        self.__result=self.__cursor.execute("SELECT MAX(playerID) AS LatestRecordedPlayer FROM Players")
        for row in self.__result:
            return row[0]
    
    def checkClub(self, name):
        self.__result=self.__cursor.execute(f'SELECT clubID FROM Clubs WHERE name="{name}"')
        try:
            #try to return id of club otherwise it is added
            for row in self.__result:
                return row[0]
        except:
            return None
        
    def addPlayer(self, name, num):
        self.__cursor.execute(f'INSERT INTO Players(playerID,name) VALUES({num},"{name}")')
        self.__conn.commit()
    
    def checkPlayer(self, name):
        self.__result=self.__cursor.execute(f'SELECT playerID FROM Players WHERE name="{name}"')
        try:
            #try to return id of player otherwise they are added to db
            for row in self.__result:
                return row[0]
        except:
            return None
    
    def checkPlayerID(self, playerID):
        self.__result=self.__cursor.execute(f'SELECT playerID FROM Players WHERE playerID={playerID}')
        try:
            #try to return id of player otherwise they are added to db
            for row in self.__result:
                return row[0]
        except:
            return None
    
    def addPlayerSeason(self,playerID,clubID,year,apps,mins,goals,nPG,assists,xG,xNPG,xA,shotsPer90,keyPassPer90,yellowCards,redCards):
        self.__cursor.execute(f'INSERT INTO PlayerSeasons(playerID,clubID,year,apps,mins,goals,nPG,assists,xG,xNPG,xA,shotsPer90,keyPassPer90,yellowCards,redCards) VALUES({playerID},{clubID},"{year}",{apps},{mins},{goals},{nPG},{assists},{xG},{xNPG},{xA},{shotsPer90},{keyPassPer90},{yellowCards},{redCards})')
        self.__conn.commit()

    def checkPlayerSeason(self,playerID,clubID,year):
        self.__result=self.__cursor.execute(f'SELECT playerSeasonID FROM PlayerSeasons WHERE playerID={playerID} AND clubID={clubID} AND year="{year}"')
        try:
            #try to return id of player season otherwise the new one is added to db
            for row in self.__result:
                return row[0]
        except:
            return None
        
    def addPlayerPosition(self,playerID,position,year,apps,mins,goals,nPG,assists,xG,xNPG,xA,shotsPer90,keyPassPer90,yellowCards,redCards):
        self.__cursor.execute(f'INSERT INTO Positions(playerID,position,year,apps,mins,goals,nPG,assists,xG,xNPG,xA,shotsPer90,keyPassPer90,yellowCards,redCards) VALUES({playerID},"{position}","{year}",{apps},{mins},{goals},{nPG},{assists},{xG},{xNPG},{xA},{shotsPer90},{keyPassPer90},{yellowCards},{redCards})')
        self.__conn.commit()
    
    def checkPlayerPosition(self,playerID,position):
        self.__result=self.__cursor.execute(f'SELECT positionID FROM Positions WHERE playerID={playerID} AND clubID={clubID} AND year="{year}" AND position="{position}"')
        try:
            #try to return id of position player otherwise new position is added to db
            for row in self.__result:
                return row[0]
        except:
            return None

def getName(dri):
    return dri.find_element(By.XPATH,"/html/body/div[1]/header/div").text

def removeSpaces(word,symbol):
    return word.replace(" ",symbol)

def getDivision(dri,teamName,year):#go to club season page, then find league stated by clicking link
    dri.get('https://understat.com/team/'+removeSpaces(teamName,"_")+'/'+year[:4])
    league = dri.find_element(By.XPATH,f"/html/body/div[1]/div[3]/ul/li[2]/a").text
    return league

def selectAdditionalStats(driver):#procedure
    #click options
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/button").click()
    #click labels - NPG, npXG, yellow cards, red cards
    wait=WebDriverWait(driver,15)
    wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[2]/div/div[7]/div[2]/label"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[2]/div/div[12]/div[2]/label"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[2]/div/div[23]/div[2]/label"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[2]/div/div[24]/div[2]/label"))).click()
    #apply changes
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[3]/a[2]").click()
    sleep(0.5)

def removeComp(x):
    for i in range (len(x)):
        if x[i] == '+' or x[i] == '-':
            return x[:i]
    return x

def recordSeason(database:Database,driver:webdriver,num:int,start:int):
    #get website then link and select additional stats
    link='https://understat.com/player/'+str(num)
    driver.get(link)
    if num==start:
        sleep(1)
        try:
            selectAdditionalStats(driver)
        except:
            print("404 error - player",num,"doesn't exist.")
            return
    sleep(0.1)
    try:
        playerName=getName(driver)
    except:
        print("404 error - player",num,"doesn't exist.")
        return
    #print(playerName)
    #get table for seasons on page
    try:
        selectSeasonsTable = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div/div[2]/table")
    except:
        print(f"Page internal table error at id {num}.")
        with open("noinfo.csv","a") as f:
            f.write(str(num)+","+playerName+'\n')
        return
    x=selectSeasonsTable.text.split('\n')
    col_names=x.pop(0).split(' ')
    #splits each row in the table into an individual season
    seasons=[]
    for season in x:
        seasons.append(season.split(' '))
    #removes total                
    seasons.pop(len(seasons)-1)
    for row in seasons:
        #makes the names 
        depth=findNameLength(row, 2, depth=2)
        clubName=row[2]
        for i in range (3, depth):
            clubName=clubName+"_"+str(row[i])
        for i in range (3, depth):
            row.remove(row[3])
        row[2]=clubName
        #removes +/-
        row[12]=float(removeComp(row[12]))
        row[11]=float(removeComp(row[11]))
        row[10]=float(removeComp(row[10]))
        for i in range (4,8):
            row[i]=int(row[i])
        for i in range (8,10):
            row[i]=float(row[i])
        for i in range (15,17):
            row[i]=int(row[i])        
    #retrieves or creates player ID
    playerID=database.checkPlayer(playerName)
    if playerID is None:
        database.addPlayer(playerName,num)
        playerID=database.checkPlayer(playerName)
    #adds each individual season to the db
    for season in seasons:
        #retrieves or creates club ID
        clubName=season[2].replace("_"," ")
        clubID=database.checkClub(clubName)
        if clubID is None:
            print(clubName)
            database.addClub(clubName,getDivision(driver,clubName,season[1]))
            clubID=database.checkClub(clubName)
        
        psID=database.checkPlayerSeason(playerID,clubID,season[1])
        if psID is None:
            database.addPlayerSeason(playerID,clubID,season[1],season[3],season[4],season[5],season[6],season[7],season[10],season[11],season[12],season[8],season[9],season[15],season[16])
    print(num,playerName)


