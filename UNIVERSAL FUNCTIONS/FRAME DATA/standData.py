# TIMEMARKS ARE CHRONOLOGICAL
import sys

stand_moves = {
"JOTARO": {
    "LIGHT_4":[
        ["freeze_frame_action", 3, 25]
    ],
    "BARRAGE":[
        ["loop_frames_action", 7, 3, 7]
    ],
    "HEAVY_1":[
        ["freeze_frame_action", 3, 12]
    ],
    "HEAVY_2":[
        ["freeze_frame_action", 4, 12],
        # ["freeze_frame_action", 5, 4]
    ],
    "HEAVY_3":[
        ["freeze_frame_action", 5, 12]
    ],
    "STAR_FINGER":[
        ["freeze_frame_action", 4, 12]
    ],
    "SMASH":[
        ["freeze_frame_action", 4, 20],
        ["freeze_frame_action", 6, 10]
    ],
    "AIR_BARRAGE":[
        ["freeze_frame_action", 5, 10],
        ["loop_frames_action", 2, 8, 14]
    ],
    "AIR_BARRAGE_FINISHER":[
        ["freeze_frame_action", 4, 10]
    ]
},
"DIO_HEAVEN": {
    "LIGHT_2":[
        ["freeze_frame_action", 6, 25]
    ],
    "LIGHT_3": [
        ["freeze_frame_action", 6, 25]
    ],
    "SURPRISE_ATTACK": [
        ["freeze_frame_action", 1, 25],
        ["freeze_frame_action", 5, 25]
    ],
    "BARRAGE": [
        ["loop_frames_action", 0, 5, 10]
    ],
}
}

def get_stand_anim(char_name, move_name):
    for char_stand_data_name in stand_moves:
        if char_name == char_stand_data_name:
            for move_data in stand_moves[char_name]:
                if move_data == move_name:
                    # print(type(stand_moves[char_stand_data_name][move_data][0]))
                    print(type(stand_moves["JOTARO"]["LIGHT_4"][0]))
                    return stand_moves[char_stand_data_name][move_data]