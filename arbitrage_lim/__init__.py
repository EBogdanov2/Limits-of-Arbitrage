from otree.api import *


doc = """
Arbitrage trading simulation.
Based on material presented:
July 8th 2023
Seminar for Behavioural Finance
Heidelberg University
"""

class C(BaseConstants):
    NAME_IN_URL = 'arbitrage_lim'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    INIT_FUND = 100
    INIT_PRICE = 10
    TRUE_VAL = 14
    DELTA = [-2,-2,-2,2]
    INVESTOR_PRESSURE = 0.70


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment = models.IntegerField(
        min = 0,
        max = C.INIT_FUND/C.INIT_PRICE
    )
    price = models.IntegerField()
    shares = models.IntegerField(initial = 0)
    funds = models.IntegerField(initial = C.INIT_FUND)
    shareval = models.IntegerField(initial = 0)
    portfolio = models.IntegerField(initial = 0)
    withdraw = models.IntegerField()

def pricechange():
    import random
    return C.DELTA[random.randint(0,3)]


def currprice(player):
    rnd = player.round_number
    prev = rnd - 1
    change = pricechange()
    print(change)
    if rnd == 1:
        player.price = C.INIT_PRICE

    elif rnd == 5:
        player.price = C.TRUE_VAL

    else:
        player.price = player.in_round(prev).price + change
    return player.price

def initvals(player):
    player.price = C.INIT_PRICE
    player.funds = C.INIT_FUND
    player.investment = 0
    player.shares = 0
    player.shareval = 0
    player.portfolio = 0
    player.withdraw = False

def changevals(player):
    rnd = player.round_number
    prev = rnd - 1

    if rnd == 1:
        player.investment = player.investment
        player.funds = player.funds - player.investment * player.price
        player.shareval = player.investment * player.price
        player.portfolio = player.shareval + player.funds

    else:
        if player.investment != 0:
            player.investment = player.in_round(prev).investment + player.investment
            player.funds = player.in_round(prev).funds - player.investment * player.price
            player.shareval = player.investment * player.price
            player.portfolio = player.shareval + player.funds
        else:
            player.investment = player.in_round(prev).investment
            player.funds = player.in_round(prev).funds
            player.shareval = player.investment * player.price
            player.portfolio = player.shareval + player.funds


    checkwithdraw(player)

def prevvals(player):
    rnd = player.round_number
    prev = rnd - 1

    currprice(player)

    player.investment = player.in_round(prev).investment
    player.funds = player.in_round(prev).funds
    player.shareval = player.in_round(prev).shareval
    player.portfolio = player.in_round(prev).portfolio


def checkwithdraw(player):
    if player.portfolio < C.INIT_FUND*C.INVESTOR_PRESSURE:
        player.withdraw = True
    else:
        player.withdraw = False



#class Changes(ExtraModel):
#    player = models.Link(Player)
#    price = models.IntegerField(init = C.INIT_PRICE)
#    shares = models.IntegerField()
#    funds = models.IntegerField()

class Trading_T1(Page):

    form_model = 'player'
    form_fields = ['investment']

    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            initvals(player)
        else:
            prevvals(player)

    @staticmethod
    def before_next_page(player, timeout_happened):
        changevals(player)


class Liquidation(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.withdraw == True
        #prev = player.round_number - 1
        #if prev == 0:
        #    pass
        #else:
        #    return player.withdraw == True



page_sequence = [Trading_T1,Liquidation]
