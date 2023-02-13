import random

# this is a dictionary of dictionaries - all move data for each character

frame_data = {
    "JOTARO":{
"lightAttack":{
    "x_size": 40,
    "y_size": 70,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 30,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 7,
    "ragebar_increase": 5
},
"lightAttackEnder":{
    "x_size": 60,
    "y_size": 80,
    "x_offset": 80,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 80,
    "damage": 50,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 60,
    },

    "x_pushback": 35,
    "y_pushback": 20,
    "ragebar_increase": 7
},
"barrage":{
    "x_size": 70,
    "y_size": 25,
    "x_offset": 0, # null
    "y_offset": 0, # null
    "effect_type": "barrage",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 30,
    "damage": 4,
    "reset_doing_move": False,
    "airOK": False,
    "frame_data": {
        "startup": 3,
        "active": 5,
        "recovery": 2,
    },

    "x_pushback": 4,
    "ragebar_increase": 0.4
},
"airBarrage":{
    "x_size": 70,
    "y_size": 70,
    "x_offset": 0, # null
    "y_offset": 0, # null
    "effect_type": "barrage",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 30,
    "damage": 7,
    "reset_doing_move": False,
    "airOK": True,
    "frame_data": {
        "startup": 3,
        "active": 5,
        "recovery": 2,
    },

    "x_pushback": 1,
    "ragebar_increase": 0.7
},
"airBarrageFinisher":{
    "x_size": 70,
    "y_size": 70,
    "x_offset": 150, # null
    "y_offset": 50, # null
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 1,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 10,
    "damage": 30,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 3,
        "active": 5,
        "recovery": 2,
    },

    "x_pushback": 30,
    "ragebar_increase": 4
},
"heavyAttack":{
    "x_size": 50,
    "y_size": 70,
    "x_offset": 100,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 30,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 8,
        "active": 12,
        "recovery": 8,
    },

    "x_pushback": 10,
    "ragebar_increase": 6
},
"heavyAttackEnder":{
    "x_size": 50,
    "y_size": 90,
    "x_offset": 90,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 50,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 8,
        "active": 12,
        "recovery": 8,
    },

    "x_pushback": 10,
    "y_pushback": 28,
    "ragebar_increase": 6
},
"starFinger":{
    "x_size": 100,
    "y_size": 30,
    "x_offset": 230,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 70,
    "damage": 10,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 20,
        "recovery": 15,
    },

    "x_pushback": -23
},
"oraSmash":{
    "x_size": 70,
    "y_size": 50,
    "x_offset": 100,
    "y_offset": 20,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 1,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 60,
    "damage": 35,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 20,
        "recovery": 15,
    },

    "x_pushback": 0,
    "y_pushback": 29,
    "ragebar_increase": 4
},
"lightAttackAir":{
    "x_size": 40,
    "y_size": 70,
    "x_offset": 80,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 25,
    "reset_doing_move": True,
    "airOK": True,

    "frame_data": {
        "startup": 5,
        "active": 8,
        "recovery": 12,
    },

    "x_pushback": 7,
    "ragebar_increase": 3
},
"lightAttackAirEnder":{
    "x_size": 70,
    "y_size": 70,
    "x_offset": 90,
    "y_offset": 20,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 1,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 35,
    "reset_doing_move": False,
    "airOK": True,

    "frame_data": {
        "startup": 5,
        "active": 8,
        "recovery": 12,
    },

    "x_pushback": 7,
    "ragebar_increase": 3
},
"timestop":{
    "x_size": 0,
    "y_size": 0,
    "x_offset": 0, # null
    "y_offset": 0, # null
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 1,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 0,
    "damage": 0,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 0,
        "active": 0,
        "recovery": 60,
    },
}
},
    "THUG":{
"lightAttack":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 20,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 7,
},
"lightAttackEnder":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 10,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 35,
},
"strong_swing":{
    "x_size": 50,
    "y_size": 100,
    "x_offset": 170,
    "y_offset": 0,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 1,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 30,
    "damage": 150,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 10,
        "recovery": 20,
    },

    "x_pushback": 20,
    "y_pushback": 20,
    "ragebar_increase": 4
},
    },
"VAMPIRE":{
"lightAttack":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 20,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 7,
},
"lightAttackEnder":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 40,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 35,
},
"dbz_combo_1":{
    "x_size": 100,
    "y_size": 50,
    "x_offset": 200,
    "y_offset": 0,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 60,
    "damage": 100,
    "reset_doing_move": False,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 60,
    },

    "x_pushback": 10,
    "y_pushback": 35,
},
"dbz_combo_2":{
    "x_size": 100,
    "y_size": 100,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 60,
    "damage": 100,
    "reset_doing_move": False,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 60,
    },

    "x_pushback": 10,
    "y_pushback": 35,
},
"dbz_combo_3":{
    "x_size": 100,
    "y_size": 100,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "heavy",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 60,
    "damage": 100,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 30,
    },

    "x_pushback": 0,
    "y_pushback": -100,
},
},
"DIO_HEAVEN":{
"lightAttack":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 10,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 7,
},
"lightAttackEnder":{
    "x_size": 20,
    "y_size": 50,
    "x_offset": 60,
    "y_offset": 0,
    "effect_type": "light",
    "effect_transparency": 255,
    "effect_size": 0.5,
    "fx_tick_speed": 50,
    "frame_tick_speed": 10,
    "hitstun": 40,
    "damage": 10,
    "reset_doing_move": True,
    "airOK": False,
    "frame_data": {
        "startup": 10,
        "active": 8,
        "recovery": 8,
    },

    "x_pushback": 35,
},
}
}

def get_movedata(char_name, name):
    for char_data in frame_data:
        if char_data == char_name:
            for move_data in frame_data[char_name]:
                if move_data == name:
                    # randomize barrage position
                    if name == "barrage":
                        frame_data[char_name]["barrage"]["x_offset"] = random.randint(120, 170)
                        frame_data[char_name]["barrage"]["y_offset"] = random.randint(-50, 50)
                    elif name == "airBarrage":
                        frame_data[char_name]["airBarrage"]["x_offset"] = random.randint(120, 170)
                        frame_data[char_name]["airBarrage"]["y_offset"] = random.randint(0, 50)
                    return frame_data[char_name][move_data]