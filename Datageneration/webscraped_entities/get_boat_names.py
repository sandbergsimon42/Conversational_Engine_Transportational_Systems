import requests
import re
import random

res = requests.get(f"https://www.marinefolie.se/navne_til_baade.html").text

names = []
for el in res.split("<br>"):
    elements = el.rsplit()
    if len(elements) > 4:
        continue

    for name in el.rsplit():
        if "<" in name:
            if len(name.split("<")[0]) > 0:
                name = name.split("<")[0]
                names.append(name)

        elif 'align="top">' in name:
                first, second = name.split('align="top">')
                names.append(second)

        else:
            if len(name) > 0:
                names.append(name)
res = []
forbidden = ["and", "the", "you"]

for name in names:
    temp_name = name

    if name.lower() in forbidden:
        continue 

   
        

    # 4 boats in 10 generates a multiple name
    if random.randint(0, 10) >= 7:
        it = 1

        if random.randint(0, 10) >= 7:
            # Tripple names
            it = 2
        
        for _ in range(it):
            rand_name = names[random.randint(0, len(names) - 1)]
            while rand_name in forbidden or rand_name == name:
                rand_name = names[random.randint(0, len(names) - 1)]

            temp_name += " " + rand_name

    res.append(temp_name)


with open("boat_names.txt", "w") as boat_file:
    boat_file.write(",".join(res))
