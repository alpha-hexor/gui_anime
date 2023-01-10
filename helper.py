from customtkinter import *

def displayResults(resultFrame, dct, animeID, listEpisodesButton):
    for widget in resultFrame.winfo_children():
        widget.pack_forget()
    label = CTkLabel(master=resultFrame, text="Select Anime")
    label.pack(padx = 5, pady = 5)
    for key in dct.keys():
        button = CTkRadioButton(master=resultFrame, text=dct[key], variable=animeID, value=key)
        button.pack(padx = 5, pady = 5)
    listEpisodesButton.pack(padx = 5, pady = 5)
    resultFrame.pack(padx = 5, pady = 5)

def listEpisodes(dct, resultFrame, lst, animeID, engine, mode, getLinkButton):
    index = list(dct).index(animeID.get())
    engine.sub_dub_episode(index, lst)
    dubEpisodes = lst[0]
    subEpisodes = lst[1]
    selectionLabel = CTkLabel(master=resultFrame, text="Select What to watch")
    if dubEpisodes:
        dubButton = CTkRadioButton(master = resultFrame, text="Dubbed Episodes", variable=mode, value="dub")
        dubButton.pack(padx = 5, pady = 5)
    if subEpisodes:
        subButton = CTkRadioButton(master = resultFrame, text="Subbed Episodes", variable=mode, value="sub")
        subButton.pack(padx = 5, pady = 5)
    getLinkButton.pack(padx = 5, pady = 5)

def extract_link(resultFrame, engine, animeID, animeName, val, mode):
    x = engine.extract_link(animeID, animeName, "1", mode)
    for item in x:
        result = CTkLabel(master=resultFrame, text=item)
        result.pack(padx = 5, pady = 5)
    