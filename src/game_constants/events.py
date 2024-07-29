from enum import Enum

class Events(Enum):
    QUEST_1_BADGE = "QUEST_1_BADGE"
    QUEST_1_COIN = "QUEST_1_COIN"
    QUEST_1_COMPLETE = "QUEST_1_COMPLETE"
    SLOTS_RIPPA_SNAPPA_DEFEATED = "SLOTS_RIPPA_SNAPPA_DEFEATED"
    BLACK_JACK_BLACK_MACK_DEFEATED = "BLACK_JACK_BLACK_MACK_DEFEATED"
    MC_NUGGET_FIRST_QUEST_COMPLETE = "MC_NUGGET_FIRST_QUEST_COMPLETE"
    MC_NUGGET_SECOND_QUEST_COMPLETE = "MC_NUGGET_SECOND_QUEST_COMPLETE"
    MC_NUGGET_THIRD_QUEST_COMPLETE = "MC_NUGGET_THIRD_QUEST_COMPLETE"


    @staticmethod
    def add_event_to_player(player, event):
        if event.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(event.value)
