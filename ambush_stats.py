import os

INSURGENTS_DEFENDER = "Insurgents"
SECURITY_DEFENDER = "Security"

defenders = {"market": INSURGENTS_DEFENDER, "station": INSURGENTS_DEFENDER,
    "tell": SECURITY_DEFENDER, "station_night": INSURGENTS_DEFENDER,
    "embassy": INSURGENTS_DEFENDER, "embassy_night":INSURGENTS_DEFENDER,
    "verticality": INSURGENTS_DEFENDER, "siege":SECURITY_DEFENDER,
    "revolt":INSURGENTS_DEFENDER}

maps = {}

unicode_errors = 0

for filename in sorted(os.listdir(".")):
    if "000.log" in filename:
            for line in open(filename).readlines():
                if "Loading map" in line:
                    map_name = line[line.index('"')+1:line.rindex('"')]
                    if map_name in maps:
                        maps[map_name]["played"] += 1
                    else:
                        maps[map_name] = {"played": 1, "insurgents":0, "security":0}                    
                    
                    found_winner = False
                        
                    try:
                        for line in open(filename[:-7] + "002.log", encoding="utf8").readlines():
                            if "Round_Win" in line:
                                found_winner = True
                                if "Insurgent" in line:
                                    maps[map_name]["insurgents"] += 1
                                elif "Security" in line:
                                    maps[map_name]["security"] += 1
                                break
                    except UnicodeDecodeError as ude:
                        unicode_errors += 1
                    except FileNotFoundError as fnfe:
                        pass
                        
                    if (found_winner is False):
                        maps[map_name]["played"] -= 1
                                
                    break

print("Unicode errors: " + str(unicode_errors))
print(maps)

defenders_win_count = 0
defenders_total_percentage = 0.0

for map in maps:
    map_info = maps[map]
    defenders_won = 0.0

    defender = "Unknown"    

    if map in defenders:
        if defenders[map] == INSURGENTS_DEFENDER:
            defender = INSURGENTS_DEFENDER
            defenders_won = map_info["insurgents"]/float(map_info["played"])
        else:
            defender = SECURITY_DEFENDER
            defenders_won = map_info["security"]/float(map_info["played"])
            
    defenders_win_count += map_info["played"]
    defenders_total_percentage += defenders_won*map_info["played"]  
    print(map + " - Played " + str(map_info["played"]) + " times." + " Defenders were " + defender + ", with win rate: " + "{0:.2f}".format(defenders_won*100.0) + "%.")
    
print("In total, defenders won " + "{0:.2f}".format(defenders_total_percentage/defenders_win_count * 100.0) + "% of time.")