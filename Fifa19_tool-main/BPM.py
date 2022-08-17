"""TODO: Find out about too many requests error when trying to quicksell (update script so it quicksells them all at once)
"""
def temporary():
    global actions
    global random
    import time
    import random
    actions = 0
    packcount = 0
    print("waiting an hour until everything expires")
    time.sleep(random.randint(3800, 4000))
    cleartradepile()

#Bronze pack method
def bpm():
    login()
    count = 1
    global actions
    global random
    actions = 0
    packcount = 0
    while True:
        try:
            session.tradepileClear()
        except Exception:
            pass
        try:
            session.relist()
        except Exception:
            pass
        actions += 1
        print("Actions updated: ", actions)
        tradepile = session.tradepile()
        print(" ")
        print(session.credits)
        print(" ")
        while len(tradepile)<93:
            if actions >450:
                print("Maximum amount of actions reached, sleeping for 30 mins, resetting actions")
                time.sleep(random.randint(900, 1800))
                login()
                actions = 0
            if packcount >4:
                print("opened 5 packs, sleeping for random time")
                time.sleep(random.randint(150, 250))
                packcount = 0
            print("Opening packs, sleeping 10-15 seconds")
            time.sleep(random.randint(20, 30))
            print("trying to open pack")
            openpack()
            packcount +=1
            tradepile = session.tradepile()
            actions += 1
            print("Actions updated: ", actions)
        print("finished buying packs, waiting 30 minutes")
        time.sleep(random.randint(2000,2200))
        print("finished sleeping")
        while True:
            login()
            print(" ")
            print(session.credits)
            print(" ")
            try:
                session.tradepileClear()
            except Exception:
                pass
            actions += 1
            print("Actions updated: ", actions)
            tradepile = session.tradepile()
            actions += 1
            print("Actions updated: ", actions)
            if len(tradepile)<75:
                actions +=1
                print("Actions updated: ",actions)
                print("Relisting items")
                try:
                    session.relist()
                except Exception:
                    pass
                print("Tradepile clear enough, reopening packs")
                actions += 1
                print("Actions updated: ", actions)
                break
            else:
                try:
                    session.relist()
                except Exception:
                    pass
                actions +=1
                print("Actions updated: ",actions)
                print("Relisting items")
                print("tradepile is full, waiting hour in to relist")
                time.sleep(random.randint(3000,3200))
                login()
                print(" ")
                print(session.credits)
                print(" ")
                try:
                    session.relist()
                except Exception:
                    pass
                actions = 0
                print("resetting actions")
                count +=1
                if count>1:
                    print("waiting an extra hour in order to check the transfer list since relistment max is reached")
                    time.sleep(random.randint(3200, 3500))
                    login()
                    cleartradepile()
                    count = 0
                continue

def login():
    global fut
    import fut
    global time
    import time
    global random
    import random
    print("Logging in...")
    global session
    session = fut.Core(email="sizzlingtrader2@gmail.com", passwd="", secret_answer="aaaa", platform='ps4',
                       debug=True)
    print("Login successfull!")

def openpack():
    global actions
    global random
    try:
        session.buyPack(100)
    except Exception:
        pass
    unasss = session.unassigned()
    actions +=1
    print("Actions updated: ", actions)
    for i in range(0, len(unasss)):
        print("Taking care of unassigned, waiting 10-15 secs")
        time.sleep(random.randint(10, 15))
        print("finished waiting")
        print("Actions updated: ", actions)
        actions += 1
        if unasss[i]['itemType'] == 'player':
            session.sendToTradepile(unasss[i]['id'])
            print("Player", i, "send to transferlist")
        elif unasss[i]['resourceId'] == 5002004:
            session.sendToTradepile(unasss[i]['id'])
            print("Rare condition card found, sending to transferlist")
        else:
            print("Quicksold item:", i)
            session.quickSell(unasss[i]['id'])
    try:
        session.tradepileClear()
    except Exception:
        pass
    tradelist = session.tradepile()
    actions += 2
    print("Actions updated: ", actions)
    print("Trying to list players")
    for i in range(0, len(tradelist)):
        if not tradelist[i]['tradeState']:
            if tradelist[i]['itemType'] == "player":
                actions += 1
                print("Actions updated: ", actions)
                price = minbin(tradelist[i]['assetId'])
                print("listing players waiting 10-15 seconds")
                time.sleep(random.randint(10,15))
                if price > 200:
                    try:
                        session.sell(item_id=tradelist[i]['id'], bid=150, buy_now=price)
                    except Exception:
                        pass
                    print("player", tradelist[i]['id'], "listed")
                else:
                    try:
                        session.sell(item_id=tradelist[i]['id'], bid=150, buy_now=200)
                        print("Selling player for minprice ",tradelist[i]['id'])
                    except Exception:
                        pass
            elif tradelist[i]['resourceId'] == 5002004:
                actions += 1
                print("Actions updated: ", actions)
                print("unassigned, waiting 10-15 secs")
                time.sleep(random.randint(10, 15))
                try:
                    session.sell(item_id=tradelist[i]['id'], bid=150, buy_now=800)
                    print("selling rare bronze fitness")
                except Exception:
                    pass
                print("listing rare bronze consumable")
    print("players listed")

def cleartradepile():
    login()
    global actions
    actions = 0
    try:
        session.tradepileClear()
    except Exception:
        pass
    tradelist = session.tradepile()
    for i in range(0, len(tradelist)-1):
        actions +=1
        print("Actions updated: ", actions)
        if tradelist[i]['itemType'] == 'player':
            price = minbin(tradelist[i]['assetId'])
            time.sleep(random.randint(10,15))
            if price > 200:
                session.sell(item_id=tradelist[i]['id'], bid=150, buy_now=price)
                print("player", tradelist[i]['id'], "listed")
            else:
                print("quicksold player",tradelist[i]['id'])
                try:
                    session.quickSell(tradelist[i]['id'])
                except Exception:
                    pass
        elif tradelist[i]['resourceId'] == 5002004:
            session.sell(item_id=tradelist[i]['id'], bid=150, buy_now=800)
            print("listing rare bronze consumable")

def minbin(data):
    global random
    global actions
    """Determines minimum price of a player on the market"""
    print("determining minimum price for", session.cardInfo(data)['lastname'], session.cardInfo(data)['rating'])
    trye = 1
    global maxprice
    maxprice = 15000000
    oldmax = 0
    search = session.searchAuctions(ctype="player", assetId=data)
    actions += 1
    print("Actions updated: ", actions)
    for p in range(0, len(search) - 1):
        if search[p]['buyNowPrice'] <= maxprice:
            maxprice = search[p]['buyNowPrice']
    if maxprice == 200:
        return maxprice
        actions += 1
        print("Actions updated: ", actions)
    if not 2 < len(search) < 16:
        while True:
            print("Waiting 5-15 seconds")
            time.sleep(random.randint(5,15))
            actions +=1
            print("Actions updated: ", actions)
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
                    print("Price found after try", trye, "price fequals:", maxprice)
                    break
            else:
                print("maximum amount of tries reached, min is ", maxprice)
                break
    else:
        print("instantly determined price to be: ", maxprice)
    buynowprice = maxprice
    return buynowprice

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

