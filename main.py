import random


class creature:
    def __init__(self, Name, HP, AC, Dice, Mod, Quantity, Hits_to_death, Hits_taken):
        self.Name = Name
        self.HP = HP
        self.AC = AC
        self.Dice = Dice
        self.Mod = Mod
        self.Quantity = Quantity
        self.Hits_to_death = Hits_to_death
        self.Hits_taken = Hits_taken

fighter = creature("Fighter", 60, 18, 12, 5, 1, 0, 0)
wizard = creature("Wizard", 20, 16, 10, 5, 1, 0, 0)
rogue = creature("Rogue", 30, 17, 6, 5, 1, 0, 0)
cleric = creature("Cleric", 45, 20, 6, 2, 1, 0, 0)


zombies = creature("Zombie", 22, 8, 6, 3, 15, 0, 0)
gnolls = creature("Gnoll", 22, 15, 8, 2, 11, 0, 0)

party = [fighter, wizard, rogue, cleric]




def dice_roll(creature):
    return random.randint(1,creature.Dice) + creature.Mod

def check_hit(attacker, defender):
    roll = random.randint(1,20)
    if roll == 20: #critical hits calculate damage differently or I could just return true/false
        defender.Hits_taken += 1
        return 2
    elif roll == 1: #rolling 1 automatically misses (this rarely comes into play )
        return 0
    elif roll + attacker.Mod >= defender.AC:
        defender.Hits_taken += 1
        return 1
    return 0



def calc_damage(hit, attacker):
    damage = 0
    if hit == 2: #when you crit, double the dice roll but not the modifier in damage calculation
        damage += (2 * random.randint(1,attacker.Dice)) + attacker.Mod
        
    elif hit == 1:
        damage += random.randint(1, attacker.Dice) + attacker.Mod
    return damage


def apply_damage(damage, defender):
    defender.HP -= damage

def attack(attacker, defender):
    hit = check_hit(attacker,defender)
    damage = calc_damage(hit, attacker)
    apply_damage(damage, defender)

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


def assign_hits_to_death(attacker, party):
    for member in party:
        member.Hits_to_death = predict_attacks_to_death(attacker, member)
    party.sort(key = lambda x: x.Hits_to_death)



#Below are functions for choosing targets from the party to attack (and applying the attacks)
'''
This is for enemies that employ hyena style tactics, picking off the weakest member
alternatively if the monsters are looking to capture the players this is a good option

It's tactically the best option - give yourself a numbers advantage ASAP - 
but if you only use this one your wizard player will not have much fun
'''
def dangerous_targets(attacker, party):
    attacks_made = 0
    while attacks_made < attacker.Quantity: 
        #There's got to be a better option than manually working through each party member like this
        if party[0].HP > 0:
            attack(attacker, party[0])
        elif party[1].HP > 0:
            attack(attacker, party[1])
        elif party[2].HP > 0:
            attack(attacker, party[2])
        elif party[3].HP > 0:
            attack(attacker, party[3])

        attacks_made += 1


'''
This option hits the target who can take the most hits
it kind of replicates what dumb brutes like an ogre / horde of zombies etc would use. 
In a typical party composition this has the monsters hitting the fighter or cleric 
who are right in front of them, not the wizard standing 30 feet behind.
 '''
def safe_targets(attacker, party):
    attacks_made = 0
    while attacks_made < attacker.Quantity: 
        #There's got to be a better option than manually working through each party member like this
        if party[-1].HP > 0:
            attack(attacker, party[-1])
        elif party[-2].HP > 0:
            attack(attacker, party[-2])
        elif party[-3].HP > 0:
            attack(attacker, party[-3])
        elif party[-4].HP > 0:
            attack(attacker, party[-4])
        assign_hits_to_death(attacker, party)
        attacks_made += 1


'''
For a disorganized crowd who will each pick their own target. e.g. a bunch of goblins
'''
def random_targets(attacker, defender):
    pass




#tests below


assign_hits_to_death(zombies, party)
for member in party:
    print(f"{member.Name} HP: {member.HP}, #attacks to knock out:{member.Hits_to_death}")
    

safe_targets(zombies, party)


for member in party:
    print(f"{member.Name} took {member.Hits_taken} hits. Current HP:{member.HP}")