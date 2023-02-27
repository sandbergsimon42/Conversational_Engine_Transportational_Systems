res = []
with open("boat_names.txt", "r") as f:
    for line in f:
        l = line.split(",") 
        for name in l:
            if len(name) > 2:
                res.append(name)

with open("boat_names.txt", "w") as f:
    f.write(",".join(res))