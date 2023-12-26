import sqlite3
conn = sqlite3.connect("info.db")
cursor = conn.cursor()
createPlayersTable = """
CREATE TABLE Players
(
playerID INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL
)"""

createClubsTable = """
CREATE TABLE Clubs
(
clubID INTEGER NOT NULL PRIMARY KEY,
name TEXT NOT NULL,
division TEXT NOT NULL
)"""

createSeasonsTable = """
CREATE TABLE PlayerSeasons
(
playerSeasonID INTEGER NOT NULL PRIMARY KEY,
playerID INTEGER NOT NULL,
clubID INTEGER NOT NULL,
year TEXT NOT NULL,
apps INTEGER NOT NULL,
mins INTEGER NOT NULL,
goals INTEGER NOT NULL,
nPG INTEGER NOT NULL,
assists INTEGER NOT NULL,
xG FLOAT NOT NULL,
xNPG FLOAT NOT NULL,
xA FLOAT NOT NULL,
shotsPer90 FLOAT NOT NULL,
keyPassPer90 FLOAT NOT NULL,
yellowCards INTEGER NOT NULL,
redCards INTEGER NOT NULL,
FOREIGN KEY (playerID) REFERENCES Players(playerID),
FOREIGN KEY (clubID) REFERENCES Clubs(clubID)
)
"""

createPositionsTable = """
CREATE TABLE Positions
(
positionID INTEGER NOT NULL PRIMARY KEY,
playerID INTEGER NOT NULL,
position TEXT NOT NULL,
year TEXT NOT NULL,
apps INTEGER NOT NULL,
mins INTEGER NOT NULL,
goals INTEGER NOT NULL,
nPG INTEGER NOT NULL,
assists INTEGER NOT NULL,
xG FLOAT NOT NULL,
xNPG FLOAT NOT NULL,
xA FLOAT NOT NULL,
xGChain FLOAT NOT NULL,
xGBuildup FLOAT NOT NULL,
shotsPer90 FLOAT NOT NULL,
keyPassPer90 FLOAT NOT NULL,
yellowCards INTEGER NOT NULL,
redCards INTEGER NOT NULL,
FOREIGN KEY (playerID) REFERENCES Players(playerID)
)"""

cursor.execute(createPlayersTable)
cursor.execute(createClubsTable)
cursor.execute(createSeasonsTable)
cursor.execute(createPositionsTable)
conn.commit()