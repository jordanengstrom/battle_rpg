#!/usr/bin/python3

from classes.game import Person, BColors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 30, 950, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Create potion items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer",
              "Fully restores HP/MP of one party member", 9999)
hi_elixer = Item("Mega-Elixer", "elixer",
                 "Fully restores party's HP/MP", 9999)

# Create attack item
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Organizing magic and items
player_magic = [fire, blizzard, thunder, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 5},
                {"item": hi_potion, "quantity": 15},
                {"item": super_potion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hi_elixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]
enemy_items = []
enemy_magic = []

# Instantiate people
player1 = Person("Valos:", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_magic, player_items)
enemy = Person("Magus:", 120000, 221, 525, 25, enemy_magic, enemy_magic)

players = [player1, player2, player3]

i = 0
running = True

print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" +
      BColors.ENDC)

# Start of the game
while running:
    print("==========================================")
    print("\n\n")
    print("NAME                 HP                                    MP            ")
    for player in players:
        player.get_stats()

    for player in players:
        print("\n\n")
        player.get_stats()
        print("\n")

        player.choose_action()
        choice = input("     Choose action (#): ")
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

            magic_dmg = player.magic[magic_choice].generate_damage()
            spell = player.magic[magic_choice]
            player.mp = player.mp - spell.cost
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

            if player.items[item_choice]["quantity"] == 0:
                print(BColors.FAIL + "\n" + "None left..." + BColors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(BColors.OKGREEN + "\n" + item.name + " heals for",
                      str(item.prop), "HP" + BColors.ENDC)

            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(BColors.OKGREEN + "\n" + item.name +
                      "fully restores HP/MP" + BColors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(BColors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage" + BColors.ENDC)

    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player1.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("------------------------------------------")
    print("Enemy HP:", BColors.FAIL + str(enemy.get_hp()) + "/" +
          str(enemy.get_max_hp()) + BColors.ENDC)


    if enemy.get_hp() == 0:
        print(BColors.OKGREEN + "You win!" + BColors.ENDC)
        running = False

    elif player.get_hp() == 0:
        print(BColors.FAIL + "You've been defeated!" + BColors.ENDC)
        running = False
