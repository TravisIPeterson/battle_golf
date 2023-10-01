import random

def drive(player):
    if player.position == 'driver':
        success_prob = (player.power + player.accuracy) / 20.0
    else:
        success_prob = (player.power + player.accuracy) / 40.0
    return random.random() < success_prob

def block(player):
    if player.position == 'blocker':
        success_prob = (player.balance + player.power + player.solidity) / 30.0
    else:
        success_prob = (player.balance + player.power + player.solidity) / 60.0
    return random.random() < success_prob

def precision_hit(player):
    if player.position == 'marksman':
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 30.0
    else:
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 60.0
    return random.random() < success_prob

def movement(player):
    success_prob = (player.speed + player.balance) / 20.0
    return random.random() < success_prob

def passing(player):
    success_prob = (player.accuracy + player.charisma) / 20.0
    return random.random() < success_prob

def diving(player):
    success_prob = (player.speed + player.balance + player.solidity) / 30.0
    return random.random() < success_prob

def offer_bribe(player):
    success_prob = (player.greed + player.integrity) / 20.0
    return random.random() < success_prob

def resist_bribe(player):
    success_prob = (player.integrity + player.cowardice) / 20.0
    return random.random() < success_prob

def hit(player):
    success_prob = (player.power + player.savagery) / 20.0
    return random.random() < success_prob