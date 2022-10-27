"""check price for player
how to run:
- import required definitions: from sbc import completesbd
- run the required modules
TODO:
- fix quicksell to take care of informs
"""



def login():
    global fut
    import fut
    global time
    import time
    print("Logging in...")
    global session
    session = fut.Core(email="sizzlingtrader2@gmail.com", passwd="", secret_answer="aaaa", platform='ps4',
                       debug=True)
    print("Login successfull!")


def completesbc():
    """Determines the price, buys (if satisfies with price) and assigned players to correct sbc"""
    players = inputplayers()
    totalcosts = 0
    pricesandplayers = []
    for i in players:
        extra = []
        playeri = minbin(i)
        extra.append(i)
        extra.append(playeri)
        totalcosts += playeri
        pricesandplayers.append(extra)
    count = 0
    for j in pricesandplayers:
            print(count, session.cardInfo(j[0])['lastname'], session.cardInfo(j[0])['rating'], j[1])
            count += 1
    print("the total costs equal:", totalcosts)
    while True:
        howmanyplayerswap = int(input("How many players would you like to swap?"))
        if howmanyplayerswap == 0:
            print("cool!")
            break
        elif howmanyplayerswap == 1:
            playertoswap = int(input("which player would you like to swap"))
            for d in pricesandplayers:
                if d[0] == players[playertoswap]:
                    totalcosts -= d[1]
                    print("for which player would you like to swap", session.cardInfo(d[0])['lastname']
                          , session.cardInfo(d[0])['rating'])
                    while True:
                        swapeeid = findplayer()
                        if not swapeeid:
                            print("Match not found (insert new name)")
                            continue
                        tocont = input('Correct? (y/n)')
                        if tocont == 'n':
                            continue
                        else:
                            break
                    swapeeprice = minbin(swapeeid)
                    d[0] = swapeeid
                    d[1] = swapeeprice
                    totalcosts += d[1]
        else:
            for o in range(1, howmanyplayerswap):
                playertoswap = int(input("which player would you like to swap"))
                for d in pricesandplayers:
                    if d[0] == players[playertoswap]:
                        totalcosts -= d[1]
                        print("for which player would you like to swap", session.cardInfo(d[0])['lastname']
                              , session.cardInfo(d[0])['rating'])
                        while True:
                            swapeeid = findplayer()
                            if not swapeeid:
                                print("Match not found (insert new name)")
                                continue
                            tocont = input('Correct? (y/n)')
                            if tocont == 'n':
                                continue
                            else:
                                break
                        swapeeprice = minbin(swapeeid)
                        d[0] = swapeeid
                        d[1] = swapeeprice
                        totalcosts += d[1]
        count = 0
        for j in pricesandplayers:
            print(count, session.cardInfo(j[0])['lastname'], session.cardInfo(j[0])['rating'], j[1])
            count += 1
        print("the total costs equal:", totalcosts)
        toContinue = input("would you want to change some other players?")
        if toContinue == 'y':
            continue
        else:
            break
    tobuy = input ("Would you want purchase this squad? (y/n)")
    if tobuy == 'y':
        for i in pricesandplayers:
            buyplayers(i)
        print("Done, check the club (;")
    else:
        print("Oke jammer, better luck next time")
        return
    """sbc = choosesbc()
    playerinclub = session.club(ctype='player')
    for i in players:
        for j in range(0, len(playerinclub)-1):
            if playerinclub[j]['assetId'] == i:
                print(i)
                global sbcitemid
                sbcitemid = playerinclub[j]['id']
        session.sendToSbs(sbc, sbcitemid)
        print("Player ", sbcitemid, " send to sbc ", sbc)
    print("sbc completed check the results")
"""


def inputplayers():
    """Asks the user to input players"""
    print("how many players would you like to search?")
    amount = int(input())
    players = []
    for i in range(1, amount+1):
        print("Getting player number ", i)
        while True:
            extra = findplayer()
            if not extra:
                print("Match not found look at the name please")
                continue
            tocont = input('Correct? (y/n)')
            if tocont == 'n':
                continue
            else:
                players.append(extra)
                break
    return players


