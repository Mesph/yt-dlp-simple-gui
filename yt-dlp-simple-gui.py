import tkinter as tk
from tkinter import messagebox, filedialog
import os, subprocess, threading, webbrowser, json, psutil, sys

ytdlp = None

def download():
    disableAll()

    savepath = savepath_entry.get()
    if savepath != readConfig()["savepath"]:
        writeConfig({"savepath": savepath})

    url = url_entry.get()
    filename = filename_entry.get()

    args = [url]

    allow_filename = True
    if filename:
        if "youtube.com" in url and ("playlist?" in url or "&list=" in url):
            allow_filename = False
    else:
        allow_filename = False

    if allow_filename:
        args.extend(["-o", filename])

    args.extend(["-P", savepath])

    if type_selected == "audio":
        args.extend(["-x"])
    elif type_selected == "videop":
        start = start_entry.get()
        end = end_entry.get()
        section = f"-ss {start} -to {end}"

        args.extend(["--postprocessor-args", section])

    if type_selected == "audio" and audio_format_selected == "mp3":
        args.extend(["--audio-format", "mp3"])
    elif type_selected != "audio" and video_format_selected == "mp4":
        args.extend(["-f", "137+140"])
    
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    additional_arguments = arguments_entry.get()
    if additional_arguments:
        args.extend([additional_arguments])

    threading.Thread(target=runScript, args=(args,), daemon=True).start()

def runScript(args):
    global ytdlp
    consoleReplaceText(f'> yt-dlp {" ".join(args)}\n\n')

    try:
        ytdlp = subprocess.Popen(["yt-dlp.exe"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW)
        replace = False
        for line in iter(ytdlp.stdout.readline, ""):
            console.config(state="normal")

            if line[:10] == "[download]":
                if not replace:
                    replace = True
                else:
                    previous_line = f'{int(console.index("insert").split(".")[0]) - 1}'
                    first_char = f"{previous_line}.0"
                    last_char = console.index(f"{previous_line}.end+1c")

                    console.delete(first_char, last_char)

                    if line[11:15] == "100%":
                        replace = False

            console.insert(tk.END, line)
            console.yview(tk.END)
            console.config(state="disabled")
        for line in iter(ytdlp.stderr.readline, ""):
            console.config(state="normal")
            console.insert(tk.END, line)
            console.yview(tk.END)
            console.config(state="disabled")
        ytdlp.stdout.close()
        ytdlp.stderr.close()
        ytdlp.wait()

    except AttributeError: # if ytdlp is None
        pass

    enableAll()

def select():
    new_savepath = filedialog.askdirectory().replace("/", "\\")
    if new_savepath:
        savepath_entry.delete(0, tk.END)
        savepath_entry.insert(0, new_savepath)

def abort():
    global ytdlp
    if ytdlp and ytdlp.poll() is None:
        process = psutil.Process(ytdlp.pid)
        for child in process.children(recursive=True):
            child.terminate()
        process.terminate()
        ytdlp = None

def update():
    disableAll(True)
    threading.Thread(target=runScript, args=(["-U"],), daemon=True).start()

def about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("260x150")
    
    info_label = tk.Label(about_window, text="yt-dlp Simple GUI v1.3.0\nby Mesph")
    link_label = tk.Label(about_window, text="https://github.com/Mesph/yt-dlp-simple-gui", fg="blue", cursor="hand2")
    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)

    link_label.bind("<Button-1>", openLink)

    info_label.pack(pady=10)
    link_label.pack(pady=10)
    close_button.pack(pady=10)

def openLink(event):
    webbrowser.open_new(r"https://github.com/Mesph/yt-dlp-simple-gui")

def consoleReplaceText(text):
    console.config(state="normal")
    console.delete("1.0", tk.END)
    console.insert(tk.END, text)
    console.config(state="disabled")

