import sys
from matplotlib import pyplot as plt
import numpy as np
import json
import os

def plot_best_dungeon(mydir: os.path, dungeon_slag: str, Player_list: list):
    files = os.listdir(mydir)
    files = sorted(files)
    dicts = {}

    for i in files:
        
        playerdb = json.load(open(os.path.join(mydir, i), "r"))
        db_name = "Players"
        if "Mains" in playerdb.keys():
            db_name = "Mains"
        for j in playerdb[db_name]:
            if j["name"] not in dicts.keys() and j["name"] in Player_list:
                dicts[j["name"]] = {}
            if j["name"] in Player_list:
                # dicts[j["name"]][i[:10]] = [x['mythic_level'] for x in j['mythic_plus_best_runs'] if x['short_name'] == dungeon_slag and x['num_keystone_upgrades'] > 0]
                dicts[j["name"]][j['gear']['item_level_equipped']] = [x['mythic_level'] for x in j['mythic_plus_best_runs'] if x['short_name'] == dungeon_slag and x['num_keystone_upgrades'] > 0]
                

    colors = ["b","g","r","c","m","y","k","w"]

    plt.xlabel("ilvl")
    plt.ylabel("Dungeon")
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 440, 2))
    plt.title(f"Dungeon Progress for: {dungeon_slag}")
    plt.grid(True)

    print(len(dicts.keys()))

    for i,Player_name in enumerate(dicts.keys()):
        # dates = list(dicts[Player_name].keys())
        # dungeons = [x[0] if len(x) > 0 else 0 for x in dicts[Player_name].values()]
        dates = []
        dungeons = []
        for k in dicts[Player_name].keys():
            if len(dicts[Player_name][k]) > 0:
                dungeons.append(dicts[Player_name][k][0])
                dates.append(k)
        
        assert len(dates) == len(dungeons)
        print(len(dates), len(dungeons))
        plt.plot(dates, dungeons, colors[i], label=Player_name)

    plt.legend()
    plt.show()

def plot_ilvl_progression(mydir: os.path, tier_lvl: str, Player_list: list):

    files = os.listdir(mydir)
    files = sorted(files)
    dicts = {}

    for i in Player_list:
        dicts[i] = {"dates":[], "ilvls":[]}

    tslots = ['head', 'chest', 'shoulder', 'legs', 'hands']

    vier_er = {}
    zwei_er = {}

    for i in range(0,len(files),2):
        playerdb = json.load(open(os.path.join(mydir,files[i]), "r"))
        db_name = "Players"
        if "Mains" in playerdb.keys():
            db_name = "Mains"
        
        for j in playerdb[db_name]:
            
            if j["name"] in Player_list:
                dicts[j["name"]]['ilvls'].append(j["gear"]['item_level_equipped'])
                dicts[j["name"]]['dates'].append(files[i][:10])
                count = 0
                for k in tslots:
                    if "tier" in j["gear"]['items'][k]:
                        if tier_lvl in str(j["gear"]['items'][k]['tier']):
                            count += 1
                if count >= 4:
                    if j["name"] not in vier_er.keys():
                        vier_er[j["name"]] = {}
                        vier_er[j["name"]]['date'] = f'({j["gear"]["item_level_equipped"]}) {files[i][:10]}'
                        vier_er[j["name"]]['gear'] = j["gear"]['items']
                if count >= 2:
                    if j["name"] not in zwei_er.keys():
                        zwei_er[j["name"]] = {}
                        zwei_er[j["name"]]['date'] = f'({j["gear"]["item_level_equipped"]}) {files[i][:10]}'
                        zwei_er[j["name"]]['gear'] = j["gear"]['items']
                            
                            
    # print("\n"*2)
    # print('2er:')
    # for i in zwei_er.keys():
    #     print(i, zwei_er[i]['date'])
    #     for k in tslots:
    #         if "tier" in zwei_er[i]['gear'][k]:
    #             print('\t',zwei_er[i]['gear'][k]['item_level'], zwei_er[i]['gear'][k]['name'])
    # print('\n')
    # print('4er:')
    # for i in vier_er.keys():
    #     print(i, vier_er[i]['date'])
    #     for k in tslots:
    #         if "tier" in vier_er[i]['gear'][k]:
    #             print('\t',vier_er[i]['gear'][k]['item_level'], vier_er[i]['gear'][k]['name'])
    # print('\n'*2)

    colors = ["b","g","r","c","m","y","k","w"]

    plt.xlabel("Date")
    plt.ylabel("Item level equipped")
    plt.xticks(rotation=90)
    plt.yticks(np.arange(0, 440, 5))
    plt.title("Item level progression")
    plt.grid(True)

    for i,Player_name in enumerate(Player_list):
        dates = dicts[Player_name]['dates']
        ilvls = dicts[Player_name]['ilvls']
        plt.plot(dates, ilvls, colors[i], label=Player_name)
        plt.plot(vier_er[Player_name]['date'][-10:], int(vier_er[Player_name]['date'][-15:-12]), colors[i]+"o", markersize=10)
        plt.text(vier_er[Player_name]['date'][-10:], int(vier_er[Player_name]['date'][-15:-12])+1, f'4er', weight='bold')
        
        plt.plot(zwei_er[Player_name]['date'][-10:], int(zwei_er[Player_name]['date'][-15:-12]), colors[i]+"o", markersize=10)
        plt.text(zwei_er[Player_name]['date'][-10:], int(zwei_er[Player_name]['date'][-15:-12])+1, f'2er', weight='bold')
        
    plt.legend()
    plt.show()

def main():
    # players = ["Thymár","Nodoká","Demage","Sup","Käseknacker", "Shalltear", 'Liamos']
    players = ["Demage", "Shalltear"]
    # plot_ilvl_progression(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mplus'), '29', players)
    plot_best_dungeon(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mplus'), 'COS' ,players)

if __name__ == "__main__":
    main()