def findplayer():
    players = session.players
    name = input("input last name")
    possibleplayers = []
    possibleplayers2 = []
    ids = None
    inputfirst = ""
    for i in players.values():
        if i['lastname'] == name:
            possibleplayers.append(i)
    if len(possibleplayers) == 1:
        print("match found! ", possibleplayers[0]['firstname'], possibleplayers[0]['lastname'],
                  possibleplayers[0]['rating'], possibleplayers[0]['id'])
        ids = possibleplayers[0]['id']
    elif len(possibleplayers) == 0:
        print("No match try again")
        return
    else:
        for j in possibleplayers:
            print(j['rating'], j['firstname'], j['lastname'], j['id'])
        inputrating = int(input("Too many choices, please insert rating of player"))
        for x in possibleplayers:
            if x['rating'] == inputrating:
                possibleplayers2.append(x)
        if len(possibleplayers2) == 1:
            print("match found! ", possibleplayers2[0]['firstname'], possibleplayers2[0]['lastname'],
                  possibleplayers2[0]['rating'], possibleplayers2[0]['id'])
            ids = possibleplayers2[0]['id']
        else:
            for b in possibleplayers2:
                print(b['rating'], b['firstname'], b['lastname'], b['id'])
            inputfirst = input("Too many choices, please insert first name of player")
            for a in possibleplayers2:
                if a['firstname'] == inputfirst:
                    print("match found! ", a['firstname'], a['lastname'],
                          a['rating'], a['id'])
                    ids = a['id']
    return ids


def choosesbc():
    session = fut.Core(email="sizzlingtrader2@gmail.com", passwd="Qmjcxrej1", secret_answer="aaaa", platform='ps4',
                       debug=True)
    sbcs = session.sbsSets()
    for c in sbcs['categories']:
        print(c['name'], len(c['sets']))
    category = input("which category?")
    for s in sbcs['categories']:
        if s['name'] == category:
            for c in s['sets']:
                print(c['setId'], c['name'])
    subcategory = input("which sub-category?")
    subs = session.sbsSetChallenges(subcategory)
    for v in subs['challenges']:
        print(v['challengeId'], v['name'], v['status'])
    sbc = input("Welke wordt het?")
    return sbc


def minbin(data):
    """Determines minimum price of a player on the market"""
    print("determining minimum price for", session.cardInfo(data)['lastname'], session.cardInfo(data)['rating'])
    trye = 1
    global maxprice
    maxprice = 15000000
    oldmax = 0
    search = session.searchAuctions(ctype="player", assetId=data)
    for p in range(0, len(search) - 1):
        if search[p]['buyNowPrice'] <= maxprice:
            maxprice = search[p]['buyNowPrice']
    if not 2 < len(search) < 16:
        while True:
            print("Waiting 3 seconds...")
            time.sleep(3)
            if not trye > 4:
                print("searching the market with max buy now set to", maxprice)
                search = session.searchAuctions(ctype="player", assetId=data, max_buy=maxprice)
                if len(search) <= 2:
                    if maxprice >= 100000:
                        maxprice += 1000
                        print("No results/snipe for ", maxprice, " on try ",trye," updating price to real price...")
                        trye += 1
                        continue
                    elif maxprice >= 50000:
                        maxprice += 500
                        print("No results/snipe for ", maxprice, " on try ",trye," updating price to real price...")
                        trye += 1
                        continue
                    elif maxprice >= 10000:
                        print("No results/snipe for ", maxprice, " on try ",trye," updating price to real price...")
                        trye += 1
                        maxprice += 250
                        continue
                    elif maxprice >= 1000:
                        print("No results/snipe for ", maxprice, " on try ",trye," updating price to real price...")
                        trye += 1
                        maxprice += 100
                        continue
                    else:
                        maxprice += 50
                        print("No results/snipe for ", maxprice, " on try ",trye," updating price to real price...")
                        trye += 1
                        continue
                if len(search) > 15:
                    print("Determining the price, try ", trye, " found price:", maxprice)
                    trye += 1
                    oldmax = maxprice
                    for p in range(0, len(search) - 1):
                        if search[p]['buyNowPrice'] <= maxprice:
                            maxprice = search[p]['buyNowPrice']
                    if oldmax == maxprice:
                        if maxprice > 100000:
                            maxprice -= 1000
                            print("updated price -1000")
                            continue
                        elif maxprice > 50000:
                            maxprice -= 500
                            print("updated price -500")
                            continue
                        elif maxprice > 10000:
                            print("updated price -250")
                            maxprice -= 250
                            continue
                        elif maxprice > 1000:
                            print("updated price -100")
                            maxprice -= 100
                            continue
                        else:
                            maxprice -= 50
                            print("updated price -50")
                            continue
                    else:
                        print("price updated to: ",maxprice)
                        continue
                else:
                    print("price after try:", trye, "equals:", maxprice)
                    break
            else:
                print("maximum amount of tries reached, min is ", maxprice)
                break
    else:
        print("instantly determined price to be: ", maxprice)
    buynowprice = maxprice
    return buynowprice


