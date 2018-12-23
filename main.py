#!/usr/bin/python3

from classes.game import Person, BColors
from classes.magic import Spell
from classes.inventory import Item


# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create potion items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer",
              "Fully restores HP/MP of one party member", 9999)
hi_elixer = Item("Mega-Elixer", "elixer",
                 "Fully restores party's HP/MP", 9999)

# Create attack item
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Organizing magic
player_magic = [fire, blizzard, thunder, meteor, quake, cure, cura]
player_items = [potion, hi_potion, super_potion, elixer,
                hi_elixer, grenade]
enemy_items = []
enemy_magic = []

# Instantiate people
player = Person(460, 65, 60, 34, player_magic, player_items)
enemy = Person(999, 65, 45, 25, enemy_magic, enemy_magic)

i = 0
running = True

print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" +
      BColors.ENDC)

while running:
    print("==========================================")
    player.choose_action()
    choice = input("Choose action (#): ")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage. Enemy HP:",
              enemy.get_hp())

    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose magic (#): ")) - 1

        # Enter 0 to go to previous menu
        if magic_choice == -1:
            continue

        # magic_dmg = player.generate_spell_damage(magic_choice)
        # spell = player.get_spell_name(magic_choice)
        # cost = player.get_spell_mp_cost(magic_choice)

        magic_dmg = player.magic[magic_choice].generate_damage()
        spell = player.magic[magic_choice]

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(BColors.FAIL + "\n Not enough MP\n" + BColors.ENDC)
            continue

        if spell.type == "white":
            player.heal(magic_dmg)
            print(BColors.OKBLUE + "\n" + spell.name + " heals for",
                  str(magic_dmg) + BColors.ENDC)

        elif spell.type == "black":
            # player.reduce_mp(spell.cost)
            enemy.take_damage(magic_dmg)
            print(BColors.OKBLUE + "\n " + spell.name + " deals",
                  str(magic_dmg),
                  "points of damage\n" + BColors.ENDC)

    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choose item: ")) - 1

        # Enter 0 to go to previous menu
        if item_choice == -1:
            continue

        item = player.items[item_choice]

        if item.type == "potion":
            player.heal(item.prop)
            print(BColors.OKGREEN + "\n" + item.name + " heals for",
                  str(item.prop), "HP" + BColors.ENDC)

    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("--------------------------------------------")
    print("Enemy HP:", BColors.FAIL + str(enemy.get_hp()) + "/" +
          str(enemy.get_max_hp()) + BColors.ENDC)

    print("Your HP:", BColors.OKGREEN + str(player.get_hp()) + "/" +
          str(player.get_max_hp()) + BColors.ENDC)

    print("Your MP:", BColors.OKBLUE + str(player.get_mp()) + "/" +
          str(player.get_max_mp()) + BColors.ENDC)

    if enemy.get_hp() == 0:
        print(BColors.OKGREEN + "You win!" + BColors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(BColors.FAIL + "You've been defeated!" + BColors.ENDC)
        running = False
