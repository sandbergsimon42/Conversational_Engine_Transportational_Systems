import requests
import re

cities = []
res = requests.get(f"http://worldportsource.com/ports/index/SWE.php").text

bolded_text = re.findall('">(.*?)</a>', res)

banned = [
    'List', 'List', 'Index', 'Trade', "Home", "Ports", "Waterways", "Shipping", "Call", "Views", "Us", "Home", "Map", "Top", "Sweden", "Port", "Europe"]

for el in bolded_text:
    temp = el.split()[-1]
    if len(temp) == 1 or temp in banned:
            continue

    cities.append(temp)

with open("cities.txt", "w") as f:
    f.write(",".join(cities))


    