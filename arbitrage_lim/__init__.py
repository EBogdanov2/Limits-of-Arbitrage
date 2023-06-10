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
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    price = models.IntegerField()
    shares = models.IntegerField(init = 0)
    funds = models.IntegerField(init = C.INIT_FUND)
    shareval = models.IntegerField(init = 0)
    portfolio = models.IntegerField(init = 0)
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

    currprice(player)

    player.investment = player.in_round(1).investment
    player.funds = C.INIT_FUND - player.in_round(1).investment * player.in_round(1).price
    player.shareval = player.investment * player.price
    player.portfolio = player.shareval + player.funds

    checkwithdraw(player)

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
