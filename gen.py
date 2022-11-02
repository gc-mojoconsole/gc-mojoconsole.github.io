import sys
import json
from collections import defaultdict


def gen_reli_list(rset, equip_affix, text_map, reli_codex, reli_set):
    result = []

    def look_for(target,value, key_name):
        for i in target:
            if i[key_name] == value:
                return i
        return None

    def look_fors(target, value, key_name):
        r = []
        for i in target:
            if i[key_name] == value:
                r.append(i)
        return r

    def get_name(id):
        return text_map[str(id)]

    for item in rset:
        i = {}
        i["id"] = item["setId"]
        if "EquipAffixId" in item:
            affix = look_for(equip_affix, item["EquipAffixId"], "id")
            i["name"] = get_name(affix["nameTextMapHash"])
        i["contains"] = {}
        has_suite = False
        for suite in look_fors(reli_codex, i["id"], "suitId"):
            has_suite = True
            level = suite["level"]
            i["contains"][level] = []
            for suite_pos_name in suite.keys():
                if suite_pos_name not in ["cupId", "leatherId", "capId", "flowerId", "sandId"]:
                    continue
                reli = suite[suite_pos_name]
                reli_detail = {}
                reli_raw = look_for(reli_set, reli, 'id')
                reli_detail["id"] = reli
                reli_detail['name'] = "(" + {
                    "cupId": "杯",
                    "leatherId": "羽",
                    "capId": "头",
                    "flowerId": "花",
                    "sandId": "沙"
                }[suite_pos_name]+ ")" + get_name(reli_raw["nameTextMapHash"])
                reli_detail["main"] = reli_raw["mainPropDepotId"]
                reli_detail["append"] = reli_raw["appendPropDepotId"]
                i["contains"][level].append(reli_detail)
        if not has_suite and len(item["containsList"]):
            level = 6
            i["contains"][level] = []
            for reli in item["containsList"]:
                reli_detail = {}
                reli_raw = look_for(reli_set, reli, 'id')
                reli_detail["id"] = reli
                reli_detail['name'] = get_name(reli_raw["nameTextMapHash"])
                reli_detail["main"] = reli_raw["mainPropDepotId"]
                reli_detail["append"] = reli_raw["appendPropDepotId"]
                i["contains"][level].append(reli_detail)
        result.append(i)
    return result


def gen_reli_main_prop(mainprop):
    o = {}
    for i in mainprop:
        depot_id = i["propDepotId"]
        if depot_id not in o:
            o[depot_id] = {}
        propName = i["propType"].replace("FIGHT_PROP_", "")
        id = i["id"]
        target = 'normal'
        if propName.endswith("_PERCENT"):
            propName = propName.replace("_PERCENT","")
            target = 'percent'
        if propName not in o[depot_id]:
            o[depot_id][propName] = {}
        o[depot_id][propName][target] = id
    return o

def gen_reli_affix_prop(affixprop):
    o = {}
    for i in affixprop:
        depot_id = i["depotId"]
        if depot_id not in o:
            o[depot_id] = {}
        propName = i["propType"].replace("FIGHT_PROP_", "")
        id = i["id"]
        target = 'normal'
        if propName.endswith("_PERCENT"):
            propName = propName.replace("_PERCENT","")
            target = 'percent'
        if propName not in o[depot_id]:
            o[depot_id][propName] = {}
        if target not in o[depot_id][propName]:
            o[depot_id][propName][target] = {}
        o[depot_id][propName][target][id] = i["propValue"]
    return o

def gen_weapon_list(weapons,text_map):
    result = []
    for weapon in weapons:
        result.append({
            "name": text_map.get(str(weapon['nameTextMapHash']), "UNKNOWN"),
            "level": weapon["rankLevel"],
            "id": weapon["id"]
        })

    return result

def gen_monster_list(monsters, monster_describe,  text_map):
    def get_name(describe_id):
        for describe in monster_describe:
            if str(describe['id']) == str(describe_id):
                return text_map.get(str(describe['nameTextMapHash']), "UNKNOWN")
        return "N/A"

    result = []
    for monster in monsters:
        if "describeId" not in monster or \
            monster['type'] not in ['MONSTER_ORDINARY', 'MONSTER_BOSS']:
            continue
        monster_type = 0 if monster['type'] == "MONSTER_ORDINARY" else 1
        name = get_name(monster['describeId'])
        if name == 'N/A':
            continue
        d = {
            "id": str(monster['id']),
            "name": name,
            "type": monster_type
        }
        result.append(d)
    return result

def gen_avatar_list(avatars, skill_depot, skills, text_map):
    result = []
    def lookup_skill_depot(sid):
        for skill in skill_depot:
            if skill['id'] == int(sid):
                return skill
        return None
    def lookup_skill(sid):
        for skill in skills:
            if skill['id'] == int(sid):
                return skill
        return None
    for avatar in avatars:
        _skill_depot = lookup_skill_depot(avatar['skillDepotId'])
        if _skill_depot is None or "energySkill" not in _skill_depot:
            continue
        skill = lookup_skill(_skill_depot['energySkill'])
        if skill is None:
            continue
        result.append({
            'id': str(avatar['id']),
            'name': text_map[str(avatar['nameTextMapHash'])],
            'element': skill['costElemType']
        })
    return result

def gen_quest_list(quests, main_quests, text_map):
    result = defaultdict(list)
    name_map = {}
    def get_name(mainId):
        if mainId not in name_map:
            for q in main_quests:
                if q['id'] == int(mainId):
                    name_map[mainId] = text_map.get(str(q['titleTextMapHash']), 'UNKNOWN')
        return name_map[mainId]
        
    for quest in quests:
        result[get_name(quest['mainId'])].append(
            [str(quest['subId']), text_map.get(str(quest['descTextMapHash']), "")]
        )
        result[get_name(quest['mainId'])].sort(key=lambda x: x[0])
    
    return result


