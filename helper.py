from customtkinter import *

def displayResults(resultFrame, animeNames:list, animeID, listEpisodesButton):
    for widget in resultFrame.winfo_children():
        widget.pack_forget()
    label = CTkLabel(master=resultFrame, text="Select Anime")
    label.pack(padx = 5, pady = 5)
    if len(animeNames) > 15:
        animeNames = animeNames[:15]
    for name in animeNames:
        button = CTkRadioButton(master=resultFrame, text=name[1], variable=animeID, value=name[0])
        button.pack(padx = 5, pady = 5)
    listEpisodesButton.pack(padx = 5, pady = 5)
    resultFrame.pack(padx = 5, pady = 5)

def listEpisodes(animeNames:list, resultFrame, lst, animeID, engine, mode, getLinkButton):
    dct = dict(animeNames)
    index = (animeID.get(), dct[animeID.get()])
    print(index)
    data = engine.anime_data(index)
    dubEpisodes = data['dub']
    subEpisodes = data['sub']
    desc = data['desc']

    selectionLabel = CTkLabel(master=resultFrame, text="Select What to watch")
    if dubEpisodes:
        dubButton = CTkRadioButton(master = resultFrame, text="Dubbed Episodes", variable=mode, value="dub")
        dubButton.pack(padx = 5, pady = 5)
    if subEpisodes:
        subButton = CTkRadioButton(master = resultFrame, text="Subbed Episodes", variable=mode, value="sub")
        subButton.pack(padx = 5, pady = 5)
    getLinkButton.pack(padx = 5, pady = 5)
    

def extract_link(resultFrame, engine, animeID, animeName, val, mode):
    x = engine.extract_link(animeID, "1", mode)
    for item in x:
        result = CTkLabel(master=resultFrame, text=item)
        result.pack(padx = 5, pady = 5)
    