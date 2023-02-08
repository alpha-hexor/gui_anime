from scrapper import Anime
import os
engine = Anime()


name = input("[*]Enter anime name: ")
anime_data=engine.search(name)


for i in range(len(anime_data)):
    print(f"{i+1}: {anime_data[i][1]}")
    
index= (int(input("[*]Enter index: "))-1)
anime_to_watch = anime_data[index]

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
x=engine.extract_link(anime_data[index][0],"1",mode)
for item in x:
    print(item)