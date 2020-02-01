import urllib
import xmltodict
import json
import time

theList = list()

for bggindex in range(1,300000):
    time.sleep(1)    
    while True:
        print(bggindex,len(theList))
        url = 'http://www.boardgamegeek.com/xmlapi/boardgame/'+ str(bggindex) + '?stats=1'
        data = ''
        try:
            #print("urllib.request.urlopen(url)....")
            file = urllib.request.urlopen(url,None,5)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
        except:
            print(data)  
            print("invalid xml data parse, try again....")
            time.sleep(5)
            continue
        break

    if('boardgames' not in data):
        print('boardgames not found in data')
        continue
    if('boardgame' not in data['boardgames']):
        print('boardgame not found in boardgames')
        continue
    if('name' not in data['boardgames']['boardgame']):
        print('name not found')
        continue
    namedata = data['boardgames']['boardgame']['name']
    name = ''
    #print(namedata)
    if('#text' in namedata):
        name = namedata['#text']
    else:
        try:
            name = namedata[0]['#text']
        except:
            pass
        for nameIndex in range(0,len(namedata)):
            try:
                if('true' == namedata[nameIndex]['@primary']):
                    name = namedata[nameIndex]['#text']
                    break
            except:
                pass
    if(name == ''):
        print('name not found')
        continue
    #print('name = ',name)
    rank = ''
    #print(json.dumps(data))
    try:
        if('@value' in data['boardgames']['boardgame']['statistics']['ratings']['ranks']['rank']):
            rank = data['boardgames']['boardgame']['statistics']['ratings']['ranks']['rank']['@value']
        elif('@value' in data['boardgames']['boardgame']['statistics']['ratings']['ranks']['rank'][0]):
            rank = data['boardgames']['boardgame']['statistics']['ratings']['ranks']['rank'][0]['@value']
        else:
            pass
    except:
        print("no statistics")
    try:
        rank = int(rank)
    except:
        print("not ranked")
        continue
    #print('rank =',rank)
    pollarray = data['boardgames']['boardgame']['poll']
    for pollIndex in range(0,len(pollarray)):
        pollname = pollarray[pollIndex]['@name']
        if(pollname == 'suggested_numplayers'):
            results = pollarray[pollIndex]['results']
            #print(json.dumps(results))
            break
    
    pollResults = []
    if('@numplayers' not in results):
        for threePlayerIndex in range(0,len(results)):
            #print(threePlayerIndex)
            numplayers = results[threePlayerIndex]["@numplayers"]
            if(numplayers == '3'):
                pollResults = results[threePlayerIndex]['result']
                break
    elif (results['@numplayers'] == '3'):
        best = 1
    else:
        print("three players not found")

    #print(json.dumps(pollResults))
    best = -1
    recommended = -1
    not_recommended = -1

    for pollResultIndex in range(0,len(pollResults)):
        if(pollResults[pollResultIndex]['@value'] == 'Best'):
            try:
                best = int(pollResults[pollResultIndex]['@numvotes'])
            except:
                pass
        elif(pollResults[pollResultIndex]['@value'] == 'Recommended'):
            try:
                recommended = int(pollResults[pollResultIndex]['@numvotes'])
            except:
                pass
        elif(pollResults[pollResultIndex]['@value'] == 'Not Recommended'):
            try:
                not_recommended = int(pollResults[pollResultIndex]['@numvotes'])
            except:
                pass
        else:
            print('unhandled ' ,pollResults[pollResultIndex]['@numvotes'])

    #print(best)
    #print(recommended)
    #print(not_recommended)

    if best > 3 and best > recommended and best > not_recommended:
        theList.append([rank,name,bggindex])
        theList.sort()
        #print(theList)
        f = open("list.txt","w")
        for s in theList:
            f.write(str(s)+"\n")
            print(s)
        f.close()

print(theList)