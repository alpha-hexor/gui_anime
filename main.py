import tkinter as tk
from tkinter import ttk
import httpx
from PIL import Image, ImageTk
import io
from scrapper import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import subprocess
import threading

def load_image(url:str,size_x:int,size_y:int):
    response = httpx.get(url)
    img_data = response.content
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((size_x,size_y))

    return img

# Define search function
def show_anime():

    # Clear previous search results
    for widget in result_frame.interior.winfo_children():
        widget.destroy()
    # Get user input
    search_term = search_entry.get()
    # Make API request
    names,images = search_anime(search_term)
    
    #if no result found
    if not len(names):
        CTkMessagebox(title='Info',message='No anime found')
    
    # Create search result thumbnails and labels
    def load_content():
        row =0
        col =0
        for i in range(len(names)):
            # Get anime thumbnail image
            img=load_image(images[i],100,150)
            photo = ImageTk.PhotoImage(img)
            # Create thumbnail widget
            thumbnail = ctk.CTkLabel(result_frame.interior, image=photo,text="")
            thumbnail.image = photo
            thumbnail.grid(row=row, column=col, padx=10, pady=10)
            # Create anime name label widget
            
            name_label = ctk.CTkLabel(result_frame.interior, text=names[i][1][:35])
            name_label.grid(row=row+1, column=col, padx=10, pady=5)
            # Update row and column counters
            
            thumbnail.bind("<Button-1>", lambda event, idx=i: on_thumbnail_click(idx,names))
            col += 1
            if col == 4:
                row += 2
                col = 0
        canvas.update() # compute scrollable region
        canvas.config(scrollregion=canvas.bbox(ctk.ALL))
    
    #start with a thread to fix the unresponsive gui
    load_episode_thread = threading.Thread(target=load_content)
    load_episode_thread.start()
    
#create a separate thread for the player function
def start_player(link):
    player_thread = threading.Thread(target=player,args=(link,))
    player_thread.start()  

#function to play the anime
def player(link):
    
    args = [
        'mpv',
        '--fullscreen',
        f"{link}"
    ]
    mpv = subprocess.Popen(args)
    mpv.wait()
    mpv.kill()
    
