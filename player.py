from tkinter import *
from tkinter import filedialog,messagebox
import pygame
import os
import shutil

# Initializing
pygame.mixer.init()

# Some imp variables
defaultplaylist = 'playlist1.txt'
currentsong=''
currentsongIndex=0
currentvolume = 0.5
songsdict={}
songsInfo=[]
songPlayed = 0
songPaused = 0
firstTime = 1

# Functions to do the work

def startSong(event=None):
    global currentsong,songPlayed,songPaused,currentsongIndex,firstTime
    
    currentsong = playlistbox.get(ACTIVE)
    currentsongIndex = playlistbox.curselection()
    if len(currentsongIndex)==0:
        currentsongIndex = (0,)
    currentsongIndex = currentsongIndex[0]
    
    if os.path.isfile(songsdict[currentsong]):
            
        pygame.mixer.music.load(songsdict[currentsong])
        playlistbox.selection_set(currentsongIndex)
        playlistbox.activate(currentsongIndex)
        pygame.mixer.music.play()
        songPlayed = 1
        songPaused = 0
        firstTime = 0
        play_button.config(image=pause_btn_img)
            
    else:
        error = messagebox.showerror(title='File not found',message=f'Music file {currentsong} does not exist at the given location : {songsdict[currentsong]}')


def playSong():
    global firstTime,songPlayed,songPaused,currentsong,currentsongIndex
    
    if firstTime:
        currentsong = playlistbox.get(currentsongIndex)
        
        if os.path.isfile(songsdict[currentsong]):
            
            pygame.mixer.music.load(songsdict[currentsong])
            playlistbox.selection_set(currentsongIndex)
            playlistbox.activate(currentsongIndex)
            pygame.mixer.music.play()
            songPlayed = 1
            firstTime = 0
            songPaused = 0
            play_button.config(image=pause_btn_img)
            
        else:
            error = messagebox.showerror(title='File not found',message=f'Music file {currentsong} does not exist at the given location : {songsdict[currentsong]}')

    elif songPlayed:
        pygame.mixer.music.pause()
        play_button.config(image=play_btn_img)
        songPaused = 1
        songPlayed = 0
        
    elif songPaused:
        pygame.mixer.music.unpause()
        play_button.config(image=pause_btn_img)
        songPaused = 0
        songPlayed = 1
    
def nextSong():
    global currentsong,songPlayed,songPaused,currentsongIndex

    playlistbox.selection_clear(0,END)
    currentsongIndex += 1
    if currentsongIndex == len(songsdict):
        currentsongIndex = 0
        
    currentsong=playlistbox.get(currentsongIndex)

    if os.path.isfile(songsdict[currentsong]):
        pygame.mixer.music.load(songsdict[currentsong])

        playlistbox.activate(currentsongIndex)
        playlistbox.selection_set(currentsongIndex)
        pygame.mixer.music.play()
        play_button.config(image=pause_btn_img)

        songPlayed = 1
        songPaused = 0
    
    else:
        error = messagebox.showerror(title='File not found',message=f'Music file {currentsong} does not exist at the given location : {songsdict[currentsong]}')
        
def prevSong():
    global currentsong,songPlayed,songPaused,currentsongIndex

    playlistbox.selection_clear(0,END)
    currentsongIndex -= 1
    if currentsongIndex < 0:
        currentsongIndex = len(songsdict) - 1
        
    currentsong=playlistbox.get(currentsongIndex)

    if os.path.isfile(songsdict[currentsong]):
        pygame.mixer.music.load(songsdict[currentsong])

        playlistbox.activate(currentsongIndex)
        playlistbox.selection_set(currentsongIndex)    
        pygame.mixer.music.play()
        play_button.config(image=pause_btn_img)
        
        songPlayed = 1
        songPaused = 0
        
    else:
        error = messagebox.showerror(title='File not found',message=f'Music file {currentsong} does not exist at the given location : {songsdict[currentsong]}')


def addSongs():
    song = filedialog.askopenfilenames(initialdir='/',title='Choose songs to add',filetypes=(('mp3 Files','*.mp3'),('ogg Files','*.ogg'),('wav Files','*.wav')))
    
    with open(defaultplaylist,'a') as file:
        for i in song:
            name=''     # Name of song to be shown in playlist
            name2=''    # Name of song to be used while playing

            l=i.split('/')
            name=l[-1]
            name2='music/'+name
            file.write(name+','+i+','+name2+'\n')
            songsdict[name]=name2
            shutil.copy(i,'music/')
            playlistbox.insert(END,name)

def savePlaylist():
    file = filedialog.asksaveasfile()
    name = file.name

    with open(name,'w') as f:
        for i in songsdict:
            f.write(i+','+songsdict[i]+'\n')

