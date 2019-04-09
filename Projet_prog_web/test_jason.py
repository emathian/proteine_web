import json



with open('data.json') as js:
  DATA = json.load(js)
  
print (DATA)

a = {}

a["nom"] = "Coucou"
a["lien"] = "./articles/coucou.txt"
a["date"]= "05/06/2019"

DATA.get("ARTICLES").append(a)

print(DATA)


with open('data.json', 'w') as outfile:
  json.dump(DATA, outfile)
