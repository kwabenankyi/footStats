#close connections to db
import sqlite3
import understat_player_seasons

db = understat_player_seasons.Database('info.db')
db.close()

