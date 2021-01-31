"""OAYEN (Only Audiobook You'll Ever Need) Audiobook in Python3 using Pyttsx3; can be used offline."""
import pyttsx3
from typing import List
import fitz
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from PIL import ImageTk, Image
import threading


class globals:
    first_page_number: int = 0
    last_page_number: int = 0
    filename: str = ""
    played: bool = False
    page: str = ""
    tmp: str = ""
    wordTrack: int
    run: bool = False
    utterance_id: str = "speak"
    window = None
    valid_file = False
    first: bool = False
    speaker = pyttsx3.init()


def onStart(name):
    ...


def onWord(location):
    globals.wordTrack = location["location"]
    if(globals.played is False):
        globals.speaker.stop()


def onEnd(name):
    while (globals.played is False and globals.utterance_id == "speak"):
        ...
    if(globals.utterance_id == "speak"):
        if(globals.played is True):
            globals.tmp = globals.tmp[globals.wordTrack:]
            globals.speaker.say(globals.tmp, globals.utterance_id)
    else:
        globals.speaker.endLoop()
        globals.window.quit()


def speak(text: str) -> None:
    globals.speaker.connect('started-utterance', onStart)
    globals.speaker.connect('started-word', onWord)
    globals.speaker.connect('finished-utterance', onEnd)
    globals.tmp = globals.page
    if (globals.played is True and globals.page != ""):
        globals.speaker.say(text, globals.utterance_id)
        globals.speaker.startLoop()


def get_text(value: str):
    # In this function we get first and last page, which we want the software to read
    string = value
    string = string.strip()
    if "-" in string:
        first_page_number = int(string.split("-")[0])
        last_page_number = int(string.split("-")[1])
    else:
        first_page_number = int(string)
        last_page_number = 0
    # returns the index of the first page and the last page to read. Both the first page and the last page is entered by the user upon running this program.
    return first_page_number, last_page_number


def fileBrowse() -> str:
    globals.filename = filedialog.askopenfilename(title="Select a PDF file", filetypes=(
        ("png files", "*.png"), ("all files", "*.*")))
    return globals.filename


def open_file(pdf_file: str, first_page: int, last_page: int) -> str:
    file = fitz.open(pdf_file)
    for p in range(first_page - 1, last_page):
        try:
            globals.page += str(file.getPageText(p)) + "\n"
        except:
            break
    return globals.page


def main() -> None:
    """GUI with Tkinter"""
    # ok for validating pdf and page syntax, cancel or x bar for closing the window and ending the program, forward 10 seconds backwards 10 seconds.

    def fileBrowse() -> str:
        globals.filename = filedialog.askopenfilename(title="Select a PDF file", filetypes=(
            ("pdf files", "*.pdf"), ("all files", "*.*")))
        selected_file.insert(0, globals.filename)
        # Use Entry.insert() and delete() instead of Entry.configure() for text changes
        return globals.filename

    def Play(self) -> None:
        globals.played = True
        play.place_forget()
        pause.place(x=180, y=120, width=100, height=100)
        if(not globals.first):
            globals.first = True
            globals.page = open_file(globals.filename, globals.first_page_number, globals.last_page_number)
            globals.run = True
            threading.Thread(target=speak, args=(globals.page,)).start()

    def Pause(self) -> None:
        globals.played = False
        pause.place_forget()
        play.place(x=180, y=120, width=100, height=100)

    def Male() -> None:
        globals.speaker.setProperty("voice", globals.speaker.getProperty("voices")[0].id)

    def Female() -> None:
        globals.speaker.setProperty("voice", globals.speaker.getProperty("voices")[10].id)
        # 10 for female voice with a fake British accent
        # 7 for British male

    def Ok() -> None:
        try:
            page_selection: str = pages_input.get()
            first_page, last_page = page_selection.split("-")
            globals.first_page_number = int(first_page)
            globals.last_page_number = int(last_page)
            globals.page = open_file(globals.filename, globals.first_page_number, globals.last_page_number)
            globals.valid_file = True
        except:
            messagebox.showerror("Syntax Error: ", "Valid page syntax (eg: 1-10)")

    def Cancel() -> None:
        if(not (globals.played or globals.run)):
            globals.window.quit()
        else:
            globals.utterance_id = ""
            globals.played = False

    globals.window = tk.Tk()
    globals.window.title("Audiobook")
    globals.window.geometry("465x280")
    globals.window.config(bg="purple")

    # PDF selection info
    selection_text = tk.Label(globals.window, text="Select PDF to speak", bg="purple", fg="orange")
    selection_text.place(x=0, y=0, width=145, height=40)
    # PDF file input field
    selected_file = tk.Entry(globals.window, width=200)
    selected_file.place(x=145, y=5, width=200)

    # File Browse button
    Browse = tk.Button(globals.window, text="Browse", highlightbackground="blue", fg="orange", command=fileBrowse)
    Browse.place(x=345, y=4, width=100, height=30)

    # Pages selection info
    pages_text = tk.Label(globals.window, text="Enter number of page(s) (eg: 1-10)", bg="purple", fg="orange")
    pages_text.place(x=0, y=40, width=240, height=40)
    # Pages selection input field
    pages_input = tk.Entry(globals.window, width=150)
    pages_input.place(x=240, y=45, width=150)

    # Voice configuration info
    voice_text = tk.Label(globals.window, text="Voice configuration", bg="purple", fg="orange")
    voice_text.place(x=0, y=80, width=140, height=40)
    # Male and female buttons
    voice_male = tk.Button(globals.window, text="Male", highlightbackground="blue", fg="orange", command=Male)
    voice_female = tk.Button(globals.window, text="Female", highlightbackground="blue", fg="orange", command=Female)
    voice_male.place(x=140, y=85, width=120, height=30)
    voice_female.place(x=260, y=85, width=120, height=30)

    # Play and Pause Buttons
    play_icon = Image.open(
        "/Users/james/Documents/UNC/comp110/comp110-workspace-20f-utilityfog/projects/Audiobook/Images/play0.png")
    # play image directory
    play_icon = play_icon.resize((100, 100), Image.ANTIALIAS)
    play_icon = ImageTk.PhotoImage(play_icon)
    play = tk.Label(image=play_icon, bg="purple")
    play.bind("<Button-1>", Play)
    play.place(x=180, y=120, width=100, height=100)
    pause_icon = Image.open(
        "/Users/james/Documents/UNC/comp110/comp110-workspace-20f-utilityfog/projects/Audiobook/Images/pause0.png")
    # pause image directory
    pause_icon = pause_icon.resize((100, 100), Image.ANTIALIAS)
    pause_icon = ImageTk.PhotoImage(pause_icon)
    pause = tk.Label(image=pause_icon, bg="purple")
    pause.bind("<Button-1>", Pause)

    # Ok and Cancel Buttons
    ok = tk.Button(globals.window, text="Ok", highlightbackground="navy", fg="orange", command=Ok)
    cancel = tk.Button(globals.window, text="Cancel", highlightbackground="navy",
                       fg="orange", command=Cancel)
    ok.place(x=10, y=240, width=100, height=30)
    cancel.place(x=110, y=240, width=100, height=30)

    globals.window.protocol("WM_DELETE_WINDOW", Cancel)
    globals.window.mainloop()


if __name__ == "__main__":
    main()
