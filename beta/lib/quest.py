class Quest():
    def __init__(self, name, description, goals=1, gold=0, ep=0, potion=0, origin="b2", equipment=...):
        self.quest_name = name
        self.quest_description = description
        self.tag = [", active", ", done"]
        self.quest_solved = False
        self.quest_goals = goals  # Falls 2 objectives erfüllt werden müssen.
        self.quest_gold_reward = gold
        self.quest_ep_reward = ep
        self.quest_potion_reward = potion  # man weiß ja nie, ob man sowas mal braucht
        self.quest_origin = origin  # location quest giver
        self.quest_equipment_reward = equipment  # Spell / Armor / Weapon Objekte
        self.quest_steps = [" "]
        self.quest_active_step = 0  # +1 für jedes self.quest_goals, dazu ein Step als Text

    def show_quest(self):
        if self.quest_solved:
            print(self.quest_name + self.tag[1])
            print("Return with your quest to get your reward.")
        else:
            print(self.quest_name + self.tag[0])
            print(self.quest_steps[self.quest_active_step])

    def achieve_goal(self):
        self.quest_goals -= 1
        self.quest_active_step += 1
        if self.quest_goals <= 0:
            self.quest_solved = True

    def get_reward(self, player):
        if self.quest_gold_reward > 0:
            player.gold += self.quest_gold_reward  # Nicht die player.get_gold wegen anderem print
            print("You were rewarded with " + str(self.quest_gold_reward) + " Gold.")
        if self.quest_ep_reward > 0:
            player.get_ep(self.quest_ep_reward)
        if self.quest_potion_reward > 0:
            if self.quest_potion_reward == 1:
                print("You got a potion.")
            else:
                print("You got " + str(self.quest_equipment_reward) + " potions.")
            player.potions += self.quest_potion_reward
        if self.quest_equipment_reward != ...:
            if self.quest_equipment_reward.obj_type == "spell":
                player.spells.append(self.quest_equipment_reward)
                print("You were taught the spell: " + self.quest_equipment_reward.name)
            elif self.quest_equipment_reward.obj_type == "weapon":
                print("You received a weapon.")
                player.get_weapon(self.quest_equipment_reward)
            elif self.quest_equipment_reward.obj_type == "armor":
                print("You recieved armor.")
                player.get_armor(self.quest_equipment_reward)

    def solve_quest(self, player):
        if player.location == self.quest_origin and self.quest_goals <= 0:
            self.get_reward(player)
