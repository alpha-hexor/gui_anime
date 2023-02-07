from scrapper import Anime
import os
engine = Anime()


name = input("[*]Enter anime name: ")
id,names=engine.search(name)

for index,name in enumerate(names,start=1):
    print(f"{index}: {name}")

index= (int(input("[*]Enter index: "))-1)
anime_to_wath = names[index]
anime_id = id[index]

data = engine.anime_data(index)
print(data['dub'])
print(data['sub'])
print(data['thumbnail'])
os.system(f"mpv {data['thumbnail']}")
print(data['desc'])
mode = "sub"

#print(engine.extract_link(anime_id,anime_to_wath,"1",mode))
# for item in engine.extract_link(anime_id,anime_to_wath,"1",mode):
#     print(item)
x=engine.extract_link(anime_id,anime_to_wath,"1",mode)
for item in x:
    print("s")
    print(item)