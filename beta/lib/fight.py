import math
import random
import sys
import time

from lib import game_object
from lib.map import zonemap
from lib.npc import Giant, Orc, Bandit
from lib.static import clear, screen_width, game_over


def fight_setup(player, poss):
    clear()
    print("#" * screen_width)
    print(" " * int((screen_width - len("FIGHT")) / 2) + "FIGHT")
    print("#" * screen_width)
    x = random.random()
    if x < poss[0]:
        enemy = Bandit()
    elif poss[0] < x < poss[0] + poss[1]:
        enemy = Orc()
    else:
        enemy = Giant()  # else, solange nur 3 mögliche Gegner
    player.karma += .1
    fight(player, enemy, zonemap)


def fight(player, enemy, zonemap):
    print("                 ")
    print("You fight against: " + enemy.name)
    enemy.health_print()
    player.health_mana()
    # Auswahl für Kampf --------------------------------------------------
    a = fight_options().lower()  # das geht sicher eleganter
    valid_options = ["attack", "heal", "magic", "flee", "show stats", "quit"]  # In den fight_options() immer ergänzen
    while a not in valid_options:
        print("Please use a valid answer.")
        a = fight_options().lower()
    # Spieler-Angriff --------------------------------------------------
    if a == "attack":
        player_attack(player, enemy, zonemap)
    # Spieler-Magie --------------------------------------------------
    elif a == "magic":
        use_magic(player, enemy, zonemap)
    # Spieler-Andere Optionen --------------------------------------------------
    elif a == "heal":
        player.use_potion()
        activate_status_effect(player, enemy, zonemap)
    elif a == "flee":
        flee_from_fight(player, enemy, zonemap)
    elif a == "show stats":
        player.show_stats()
        fight(player, enemy, zonemap)
    elif a == "quit":  # ganz Spiel aus im Kampf?
        sys.exit()


def player_attack(player, enemy, zonemap):
    if not player.weapon.broken:
        print("You attack with your weapon and do " + str(player.weapon.damage) + " damage.")
        player.weapon.durability[0] -= 1
        print("Weapon durability: " + str((player.weapon.durability[0] / player.weapon.durability[1]) * 100) + "%")
        if player.weapon.durability[0] == 0:
            player.weapon.broken = True
            print("Your weapon broke! Repair it at a Blacksmith's.")
        enemy.health -= player.weapon.damage
    else:
        broken_damage = math.ceil(
            player.weapon.damage * 0.1)  # Immer aufgerundet (aka 1,2 wird 2), 10% Waffenschaden falls kaputt
        print("Your weapon is broken. You only do " + str(broken_damage) + " damage.")
        enemy.health -= broken_damage
    print("enemy: " + random.choice(enemy.quip))
    check_victory(player, enemy, zonemap)


def use_magic(player, enemy, zonemap):
    if player.spells:
        i = 0
        print("#" * screen_width)
        print("Your spells:")
        for spell in player.spells:
            if spell.status_effect == "healing":
                print(str(i + 1) + ". " + spell.name + " with " + str(spell.damage) + " healing")
            else:
                print(str(i + 1) + ". " + spell.name + " with " + str(spell.damage) + " damage")
            i += 1
        print("Which one do you want to cast? (choose number)")
        a = str(input("> ")).lower()
        valid_choices = [str(k + 1) for k in range(i)]
        if a not in valid_choices:
            print("You misspoke your spell and failed to cast it. Try again.")
            use_magic(player, enemy, zonemap)
        else:
            cast_spell = ""
            for cast in list(enumerate(valid_choices)):
                if cast[1] == a:
                    cast_spell = player.spells[cast[0]]
        # This is where the magic happens... -----------------------------------------
        if player.mp_cur_max[0] >= cast_spell.mana_cost:  # genug mana?
            player.mp_cur_max[0] -= cast_spell.mana_cost
            if cast_spell.status_effect == "healing":  # Selbstheilung
                amount = player.health_max - player.health_cur
                if amount == 0:
                    print("You are at full health.")
                elif amount < cast_spell.damage:
                    print("You heal for " + str(amount) + " HP.")
                    player.health_cur += amount
                else:
                    print("You heal yourself for " + str(cast_spell.damage) + " HP.")
                    player.health_cur += cast_spell.damage
                activate_status_effect(player, enemy, zonemap)  # Status-Schaden nach Selbstheilung
            else:  # spell ist NICHT healing -->
                print("You cast " + cast_spell.name)
                if cast_spell.damage > 0:  # Spell hat Sofort-Schaden
                    print("Your enemy takes " + str(cast_spell.damage) + " damage")
                    enemy.health -= cast_spell.damage
                if not enemy.active_effect:  # Noch kein Effekt vorhanden
                    if random.random() < cast_spell.status_chance:
                        print("Your enemy suffers from " + cast_spell.status_effect)
                        enemy.active_effect.append(cast_spell)  # Gegner bekommt Spell übergeben (wegen Effekt)
                    else:
                        print("You failed to apply any status effects.")
                else:
                    print("Your enemy is already under a spell, you don't apply any effects.")
                check_victory(player, enemy, zonemap)
        else:
            print("You don't have enough mana, you cast " + random.choice(
                ["butterflies", "bubbles", "hot air", "a flower"]) + " instead.")
            fight(player, enemy, zonemap)
    else:
        print("You haven't learnt any spells.")
        fight(player, enemy, zonemap)


