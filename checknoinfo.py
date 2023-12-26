from understat_player_seasons import *
import csv

db = Database('info.db')

def deleteRecordedPlayers(db,file_name):
    recordedplayers=set()
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            line = line.split(",")
            player_id = line[0]
            flag = db.playerHasSeasons(player_id)
            if flag==True:
                recordedplayers.add(player_id)

    #delete line if id is in set
    with open(file_name,"r") as f:
        reader=csv.reader(f)
        rows=[row for row in reader if row[0] not in recordedplayers]
    with open(file_name,"w") as f:
        writer=csv.writer(f)
        writer.writerows(rows)

#delete duplicates
def deleteDuplicates(file_name):
    with open(file_name,"r") as f:
        reader=csv.reader(f)
        rows=[row for row in reader]
        rows=list(set([tuple(row) for row in rows]))
    with open(file_name,"w") as f:
        writer=csv.writer(f)
        writer.writerows(rows)