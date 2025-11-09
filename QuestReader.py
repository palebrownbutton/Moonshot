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

class QuestLevel():

    def __init__(self, quest_id):
        
        self.quest_id = quest_id
        self.level = 0
    
    def update(self, quest):

        while self.level < len(quest["isCompleted"]) and quest["isCompleted"][self.level]:
                self.level += 1

        if self.level >= len(quest["isCompleted"]):
            self.level = len(quest["isCompleted"]) - 1

quests = quest_list1()
quests_levels = [QuestLevel(qid) for qid in quests.keys()]
for quest_id in quests.keys():
    quests_levels.append(QuestLevel(quest_id))

skeleton_current_wave = 0
archer_current_wave = 0

def quest_update(enemy_type, direction, wave, current_archers, current_skeletons):
    global quest, quests_levels, skeleton_current_wave, archer_current_wave

    quests = quest_list2()

    for idx, quest in enumerate(quests):
        quest_level = quests_levels[idx]

        if "skeletonsDefeated" in quest["objectives"] and enemy_type == "Skeleton_Spearman" and quest["id"] == 1:
            quest["objectives"]["skeletonsDefeated"] += 1
            if quest["objectives"]["skeletonsDefeated"] >= quest["objectives"]["requiredSkeletons"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True

        if "archersDefeated" in quest["objectives"] and enemy_type == "Skeleton_Archer" and quest["id"] == 2:
            quest["objectives"]["archersDefeated"] += 1
            if quest["objectives"]["archersDefeated"] >= quest["objectives"]["requiredArchers"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True
            
        if direction == "left" and "leftDefeated" in quest["objectives"] and quest["id"] == 3:
            quest["objectives"]["leftDefeated"] += 1
            if quest["objectives"]["leftDefeated"] >= quest["objectives"]["requiredLeft"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True

        if direction == "right" and "rightDefeated" in quest["objectives"] and quest["id"] == 4:
            quest["objectives"]["rightDefeated"] += 1
            if quest["objectives"]["rightDefeated"] >= quest["objectives"]["requiredRight"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True

        if wave is not None and "wavesDefeated" in quest["objectives"] and quest["id"] == 5:
            quest["objectives"]["wavesDefeated"] += 1
            if quest["objectives"]["wavesDefeated"] > quest["objectives"]["requiredWaves"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True

        if wave is not None and current_archers == 0:
            archer_current_wave += 1

        if "requiredWaves" in quest["objectives"] and quest["id"] == 6:
            if current_archers == 0 and archer_current_wave > quest["objectives"]["requiredWaves"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True

        if wave is not None and current_skeletons == 0:
            skeleton_current_wave += 1

        if "requiredWaves" in quest["objectives"] and quest["id"] == 7:
            if current_skeletons == 0 and skeleton_current_wave > quest["objectives"]["requiredWaves"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True
         
        quest_level.update(quest)

    with open ("quest_list.json", "w") as file:
        json.dump(quests, file, indent=2)

    