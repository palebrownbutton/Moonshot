from pygame import *
import json

def quest_list1():

    with open ("quest_list.json", "r") as file:

        quest_data = json.load(file)

    quests = {
        quest["id"]: {
            "title": quest["title"],
            "details": quest["details"],
            "reward": quest["reward"],
            "isCompleted": quest["isCompleted"],
            "objectives": quest["objectives"]
        }
        for quest in quest_data
    }
    return quests

def quest_list2():

    with open ("quest_list.json", "r") as file:

        return json.load(file)

def quest_update(enemy_type, direction, wave):

    quests = quest_list2()

    for quest in quests:

        if enemy_type == "Skeleton_Spearman":

            if "skeletonsDefeated" in quest["objectives"]:
                quest["objectives"]["skeletonsDefeated"] += 1

            if quest["id"] in [1, 2]:

                if quest["objectives"]["skeletonsDefeated"] >= quest["objectives"]["requiredSkeletons"]:
                    quest["isCompleted"] = True

        if enemy_type == "Skeleton_Archer":
            
            if "archersDefeated" in quest["objectives"]:
                quest["objectives"]["archersDefeated"] += 1

            if quest["id"] in [3, 4]:

                if quest["objectives"]["archersDefeated"] >= quest["objectives"]["requiredArchers"]:
                    quest["isCompleted"] = True

        if direction == "left":

            if "leftDefeated" in quest["objectives"]:
                quest["objectives"]["leftDefeated"] += 1

            if quest["id"] in [5]:

                if quest["objectives"]["leftDefeated"] >= quest["objectives"]["requiredLeft"]:
                    quest["isCompleted"] = True

        if direction == "right":

            if "rightDefeated" in quest["objectives"]:
                quest["objectives"]["rightDefeated"] += 1

            if quest["id"] in [6]:

                if quest["objectives"]["rightDefeated"] >= quest["objectives"]["requiredRight"]:
                    quest["isCompleted"] = True

        if wave is not None:

            if "wavesDefeated" in quest["objectives"]:
                quest["objectives"]["wavesDefeated"] += 1

            if quest["id"] in [7]:

                if quest["objectives"]["wavesDefeated"] > quest["objectives"]["requiredWaves"]:
                    quest["isCompleted"] = True

    with open ("quest_list.json", "w") as file:
        json.dump(quests, file, indent=2)