#new anime window function
def open_anime_window(index,names):
    anime_id,anime_name = names[index]
    # Create new toplevel window
    anime_window = ctk.CTkToplevel(root)
    anime_window.geometry("800x800")
    anime_window.resizable(0,0)
    #anime_window.attributes('-topmost', 1)
    anime_window.grab_set()
    anime_window.title(anime_name)
    

    # Create a canvas to add a scrollbar to
    canvas = ctk.CTkCanvas(anime_window)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ctk.CTkScrollbar(anime_window, orientation=ctk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for the anime window content
    anime_frame = ctk.CTkFrame(canvas)
    anime_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    # Get anime info from API
    anime_info = get_anime_data(anime_id,anime_name)
    banner_url = anime_info["banner_url"]
    thumbnail_url = anime_info["thumbnail_url"]
    desc = anime_info["desc"]
    sub_eps = anime_info["sub_eps"]
    dub_eps = anime_info["dub_eps"]

    # Create banner image widget

    banner_img = load_image(banner_url,800,200)
    banner_photo = ImageTk.PhotoImage(banner_img)
    banner_label = ctk.CTkLabel(anime_frame, image=banner_photo,text="")
    banner_label.image = banner_photo
    banner_label.pack()

    # Create thumbnail image widget
    thumbnail_img = load_image(thumbnail_url,150,225)
    thumbnail_photo = ImageTk.PhotoImage(thumbnail_img)
    thumbnail_label = ctk.CTkLabel(anime_frame, image=thumbnail_photo,text="")
    thumbnail_label.image = thumbnail_photo
    thumbnail_label.place(x=10, y=210)

    # Create anime description widget
    desc_label = ctk.CTkLabel(anime_frame, text=desc, wraplength=600)
    desc_label.place(x=170, y=210)

    #Create checkbox widgets for sub and dub episodes
    sub_var = tk.BooleanVar()
    sub_checkbutton = ctk.CTkCheckBox(anime_frame, text="Sub Episodes", variable=sub_var, command=lambda: show_episodes(sub_var.get(), dub_var.get(), sub_eps, dub_eps))
    sub_checkbutton.place(x=170, y=400)

    dub_var = tk.BooleanVar(value=False)
    dub_checkbutton = ctk.CTkCheckBox(anime_frame, text="Dub Episodes", variable=dub_var, command=lambda: show_episodes(sub_var.get(), dub_var.get(), sub_eps, dub_eps))
    dub_checkbutton.place(x=300, y=400)

    anime_window.focus()
    anime_frame.update_idletasks()
    canvas.configure(scrollregion=anime_frame.bbox())
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))
    #functio for show epsidoes
    def show_episodes(is_sub,is_dub, sub_eps, dub_eps):
        def on_episode_click(episode_num, audio_type):
            #print(audio_type)
            data = stream_link(anime_id,str(episode_num),audio_type)
            quality_window = ctk.CTkToplevel(anime_window)
            quality_window.grab_set()
            quality_window.attributes()
            quality_window.title(f"Qualities - Episode {episode_num}, {audio_type}")
            quality_frame = ctk.CTkFrame(quality_window)
            quality_frame.pack()
            for quality,link in data.items():
                quality_btn = ctk.CTkButton(quality_frame, text=f"{quality}p", width=10,command=lambda link=link: (start_player(link)))
                quality_btn.pack(pady=5)
            

        audio_type = "sub" if is_sub else "dub"
        episode_list = []
        for i in range(1, int(sub_eps) + 1) if audio_type == 'sub' else range(1, int(dub_eps) + 1):
            episode_list.append(f"Ep-{i}")
        if not len(episode_list):
            CTkMessagebox(title="Error", message=f"{audio_type} is not available choose the other one", icon="cancel")
        else:
 
            num_rows = (len(episode_list) + 4) // 5
            num_cols = 5
            button_width = 15
            episode_frame_width = 400

            # Create episode frame
            episode_frame = ctk.CTkFrame(anime_window, width=episode_frame_width)
            episode_frame.place(x=170, y=450)

            scrollbar = ctk.CTkScrollbar(episode_frame)
            scrollbar.pack(side="right", fill="y")

            episode_scroll = ctk.CTkCanvas(episode_frame, yscrollcommand=scrollbar.set, bg=root.cget('bg'))
            episode_scroll.pack(side="left", fill="both", expand=True)
            scrollbar.configure(command=episode_scroll.yview)

            episode_content = ctk.CTkFrame(episode_scroll)
            episode_scroll.create_window((0, 0), window=episode_content, anchor="nw")

            # Configure episode_content frame with grid layout
            episode_content.columnconfigure(list(range(num_cols)), weight=1)
            episode_content.rowconfigure(list(range(num_rows)), weight=1)

            # Place buttons in the grid
            
            for i, episode in enumerate(episode_list):
                episode_btn = ctk.CTkButton(episode_content, text=episode, width=button_width,
                                            command=lambda episode=episode: on_episode_click(episode.split("-")[1], audio_type))
                episode_btn.grid(row=i // num_cols, column=i % num_cols, padx=5, pady=5)

            episode_scroll.bind("<MouseWheel>", lambda e: episode_scroll.configure(scrollregion=episode_scroll.bbox("all")))

def on_thumbnail_click(idx,names):
   open_anime_window(idx,names)
   

# Define tkinter window
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()  
root = ctk.CTk()
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.title("Anime App")   
   
# Define search label and entry widget
search_label = ctk.CTkLabel(root, text="Enter anime name")
search_label.pack(pady=10)
search_entry = ctk.CTkEntry(root,width=800)
search_entry.pack(pady=10)

# Define search button widget
search_button = ctk.CTkButton(root, text="Search", command=show_anime)
search_button.pack(pady=10)

#bind the enter key
root.bind('<Return>', lambda event: show_anime())


# Define scrollable frame to hold search result widgets
result_frame = ctk.CTkFrame(root, width=900, height=900)
result_frame.pack(pady=10)

scrollbar_y = ctk.CTkScrollbar(result_frame,orientation=ctk.VERTICAL)
scrollbar_y.pack(side=ctk.RIGHT, fill=ctk.Y)
scrollbar_x = ctk.CTkScrollbar(result_frame, orientation=ctk.HORIZONTAL)
scrollbar_x.pack(side=ctk.BOTTOM, fill=ctk.X)

canvas = ctk.CTkCanvas(result_frame, yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set ,width=900, height=900,background=root.cget("bg"))
canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
#canvas.create_rectangle(0, 0, 900, 900, fill=root.cget("bg"), width=0)

result_frame.interior = ctk.CTkFrame(canvas, width=900, height=900)
result_frame.interior.pack(fill=ctk.BOTH, expand=True)


scrollbar_y.configure(command=canvas.yview)
scrollbar_x.configure(command=canvas.xview)
canvas.create_window((0, 0), window=result_frame.interior, anchor=ctk.NW)
canvas.config(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

# Start the GUI loop
root.mainloop()
