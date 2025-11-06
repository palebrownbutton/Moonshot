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
