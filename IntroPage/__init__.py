from otree.api import *



doc = """
Introduction for the Arbitrage Simulation Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class ArbitrageLimit(Page):
    pass


page_sequence = [ArbitrageLimit]