def enableAll(abort=False):
    url_entry.config(state="normal")
    filename_entry.config(state="normal")
    savepath_entry.config(state="normal")
    select_button.config(state="normal")
    arguments_entry.config(state="normal")
    audio_radio.config(state="normal")
    videof_radio.config(state="normal")
    videop_radio.config(state="normal")
    download_button.config(state="normal")
    update_button.config(state="normal")

    if type_selected == "videop":
        start_entry.config(state="normal")
        end_entry.config(state="normal")
    
    if type_selected == "audio":
        default_audio_radio.config(state="normal")
        mp3_radio.config(state="normal")

    if type_selected != "audio":
        default_video_radio.config(state="normal")
        if type_selected == "videof":
            mp4_radio.config(state="normal")
        else:
            mp4_radio.config(state="disabled")

    if abort:
        state = "normal"
    else:
        state = "disabled"
    abort_button.config(state=state)

def disableAll(abort=False):
    url_entry.config(state="readonly")
    filename_entry.config(state="readonly")
    savepath_entry.config(state="readonly")
    select_button.config(state="disabled")
    arguments_entry.config(state="readonly")
    audio_radio.config(state="disabled")
    videof_radio.config(state="disabled")
    videop_radio.config(state="disabled")
    start_entry.config(state="readonly")
    end_entry.config(state="readonly")
    default_audio_radio.config(state="disabled")
    mp3_radio.config(state="disabled")
    default_video_radio.config(state="disabled")
    mp4_radio.config(state="disabled")
    download_button.config(state="disabled")
    update_button.config(state="disabled")

    if abort:
        state = "disabled"
    else:
        state = "normal"
    abort_button.config(state=state)

def selectType():
    global type_selected
    type_selected = type.get()

    if type_selected == "videop":
        new_state = "normal"
    else:
        new_state = "disabled"
    start_entry.config(state=new_state)
    end_entry.config(state=new_state)

    if type_selected == "audio":
        new_state = "normal"
    else:
        new_state = "disabled"
    default_audio_radio.config(state=new_state)
    mp3_radio.config(state=new_state)

    if type_selected != "audio":
        default_video_radio.config(state="normal")
        if type_selected == "videof":
            mp4_radio.config(state="normal")
        else:
            mp4_radio.config(state="disabled")
            video_format.set("default_video")
            global video_format_selected
            video_format_selected = "default_video"
    else:
        default_video_radio.config(state="disabled")
        mp4_radio.config(state="disabled")

def selectAudioFormat():
    global audio_format_selected
    audio_format_selected = audio_format.get()

def selectVideoFormat():
    global video_format_selected
    video_format_selected = video_format.get()

def filePath():
    if getattr(sys,"frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

def readConfig():
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            return json.load(file)
    return None

def writeConfig(data):
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)

root = tk.Tk()
root.title("yt-dlp Simple GUI")
root.geometry("640x480")
root.resizable(False, False)

# url frame
url_frame = tk.Frame(root)
url_frame.pack(anchor=tk.W)

url_label = tk.Label(url_frame, text="URL:           ")
url_entry = tk.Entry(url_frame, width=94)

url_label.pack(side=tk.LEFT)
url_entry.pack(side=tk.LEFT)

# filename frame
filename_frame = tk.Frame(root)
filename_frame.pack(anchor=tk.W)

filename_label = tk.Label(filename_frame, text="File name: ")
filename_entry = tk.Entry(filename_frame, width=66)
filename_default_label = tk.Label(filename_frame, text="(leave empty for default name)")

filename_label.pack(side=tk.LEFT)
filename_entry.pack(side=tk.LEFT)
filename_default_label.pack(side=tk.LEFT)

# savepath frame
savepath_frame = tk.Frame(root)
savepath_frame.pack(anchor=tk.W)

savepath_label = tk.Label(savepath_frame, text="Save to:     ")
savepath_entry = tk.Entry(savepath_frame, width=87)
select_button = tk.Button(savepath_frame, text="Select", command=select)

savepath_label.pack(side=tk.LEFT)
savepath_entry.pack(side=tk.LEFT)
select_button.pack(side=tk.LEFT)

# arguments frame
arguments_frame = tk.Frame(root)
arguments_frame.pack(anchor=tk.W)

arguments_label = tk.Label(arguments_frame, text="Additional arguments: ")
arguments_entry = tk.Entry(arguments_frame, width=83)

arguments_label.pack(side=tk.LEFT)
arguments_entry.pack(side=tk.LEFT)

# type frames
audio_frame = tk.Frame(root)
audio_frame.pack(anchor=tk.W)