def main(resource_folder, lang):
    output_dict = {
        "weapon_list": "",
        "avatar_list": "",
        "reli_list": "",
        "reli_main_prop": "",
        "reli_affix_prop": "",
        "monster_data": "",
        "quest_list": "",
    }
    rset = json.load(open(f"{resource_folder}/ExcelBinOutput/ReliquarySetExcelConfigData.json"))
    equip_affix = json.load(open(f"{resource_folder}/ExcelBinOutput/EquipAffixExcelConfigData.json"))
    reli_set = json.load(open(f"{resource_folder}/ExcelBinOutput/ReliquaryExcelConfigData.json"))
    text_map = json.load(open(f"{resource_folder}/TextMap/TextMap{lang.upper()}.json"))
    mainprop = json.load(open(f"{resource_folder}/ExcelBinOutput/ReliquaryMainPropExcelConfigData.json"))
    affixprop = json.load(open(f"{resource_folder}/ExcelBinOutput/ReliquaryAffixExcelConfigData.json"))
    reli_codex = json.load(open(f"{resource_folder}/ExcelBinOutput/ReliquaryCodexExcelConfigData.json"))
    weapon = json.load(open(f"{resource_folder}/ExcelBinOutput/WeaponExcelConfigData.json"))
    monster = json.load(open(f"{resource_folder}/ExcelBinOutput/MonsterExcelConfigData.json"))
    monster_describe = json.load(open(f"{resource_folder}/ExcelBinOutput/MonsterDescribeExcelConfigData.json"))
    avatar = json.load(open(f"{resource_folder}/ExcelBinOutput/AvatarExcelConfigData.json"))
    skill_depot = json.load(open(f"{resource_folder}/ExcelBinOutput/AvatarSkillDepotExcelConfigData.json"))
    skills = json.load(open(f"{resource_folder}/ExcelBinOutput/AvatarSkillExcelConfigData.json"))
    quests = json.load(open(f"{resource_folder}/ExcelBinOutput/QuestExcelConfigData.json"))
    main_quests = json.load(open(f"{resource_folder}/ExcelBinOutput/MainQuestExcelConfigData.json"))

    output_dict['reli_list'] = json.dumps(gen_reli_list(rset, equip_affix, text_map, reli_codex, reli_set))
    output_dict['reli_main_prop'] = json.dumps(gen_reli_main_prop(mainprop))
    output_dict['reli_affix_prop'] = json.dumps(gen_reli_affix_prop(affixprop))
    output_dict['weapon_list'] = json.dumps(gen_weapon_list(weapon, text_map))
    output_dict['monster_data'] = json.dumps(gen_monster_list(monster, monster_describe, text_map))
    output_dict['avatar_list'] = json.dumps(gen_avatar_list(avatar, skill_depot, skills, text_map))
    output_dict['quest_list'] = json.dumps(gen_quest_list(quests, main_quests, text_map))
    
    return output_dict


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} [Resource_folder] [LANG] [path/to/data.js]")
        sys.exit(1)
    out = main(sys.argv[1], sys.argv[2])
    if 'ch' in sys.argv[2].lower(): # translate prop name to chinese 
        mappings = {
            "HP": "生命值",
            "ATTACK": "攻击力",
            "DEFENSE": "防御力",
            "CHARGE_EFFICIENCY": "充能效率",
            "ELEMENT_MASTERY": "元素精通",
            "CRITICAL_HURT": "暴击伤害",
            "CRITICAL": "暴击率",
            "ICE": "冰元素",
            "ELEC": "雷元素",
            "_ADD_HURT": "增伤",
            "_SUB_HURT": "减伤",
            "WATER": "水元素",
            "FIRE": "火元素",
            "ROCK": "岩元素",
            "GRASS": "草元素",
            "PHYSICAL": "物理",
            "WIND": "风元素",
            "HEAL_ADD": "治疗加成"
        }
        for key in mappings.keys():
            out['reli_main_prop'] = out['reli_main_prop'].replace(key, json.dumps(mappings[key])[1:-1])
            out['reli_affix_prop'] = out['reli_affix_prop'].replace(key, json.dumps(mappings[key])[1:-1])
    
        output = """var weapon_list = JSON.parse(`{weapon_list}`);
var avatar_list = JSON.parse(`{avatar_list}`);
var reli_list = JSON.parse(`{reli_list}`);
var reli_main_prop = JSON.parse(`{reli_main_prop}`);
var reli_affix_prop= JSON.parse(`{reli_affix_prop}`);
var monster_data = JSON.parse(`{monster_data}`);
var quest_list = JSON.parse(`{quest_list}`);
"""

    if 'en' in sys.argv[2].lower(): # translate prop name to chinese 
        mappings = {
            "cup": "杯",
            "leather": "羽",
            "cap": "头",
            "flower": "花",
            "sand": "沙"
        }
        output = """var weapon_list = {weapon_list};
var avatar_list = {avatar_list};
var reli_list = {reli_list};
var reli_main_prop = {reli_main_prop};
var reli_affix_prop= {reli_affix_prop};
var monster_data = {monster_data};
var quest_list = {quest_list};
"""
        for key in mappings.keys():
            out['reli_list'] = out['reli_list'].replace(f"({json.dumps(mappings[key])[1:-1]})", f"({key})")



    if len(sys.argv) > 3:
        open(sys.argv[3], 'w').write(output.format(**out))
    else:
        open('data.js', 'w').write(output.format(**out))

    # main()