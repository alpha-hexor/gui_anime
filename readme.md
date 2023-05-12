**A Simple gui app written in python based on the mpv video player to watch anime**


## Preview



## Prerequests
1. **python 3.7+**

2. **mpv video player should be on window path or you can change the player function in the script**

## Installation

``pip install -r requirements.txt``
``python main.py``

## Compile to executable
```sh
pip install pyinstaller

pip show customtkinter #to get the location
```
```sh
pyinstaller --noconfirm --onedir --windowed --add-data "<path to python site-packages>/customtkinter;customtkinter/" --add-data "<path to python site packages>/CTkMessagebox;CTkMessagebox" --name=anime_app main.py scrapper.py
```
**executable will be found in dist/anime_app/anime_app.exe**

## TODO

* Fix GUI issues
* Fix display issues
* Add history functionality
* Code Cleanup 