def flee_from_fight(player, enemy, zonemap):
    if random.random() < 0.6:  # 60% Fluchtchance (fix? Future-Feature)
        print("You got away.")
        print("You don't get any rewards.")

    else:
        print("Your enemy won't let you go!")
        activate_status_effect(player, enemy, zonemap)


def enemy_attack(player, enemy, zonemap):
    # Gegner-Angriff --------------------------------------------------
    if random.random() < enemy.accuracy:  # Spieler nimmt Schaden
        if player.armor == 0:  # Wenn keine Rüstung anliegt
            print("Your enemy attacks and does " + str(enemy.strength) + " damage.")
            player.health_cur -= enemy.strength
        else:  # Es gibt Rüstung
            print("Your enemy attacks and does " + str(enemy.strength - player.armor) + " damage.")
            player.health_cur -= enemy.strength - player.armor
            # Es wird ein Index eines zufälligen aber angelegten Rüstungsteils gewählt
            x = player.inventory["armor"][
                random.choice([a for a, b in list(enumerate(player.inventory["armor"])) if b.equipped == True])]
            x.durability[0] -= 1
            print("Your " + x.slot + " armor was hit.")
            print("Durability: " + str((x.durability[0] / x.durability[1]) * 100) + "%")
        if player.health_cur <= 0:
            print("Your enemy defeated you!")
            game_over()
        else:
            fight(player, enemy, zonemap)
    else:  # Spieler nimmt keinen Schaden
        print("Your enemy attacks.")
        time.sleep(0.7)  # dramatic pause :D
        print("Missed!")
        fight(player, enemy, zonemap)


def activate_status_effect(player, enemy, zonemap):  # Es muss SICHER SEIN, dass der Gegner einen active spell hat
    if enemy.active_effect:
        magic = enemy.active_effect[0]
        magic.spell_activated = True
        magic.status_duration -= 1
        if magic.status_damage > 0:  # Es ist ein Spell mit Schadenswirkung
            print(magic.status_description)
            print("Your enemy takes " + str(magic.status_damage) + " damage.")
            enemy.health -= magic.status_damage
            if magic.status_duration < 0:
                enemy.active_effect.clear()
            check_victory(player, enemy, zonemap)
        else:
            if magic.status_effect == "knockout":
                print("Your enemy is knocked out and cannot attack you.")
            elif magic.status_effect == "freezing":
                print("Your enemy is frozen and cannot attack you.")
            if magic.status_duration < 0:
                enemy.active_effect.clear()
            fight(player, enemy, zonemap)
    else:
        enemy_attack(player, enemy, zonemap)


def win_fight(player, enemy, zonemap):
    print("       ")
    print("**** You won!!! ****")
    print("       ")
    zonemap[player.location]["ENCOUNTERS"] -= 1
    # Kampf ist vorbei --------------------------------------------------
    if random.random() < enemy.loot_chance:  # Chance ob Loot-Drop oder nicht (abhängig von Gegner)
        loot(enemy, player)  # Spieler erhält Trank(30%) oder Gegenstand(70%)
    else:
        print("Looks like you found nothing interesting...")
    # Garantierte Belohnungen: Gold und Erfahrung
    player.get_ep(enemy.ep_drop)
    player.get_gold(random.randrange(10, 20) * enemy.loot_level)
    time.sleep(2)  # Notwendig?
    clear()


def check_victory(player, enemy, zonemap):
    if enemy.health <= 0:
        win_fight(player, enemy, zonemap)
    else:
        if enemy.active_effect and enemy.active_effect[0].spell_activated == False:
            activate_status_effect(player, enemy, zonemap)
        elif enemy.active_effect and enemy.active_effect[0].spell_activated == True:
            enemy_attack(player, enemy, zonemap)
        elif not enemy.active_effect:
            enemy_attack(player, enemy, zonemap)


def loot(enemy, player):
    if random.random() < 0.70:  # Chance auf Gegenstand: 70%, sonst Trank
        g = random.choice([game_object.Weapon(enemy.loot_level), game_object.Armor(enemy.loot_level)])
        if g.obj_type == "weapon":
            print("You find: " + g.name)
            print("Damage: " + str(g.damage))
            print("Would you like to swap your weapon? (y/n)\n")
            ant = input("> ")
            while ant not in ["y", "n"]:
                print("I need a decision: ")
                ant = input("> ")
            print(" ")
            if ant.lower()[0] in ["y", ""]:
                player.equip_weapon(g)  # neue Waffe angelegt und alte Waffe equipped = False
            player.get_weapon(g, p=False)  # Waffe (zusätzlich) ins Inventar
        elif g.obj_type == "armor":
            print("You find: " + g.name)
            print("Protection: " + str(g.protection))
            print("Slot: " + g.slot)
            print("Would you like to swap your armor? (y/n)\n")
            ant = input("> ")
            print("")
            if ant.lower()[0] in ["y", ""]:
                player.equip_armor(g)  # Rüstung angelegt und alte Rüstung equipped = False
                print("You equip your new armor.")
            player.get_armor(g, p=False)  # Waffe (zusätzlich) ins Inventar
    else:
        player.get_potion()


def fight_options():
    print("Choose: attack, magic, heal, flee, show stats, quit\n")
    ant = input("> ")
    clear()
    return ant
