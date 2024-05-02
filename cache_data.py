
import requests
import ast
import os

pokedex_dict = {}
max_pokemon = 905

## CACHING BY WRITING INTO A FILE
if os.path.exists("api-cache.txt"):
    f = open("api-cache.txt", "r")
    pokedex_dict = ast.literal_eval(f.read())

else:
    use_export = os.path.exists("export.txt")

    # Open export list
    export_pokemon = {}
    n = 0
    if use_export:
        with open("export.txt", "r") as f:
            for line in f.readlines():
                n += 1
                export_pokemon[line.split("(")[1].split(")")[0].replace("_", "-")] = n

    for n in range(1, max_pokemon): #All pokemon in Kanto region = 1 (Bulbasaur) to 807 (Zeraora) ==> total of 807 Pokemon exist
        pokemon = requests.get('https://pokeapi.co/api/v2/pokemon/'+str(n)).json()
        name = pokemon['name']
        if use_export and (name.upper() not in export_pokemon.keys()):
            print("SKIP " + name)
            continue
        if use_export:
            i = export_pokemon[name.upper()]
        else:
            i = n
        pokedex_dict[i] = {}
        print("Fetching " + name)
        img_url = pokemon['sprites']['front_default']
        id = pokemon['id']
        type = []
        if len(pokemon['types'])>1:
            type.append(pokemon['types'][0]['type']['name'])
            type.append(pokemon['types'][1]['type']['name'])
        else:
            type.append(pokemon['types'][0]['type']['name'])
        pokedex_dict[i]['name'] = name
        pokedex_dict[i]['id'] = id
        pokedex_dict[i]['img_url'] = img_url
        pokedex_dict[i]['type'] = type
        pokedex_dict[i]['export_id'] = i

    f = open("api-cache.txt", "w")
    f.write(str(pokedex_dict))
    f.close()

print("PokeDex of length:")
print(len(pokedex_dict))
