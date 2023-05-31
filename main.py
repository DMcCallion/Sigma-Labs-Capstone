import random

player1 = {
    "HP" : 100,
    "AC" : 20
}
player2 = {
    "HP" : 50,
    "AC" : 15
}

def dice_roll(sides, mod):
    return random.randint(1,sides) + mod

def check_hit(target, mod):
    roll = dice_roll(20, mod) 
    if roll >= target:
        return True
    return False

#checking if you hit with an attack in 5e requires a d20 roll plus your modifier, compared to the target's defense (Armor Class)
def ask_for_target():
    user_target = input("Please enter an armor class target:")
    return int(user_target)

def ask_attack_count():
    attack_count = input("How many attacks should be rolled?:")
    return int(attack_count)

def ask_dice_size():
    num_sides = input("What size dice should be used to calculate damage?:")
    return int(num_sides)

def ask_attack_mod():
    mod = input("Please enter attack modifier:")
    return int(mod)


def single_target_calc():
    target = ask_for_target()
    attacks = ask_attack_count()
    mod = ask_attack_mod()
    dice = ask_dice_size()
    hits = 0
    damage = 0
    
    for i in range(attacks):
        if check_hit(target, mod):
            hits += 1

    for j in range(hits):
        damage += dice_roll(dice, mod)

    return f"You got {hits} hits against AC {target}, for a total of {damage} damage"


print(single_target_calc())