def buyplayers(data):
    """Buys players at specified price"""
    print("Buying player", session.cardInfo(data[0])['lastname'], session.cardInfo(data[0])['rating'])
    global maxprice2
    price = data[1]
    trye = 1
    while True:
        if not trye > 4:
            search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
            if len(search) == 0:
                if price >= 100000:
                    price += 1000
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
                elif price >= 50000:
                    price += 500
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
                elif price >= 10000:
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    price += 250
                    continue
                elif price >= 1000:
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    price += 100
                    continue
                else:
                    price += 50
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
            if len(search) >= 16:
                if price >= 100000:
                    price -= 1000
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
                elif price >= 50000:
                    price -= 500
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
                elif price >= 10000:
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    price -= 250
                    continue
                elif price >= 1000:
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    price -= 100
                    continue
                else:
                    price -= 50
                    print("current price ", price)
                    print("this is try ", trye)
                    trye += 1
                    continue
            else:
                itemtobuy = -1
                for i in range(0, len(search) - 1):
                    if search[i]['buyNowPrice'] <= price:
                        global maxprice5
                        maxprice5 = search[i]['buyNowPrice']
                        itemtobuy = i
                bidding = session.bid(trade_id=search[itemtobuy]['tradeId'], bid=maxprice5, fast=True)
                print("bidding at ", maxprice5, " bid was ", bidding)
                if not bidding:
                    continue
                elif bidding:
                    unass = session.unassigned()
                    if len(unass) == 0:
                        print("item could not be send at this moment")
                    else:
                        begone = session.sendToClub(unass[0]['id'])
                        print("item send to club: ", begone)
                        return
        else:
            search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
            if len(search) == 0:
                if price >= 100000:
                    price += 1000
                    search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
                elif price >= 50000:
                    price += 500
                    search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
                elif price >= 10000:
                    price += 250
                    search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
                elif price >= 1000:
                    price += 100
                    search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
                else:
                    price += 50
                    search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
            for i in range(0, len(search)-1):
                if search[i]['buyNowPrice'] <= price:
                    global maxprice6
                    maxprice6 = search[i]['buyNowPrice']
                    global itemtobuy2
                    itemtobuy2 = i
            bidding = session.bid(trade_id=search[itemtobuy2]['tradeId'], bid=maxprice6, fast=True)
            print("bidding at ", maxprice6, " bid was ", bidding)
            if not bidding:
                continue
            elif bidding:
                unass = session.unassigned()
                if len(unass) == 0:
                    print("item could not be send at this moment")
                else:
                    begone = session.sendToClub(unass[0]['id'])
                    print("item send to club: ", begone)
                    return


'''TOOLS'''


