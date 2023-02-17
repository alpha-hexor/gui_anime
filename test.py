from scrapper import Anime
import os
engine = Anime()


name = input("[*]Enter anime name: ")
names = []
engine.search(name, names)


for name in names:
    print(str(name) + "\n")
    
index= (int(input("[*]Enter index: "))-1)
anime_to_watch = (names[index][0], names[index][1])
print(anime_to_watch)

data = engine.anime_data(anime_to_watch)
print(data['dub'])
print(data['sub'])
print(data['thumbnail'])
os.system(f"mpv {data['thumbnail']}")
print(data['desc'])
mode = "sub"

#print(engine.extract_link(anime_id,anime_to_wath,"1",mode))
# for item in engine.extract_link(anime_id,anime_to_wath,"1",mode):
#     print(item)
x=engine.extract_link(names[index][0],"1",mode)
for item in x:
    print(item)