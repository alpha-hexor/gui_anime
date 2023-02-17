from customtkinter import *
from scrapper import Anime
from helper import *

engine = Anime()

set_default_color_theme("blue")
set_appearance_mode("dark")

# initializing the main window
mainWindow = CTk()
width = mainWindow.winfo_screenwidth()
height = mainWindow.winfo_screenheight()
dim = str(width) + "x" + str(height)
mainWindow.title("MainWindow")
mainWindow.geometry(dim)

mainFrame = CTkFrame(master=mainWindow)
mainFrame.pack(padx=5, pady=5)

resultFrame = CTkFrame(master=mainFrame)

animeNames = []
lst = []

titleLabel = CTkLabel(master=mainFrame, text="Enter Anime Name")
animeName = StringVar()
animeID = StringVar()
mode = StringVar()
mode.set("sub")
titleEntry = CTkEntry(master=mainFrame, placeholder_text="anime name", textvariable=animeName, width=300)
searchButton = CTkButton(master = mainFrame, text="Search", command= lambda : [engine.search(animeName.get(), animeNames), displayResults(resultFrame, animeNames, animeID, listEpisodesButton)])

listEpisodesButton = CTkButton(master=resultFrame, text="List Episodes", command=lambda : listEpisodes(animeNames, resultFrame, lst, animeID, engine, mode, getLinkButton))
getLinkButton = CTkButton(master=resultFrame, text="Get Links", command = lambda : extract_link(resultFrame, engine, animeID.get(), animeName.get(), "1", mode.get()))


titleLabel.pack(padx=5, pady=5)
titleEntry.pack(padx=5, pady=5)
searchButton.pack(padx=5, pady=5)

mainWindow.mainloop()