videof_frame = tk.Frame(root)
videof_frame.pack(anchor=tk.W)

videop_frame = tk.Frame(root)
videop_frame.pack(anchor=tk.W)

type = tk.StringVar(value="audio")
type_selected = "audio"

audio_radio = tk.Radiobutton(audio_frame, text="Audio", variable=type, value="audio", command=selectType)
videof_radio = tk.Radiobutton(videof_frame, text="Video (full)", variable=type, value="videof", command=selectType)
videop_radio = tk.Radiobutton(videop_frame, text="Video (partial)", variable=type, value="videop", command=selectType)

start_label = tk.Label(videop_frame, text="Start:")
start_entry = tk.Entry(videop_frame, width=7)
end_label = tk.Label(videop_frame, text="End:")
end_entry = tk.Entry(videop_frame, width=7)

audio_radio.pack(side=tk.LEFT)
videof_radio.pack(side=tk.LEFT)
videop_radio.pack(side=tk.LEFT)
start_label.pack(side=tk.LEFT)
start_entry.pack(side=tk.LEFT)
end_label.pack(side=tk.LEFT)
end_entry.pack(side=tk.LEFT)

start_entry.config(state="disabled")
end_entry.config(state="disabled")

# format frame
format_frame = tk.Frame(root)
format_frame.pack(anchor=tk.W)

audio_format = tk.StringVar(value="default_audio")
audio_format_selected = "default_audio"

video_format = tk.StringVar(value="default_video")
video_format_selected = "default_video"

audio_format_label = tk.Label(format_frame, text="Audio format:  ")
default_audio_radio = tk.Radiobutton(format_frame, text="Default", variable=audio_format, value="default_audio", command=selectAudioFormat)
mp3_radio = tk.Radiobutton(format_frame, text="MP3", variable=audio_format, value="mp3", command=selectAudioFormat)

video_format_label = tk.Label(format_frame, text="  Video format:  ")
default_video_radio = tk.Radiobutton(format_frame, text="Default", variable=video_format, value="default_video", command=selectVideoFormat)
mp4_radio = tk.Radiobutton(format_frame, text="MP4", variable=video_format, value="mp4", command=selectVideoFormat)

audio_format_label.pack(side=tk.LEFT)
default_audio_radio.pack(side=tk.LEFT)
mp3_radio.pack(side=tk.LEFT)

video_format_label.pack(side=tk.LEFT)
default_video_radio.pack(side=tk.LEFT)
mp4_radio.pack(side=tk.LEFT)

default_video_radio.config(state="disabled")
mp4_radio.config(state="disabled")

# buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(anchor=tk.W)

download_button = tk.Button(buttons_frame, text="Download", command=download)
abort_button = tk.Button(buttons_frame, text="Abort", command=abort)
update_button = tk.Button(buttons_frame, text="Update yt-dlp", command=update)
about_button = tk.Button(buttons_frame, text="About", command=about)

download_button.pack(side=tk.LEFT, padx=5)
abort_button.pack(side=tk.LEFT, padx=5)
update_button.pack(side=tk.LEFT, padx=5)
about_button.pack(side=tk.LEFT, padx=5)

abort_button.config(state="disabled")

# console frame
console_frame = tk.Frame(root, padx=10, pady=10)
console_frame.pack(anchor=tk.W)

console = tk.Text(console_frame, height=15, width=77)
console.pack(side=tk.LEFT)

console.config(state="disabled")

if __name__ == "__main__":
    os.chdir(filePath())

    if not os.path.isfile("yt-dlp.exe") or not os.path.isfile("ffmpeg.exe"):
        root.withdraw()
        messagebox.showinfo("yt-dlp Simple GUI", "One or both of these files are missing:\n'yt-dlp.exe' and 'ffmpeg.exe'\nDownload them from the internet and place them in the same directory as this executable")
        sys.exit()
    else:
        if readConfig():
            savepath = readConfig()["savepath"]
        else:
            savepath = f'{os.path.expanduser("~")}\\Downloads\\yt-dlp'
            writeConfig({"savepath": savepath})
        savepath_entry.insert(0, savepath)

        root.mainloop()
