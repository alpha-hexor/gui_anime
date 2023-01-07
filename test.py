from scrapper import Anime
engine = Anime()

name = input("[*]Enter anime name: ")
id,names=engine.search(name)

for index,name in enumerate(names,start=1):
    print(f"{index}: {name}")

index= (int(input("[*]Enter index: "))-1)
anime_to_wath = names[index]
anime_id = id[index]

dub,sub = engine.sub_dub_episode(index)
print(dub)
print(sub)
mode = "sub"

#print(engine.extract_link(anime_id,anime_to_wath,"1",mode))
# for item in engine.extract_link(anime_id,anime_to_wath,"1",mode):
#     print(item)
x=engine.extract_link(anime_id,anime_to_wath,"1",mode)
for item in x:
    print(item)