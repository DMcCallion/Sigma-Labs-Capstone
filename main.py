import random


#Should I use class/objects for this? 
# if I want to calculate player attacks on monsters as well it might be easiest to group them all in a 'creature' class
player_stats = {
    "Player 1" : [100,20, 0], # [hp, ac, expected hits to death]
    "Player 2" : [50,15, 0]
}
monster_stats = {
    "Dice" : 6,
    "Mod" : 3
}

def dice_roll(sides, mod):
    return random.randint(1,sides) + mod

def check_hit(target, mod):
    roll = random.randint(1,20)
    if roll == 20: #critical hits calculate damage differently or I could just return true/false
        return 2
    elif roll == 1: #rolling 1 automatically misses (this rarely comes into play )
        return 0
    elif roll + mod >= target:
        return 1
    return 0



def calc_damage(hit, dice, mod):
    damage = 0
    if hit == 2: #when you crit, double the dice roll but not the modifier in damage calculation
        damage += (2 * random.randint(1,dice)) + mod
        
    elif hit == 1:
        damage += random.randint(1,dice) + mod
    return damage


#see Readme - hitrate if this is confusing
def calc_hitrate(target, mod):
    effective_ac = target - mod #needing to roll a 10 + 5 to hit 15 is the same as needing to roll a 10 to hit 15 - 5
    
    effective_ac = max(effective_ac,2)
    effective_ac = min(effective_ac,20)
    #if we go below 2 or above 20, we'll be getting % chances to hit below 5% or above 95% 
    # but since 1 and 20 on the dice roll auto miss/hit, there should always be at least a 5% chance to hit/miss

    
    hitrate = (21 - effective_ac) / 20 # 21 looks weird here, but it's due to rolling the same as ac counting as a hit
    return hitrate 



def predict_attacks_to_death(HP, AC, dice, mod):
    hitrate = calc_hitrate(AC, mod)
    avg_damage = (1+dice)/2 + mod

    expected_damage = hitrate * avg_damage 
    # if your attack averages 10 dmg, but only has 50% hitrate, each attack would be expected to do 5

    count = 0 
    total_expected_damage = 0
    while total_expected_damage < HP:
        total_expected_damage += expected_damage
        count += 1
    return count


#checking if you hit with an attack in 5e requires a d20 roll plus your modifier, compared to the target's defense (Armor Class)



# def ask_for_target():
#     user_target = input("Please enter an armor class target:")
#     return int(user_target)

# def ask_attack_count():
#     attack_count = input("How many attacks should be rolled?:")
#     return int(attack_count)

# def ask_dice_size():
#     num_sides = input("What size dice should be used to calculate damage?:")
#     return int(num_sides)

# def ask_attack_mod():
#     mod = input("Please enter attack modifier:")
#     return int(mod)



# def single_target_calc():
#     target = ask_for_target()
#     attacks = ask_attack_count()
#     mod = ask_attack_mod()
#     dice = ask_dice_size()
#     hits = 0
#     damage = 0
    
#     for i in range(attacks):
#         if check_hit(target, mod):
#             hits += 1

#     for j in range(hits):
#         damage += dice_roll(dice, mod)

#     return f"You got {hits} hits against AC {target}, for a total of {damage} damage"


#print(single_target_calc())
print(calc_hitrate(18,5))

print(predict_attacks_to_death(100, 18, 6, 5))