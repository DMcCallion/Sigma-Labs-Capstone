import random


#Should I use class/objects for this? 
# if I want to calculate player attacks on monsters as well it might be easiest to group them all in a 'creature' class

class creature:
    def __init__(self, HP, AC, Dice, Mod, Quantity):
        self.HP = HP
        self.AC = AC
        self.Dice = Dice
        self.Mod = Mod
        self.Quantity = Quantity

barbarian = creature(100, 15, 12, 9, 1)
wizard = creature(45, 18, 10, 9, 1)
zombies = creature(8, 10, 3, 4, 20)



def dice_roll(creature):
    return random.randint(1,creature.Dice) + creature.Mod

def check_hit(attacker, defender):
    roll = random.randint(1,20)
    if roll == 20: #critical hits calculate damage differently or I could just return true/false
        return 2
    elif roll == 1: #rolling 1 automatically misses (this rarely comes into play )
        return 0
    elif roll + attacker.mod >= defender.AC:
        return 1
    return 0



def calc_damage(hit, attacker):
    damage = 0
    if hit == 2: #when you crit, double the dice roll but not the modifier in damage calculation
        damage += (2 * random.randint(1,attacker.Dice)) + attacker.Mod
        
    elif hit == 1:
        damage += random.randint(1, attacker.Dice) + attacker.Mod
    return damage


#see Readme - hitrate if this is confusing
def calc_hitrate(attacker, defender):
    effective_ac = defender.AC - attacker.Mod #needing to roll a 10 + 5 to hit 15 is the same as needing to roll a 10 to hit 15 - 5
    
    effective_ac = max(effective_ac,2)
    effective_ac = min(effective_ac,20)
    #if we go below 2 or above 20, we'll be getting % chances to hit below 5% or above 95% 
    # but since 1 and 20 on the dice roll auto miss/hit, there should always be at least a 5% chance to hit/miss

    
    hitrate = (21 - effective_ac) / 20 # 21 looks weird here, but it's due to rolling the same as ac counting as a hit
    return hitrate 


def predict_attacks_to_death(attacker, defender):
    hitrate = calc_hitrate(attacker, defender)
    avg_damage = (1+attacker.Dice)/2 + attacker.Mod

    expected_damage = hitrate * avg_damage 
    # if your attack averages 10 dmg, but only has 50% hitrate, each attack would be expected to do 5

    count = 0 
    total_expected_damage = 0
    while total_expected_damage < defender.HP:
        total_expected_damage += expected_damage
        count += 1
    return count

#I want to make some options for the user in terms of targetting: 
#target lowest/highest attacks to death, and target random


def dangerous_targets(attacker, defender):
    print(barbarian.HP)

def safe_targets(attacker, defender):
    pass

def random_targets(attacker, defender):
    pass



print(predict_attacks_to_death(zombies, barbarian))
dangerous_targets(1,2)