def removeCurrentSong():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    removedsong = playlistbox.get(ACTIVE)
    playlistbox.delete(ACTIVE)
    os.remove(songsdict[removedsong])
    songsdict.pop(removedsong)

    with open(defaultplaylist,'w') as file:
        for i in songsdict:
            file.write(i+','+songsdict[i]+'\n')

def removeAllSongs():
    global songsdict
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    for i in songsdict:
        os.remove(songsdict[i])
    playlistbox.delete(0,END)
    songsdict={}

    with open(defaultplaylist,'w') as file:
        pass

def changeVolume(x):
    global currentvolume
    currentvolume = int(x)/1000
    pygame.mixer.music.set_volume(currentvolume)
    
def default(event=None):
    pass


# Creating window
root=Tk()
root.geometry('500x500')
root.maxsize(500,500)
root.minsize(500,500)
root.title('Music Player')
root.config(bg='#042337')

# Creating Menu
mainmenu = Menu(root)
root.config(menu=mainmenu)

m1 = Menu(mainmenu,tearoff=0,title='Add') # The title here is not shown in the menu bar. It is shown when we tearoff the menu
mainmenu.add_cascade(label='Edit',menu=m1)
m1.add_command(label='Add Song(s)',command=addSongs)
m1.add_command(label='Remove Current Song',command=removeCurrentSong)
m1.add_command(label='Remove All Songs',command=removeAllSongs)

m2 = Menu(mainmenu,tearoff=0,title='Save')
mainmenu.add_cascade(label='Save',menu=m2)
m2.add_command(label='Save Playlist As',command=savePlaylist)


# Opening images for buttons
play_btn_img = PhotoImage(file='mediabuttons/play.png')
pause_btn_img = PhotoImage(file='mediabuttons/pause.png')
stop_btn_img = PhotoImage(file='mediabuttons/power.png')
next_btn_img = PhotoImage(file='mediabuttons/next.png')
prev_btn_img = PhotoImage(file='mediabuttons/prev.png')


# Creating widgets

# Frames
mediabutton_frame = Frame(root,bg='#042337')
playlist_frame = Frame(root)
volume_frame = Frame(root)

# Buttons
play_button = Button(mediabutton_frame,text='Play',image=play_btn_img,bd=0,command=playSong)
stop_button = Button(mediabutton_frame,text='Stop',image=stop_btn_img,bd=0,command=default)
next_button = Button(mediabutton_frame,text='Next',image=next_btn_img,borderwidth=0,command=nextSong)
prev_button = Button(mediabutton_frame,text='Previous',image=prev_btn_img,borderwidth=0,command=prevSong)

# Playlist box and its scrollbar
scroll = Scrollbar(playlist_frame)
playlistbox = Listbox(playlist_frame,yscrollcommand=scroll.set,bg='#042337',font='monospaced 10 bold',fg='#fff',width=42)
scroll.config(command=playlistbox.yview,width=15)

# Just a try to bind playlistbox to an event WORKS
playlistbox.bind('<Double-1>',startSong)
#If I use <Button-1> and run this, then it plays the songs in order when i click on any song and not the song which i click. But, if I keep <Double-1>, then no such error occurs

# Volume bar
volumebar = Scale(volume_frame,bg='#042337',label='Volume',fg='#fff',font='monospaced 10 bold',from_=0,to=1000,orient='horizontal',length=200,showvalue=0,sliderrelief='flat',sliderlength=20,command=changeVolume)
volumebar.set(currentvolume*1000)

# Adding songs to Playlistbox
# If no song is there in default playlist, then no song will be added to playlistbox
with open(defaultplaylist) as file:
    data = file.readlines()
    for i in data:
        i=i.split(',')
        songsdict[i[0]] = i[-1].rstrip()
##        print(i)
        if (not os.path.isfile(songsdict[i[0]])):
            shutil.copy(i[1],'music/')
        playlistbox.insert(END,i[0])

# Packing the widgets

playlist_frame.place(in_=root,x=50,y=50,width=400,height=150)
mediabutton_frame.place(in_=root,x=100,y=250,width=300,height=60)
volume_frame.place(in_=root,x=100,y=350,width=300,height=45)

# playlistbox.pack(side='left',anchor='n')
# scroll.pack(side='right',anchor='e',fill='y')

playlistbox.place(in_=playlist_frame,x=0,y=0,width=385,height=150)
scroll.place(in_=playlist_frame,x=385,y=0,width=15,height=150)

prev_button.grid(row=0,column=0,padx=20)
play_button.grid(row=0,column=1,padx=20)
next_button.grid(row=0,column=2,padx=20)

volumebar.place(in_=volume_frame,x=0,y=0,width=300,height=45)

# Adding icon
icon=PhotoImage(file='music.png')
root.tk.call('wm','iconphoto',root._w,icon)
#tk.call method is the Tkinter interface to the tcl interpreter. It is handy when Tkinter wrapper could not have access to some tcl/tk features

root.mainloop()
