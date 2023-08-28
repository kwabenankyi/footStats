def findNameLength(row,start,depth=0):
    try:
        if row[start][0]=="0":
            depth=findNameLength(row,start+1,depth+1)
        else:
            try:
                if (int(row[start]) > 40):
                    depth=findNameLength(row,start+1,depth+1)
            except:
                depth=findNameLength(row,start+1,depth+1)
    except:
        depth=findNameLength(row,start+1,depth+1)
    return depth 