def movetotradepile():
    print("Logging in...")
    session = fut.Core(email="sizzlingtrader2@gmail.com", passwd="Qmjcxrej1", secret_answer="aaaa", platform='ps4',
                       debug=True)
    print("login succesfull!")
    unasss = session.unassigned()
    if len(unasss) == 0:
        print("unassigned is empty")
    elif len(unasss) == 1:
        session.sendToTradepile(unasss[0]['id'])
        print("moving item ", session.cardInfo(unasss[0]['resourceId'])['lastname'],
              session.cardInfo(unasss[0]['resourceId'])['rating'], " to the trade pile")
    else:
        for i in range(0, len(unasss)-1):
            session.sendToTradepile(unasss[i]['id'])
            print("moving item ", session.cardInfo(unasss[i]['resourceId'])['lastname'],
                  session.cardInfo(unasss[i]['resourceId'])['rating'], " to the trade pile")


def removesolditems():
    tradables = session.tradepile()
    if len(tradables) == 1:
        if tradables[0]['tradeState'] == 'closed':
            session.tradepileClear()
            print("Trade pile cleared")
            return
        else:
            print("Tradepile contains noof sold items")
            return
    else:
        for i in range(0, len(tradables)-1):
            if tradables[i]['tradeState'] == 'closed':
                session.tradepileClear()
                print("Trade pile cleared")
                return
        else:
            print("Tradepile contains no sold items")
            return


def sellformin():
    removesolditems()
    tradables = session.tradepile()
    if len(tradables) == 1:
        if (not tradables[0]['tradeState']) or tradables[0]['tradeState'] == 'expired':
            player = [tradables[0]['assetId']]
            minimum_price = minbin(player[0])
            correction = 0
            if minimum_price > 100000:
                 correction += 1000
            elif minimum_price > 50000:
                correction += 500
            elif minimum_price > 10000:
                correction += 250
            elif minimum_price > 1000:
                correction += 100
            else:
                correction += 50
            sellprice = minimum_price-correction
            if minimum_price in [700, 650, 600] and tradables[0]['discardValue'] > 600:
                session.quickSell(tradables[0]['id'])
                print("sell value to low, quicksold @", tradables[0]['discardValue'])
            else:
                print(session.cardInfo(tradables[0]['assetId'])['lastname'],
                      session.cardInfo(tradables[0]['assetId'])['rating'], "put up for auction @ ", sellprice)
                session.sell(item_id=tradables[0]['id'],
                             bid=max(sellprice - correction, round(tradables[0]['discardValue'], -2)),
                             buy_now=sellprice)
    else:
        for i in range(0, len(tradables)):
            if (not tradables[i]['tradeState']) or tradables[i]['tradeState'] == 'expired':
                player = [tradables[i]['assetId']]
                minimum_price = minbin(player[0])
                correction = 0
                if minimum_price > 100000:
                    correction += 1000
                elif minimum_price > 50000:
                    correction += 500
                elif minimum_price > 10000:
                    correction += 250
                elif minimum_price > 1000:
                    correction += 100
                else:
                    correction += 50
                sellprice = minimum_price-correction
                if minimum_price in [700, 650, 600] and tradables[i]['discardValue'] > 599:
                    session.quickSell(tradables[i]['id'])
                    print("sell value to low, quicksold @", tradables[i]['discardValue'])
                    continue
                if minimum_price in [350, 400, 300] and tradables[i]['discardValue'] > 299:
                    session.quickSell(tradables[i]['id'])
                    print("sell value to low, quicksold @", tradables[i]['discardValue'])
                    continue
                else:
                    print(session.cardInfo(tradables[i]['assetId'])['lastname'],
                          session.cardInfo(tradables[i]['assetId'])['rating'], "put up for auction @ ", sellprice)
                    session.sell(item_id=tradables[i]['id'], bid=max(sellprice - correction,
                                                                     round(tradables[i]['discardValue'], -2)),
                                 buy_now=sellprice)
    print("All players listed!")
    session.logout()

