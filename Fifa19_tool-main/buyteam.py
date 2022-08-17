""" TODO:
- turn player to player id
"""

import fut

def completesbd(players):
    global session
    session = fut.Core(email="sizzlingtrader2@gmail.com", passwd="", secret_answer="aaaa", platform='ps4',
                       debug=True)
    totalcosts = 0
    count = 1
    for i in players:
        playeri = minbin(i)
        totalcosts += playeri
        difference = playeri - i[1]
        i[1] = playeri
        count +=1
        print("the difference in costs for player ", count, " is ", difference)
    print("the total costs equal:", totalcosts)

    toContinue = input("Would you like to continue the purchase? (Y/N)")
    if toContinue=="Y":
        for i in players:
            buyplayers(i)
    else:
        print("Oke gf boi, better luck next time")
        return
    print("team bought check the results")


def choosesbc():
    sbcs = session.sbsSets()
    for c in sbcs['categories']:
        print(c['name'], len(c['sets']))
    category = input("which category?")
    for s in sbcs['categories']:
        if s['name'] == category:
            for c in s['sets']:
                print(c['setId'], c['description'])
    sbc = input("Welke wordt het?")
    return sbc


def inputplayers():
    print("how many players would you like to search?")
    amount = int(input())
    players = []
    for i in range(1, amount+1):
        extra = []
        print("Input player number ", i)
        extra.append(int(input()))
        print("Input maxbin of number ", i)
        extra.append(int(input()))
        players.append(extra)
    return players


def minbin(data):
    price = data[1]
    trye = 0
    while True:
        search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
        if len(search) <= 2:
            if price <= 950:
                price += 50
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            elif price <= 9900:
                price += 100
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            else:
                price += 250
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
        else:
            buynowprice = search[0]['buyNowPrice']
            break
    return buynowprice


def buyplayers(data):
    maxprice = 500000000000
    itemtobuy = -1
    price = data[1]
    trye = 0
    while True:
        search = session.searchAuctions(ctype="player", assetId=data[0], max_buy=price)
        if len(search) <= 2:
            if price <= 950:
                price += 50
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            elif price <= 9900 and price >=1000:
                price += 100
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            else:
                price += 250
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
        if len(search) >= 15:
            if price <= 1000:
                price -= 50
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            elif price <= 10000 and price >=1000:
                price -= 100
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
            else:
                price -= 250
                print("current price ", price)
                print("this is try ", trye)
                trye += 1
        for i in range(0, len(search) - 1):
            if search[i]['buyNowPrice'] <= maxprice:
                maxprice = search[i]['buyNowPrice']
                itemtobuy = i

        bidding = session.bid(trade_id=search[itemtobuy]['tradeId'], bid=maxprice, fast=True)
        print("bidding at ", maxprice, " bid was ", bidding)
        if bidding:
            unass = session.unassigned()
            begone = session.sendToClub(unass[0]['id'])
            print("item send to club: ", begone)
            break


def movetotradepile():
    sessions = fut.Core(email="sizzlingtrader2@gmail.com", passwd="Qmjcxrej1", secret_answer="aaaa", platform='ps4',
                       debug=True)
    unasss = sessions.unassigned()
    if len(unasss) == 0:
        print("unassigned is empty")
    else:
        for i in range(0, len(unasss)-1):
            sessions.sendToTradepile(unasss[i]['id'])
            print("moving item ", unasss[i]['id'], " to the trade pile")

    sessions.logout()


def removesolditems():
    session1 = fut.Core(email="sizzlingtrader2@gmail.com", passwd="Qmjcxrej1", secret_answer="aaaa", platform='ps4',
                       debug=True)
    tradables = session1.tradepile()
    for i in range(0, len(tradables)-1):
        if session1.tradeStatus(tradables[i]['tradeId'])[0]['tradeState'] == 'closed':
            session1.tradepileClear()
            tradables = session1.tradepile()
            print("Trade pile cleared")
            break
    session1.logout()

def listitems():
    session1 = fut.Core(email="sizzlingtrader2@gmail.com", passwd="Qmjcxrej1", secret_answer="aaaa", platform='ps4',
                       debug=True)
    tradables = session1.tradepile()
    for i in range(0, len(tradables)-1):
        if not tradables[i]['tradeState']:
            search = session1.searchAuctions(ctype="player", assetId=tradables[i]['assetId'])
            reference = 500000000000
            for j in range(0, len(search)-1):
                if search[j]['buyNowPrice'] <= reference:
                    reference = search[j]['buyNowPrice']
            if reference <= 950:
                correction = 50
            elif reference <= 9900 and reference>=1000:
                correction = 100
            else:
                correction = 250
            session1.sell(item_id=tradables[i]['id'], bid=max(reference-correction,
                                                        round(tradables[i]['discardValue'], -2)), buy_now=reference)
            print("item put up for auction @ ", max(reference-correction,
                                                        round(tradables[i]['discardValue'], -2)))

    session1.logout()