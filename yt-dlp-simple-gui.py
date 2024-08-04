import tkinter as tk
import os, subprocess, threading, webbrowser, json

def download():
    disableAll()

    config_data = loadConfig()
    saveto = saveto_entry.get()

    if saveto != config_data["saveto"]:
        config_data["saveto"] = saveto
        with open(config, 'w') as file:
            json.dump(config_data, file, indent=4)

    url = url_entry.get()
    filename = filename_entry.get()

    args = [url]
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

    args.extend(["-P", saveto])

    if filename:
        args.extend(["-o", filename])
    
    if not os.path.exists(saveto):
        os.makedirs(saveto)

    if checkFiles():
        threading.Thread(target=runScript, args=(args,), daemon=True).start()

def runScript(args):
    console.config(state="normal")
    console.delete("1.0", tk.END)
    console.insert(tk.END, f"> yt-dlp {" ".join(args)}\n\n")
    console.config(state="disabled")

    process = subprocess.Popen(["yt-dlp.exe"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW)
    replace = False
    for line in iter(process.stdout.readline, ''):
        console.config(state="normal")

        if line[:10] == "[download]":
            if not replace:
                replace = True
            else:
                previous_line = f"{int(console.index("insert").split(".")[0]) - 1}"
                first_char = f"{previous_line}.0"
                last_char = console.index(f"{previous_line}.end+1c")

                console.delete(first_char, last_char)

                if line[11:15] == "100%":
                    replace = False

        console.insert(tk.END, line)
        console.yview(tk.END)
        console.config(state="disabled")
    for line in iter(process.stderr.readline, ''):
        console.config(state="normal")
        console.insert(tk.END, line)
        console.yview(tk.END)
        console.config(state="disabled")
    process.stdout.close()
    process.stderr.close()
    process.wait()

    enableAll()

def update():
    if checkFiles():
        disableAll()
        threading.Thread(target=runScript, args=(["-U"],), daemon=True).start()
    else:
        missingFiles()

def refresh():
    if checkFiles():
        refresh_button.pack_forget()
        about_button.pack_forget()
        download_button.pack(side=tk.LEFT, padx=5)
        update_button.pack(side=tk.LEFT, padx=5)
        about_button.pack(side=tk.LEFT, padx=5)

        enableAll()

def about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("260x150")
    
    about_info = tk.Label(about_window, text="yt-dlp Simple GUI v1.0.0\nby Mesph")
    about_link = tk.Label(about_window, text="https://github.com/Mesph/yt-dlp-simple-gui", fg="blue", cursor="hand2")

    about_info.pack(pady=10)
    about_link.pack(pady=10)

    about_link.bind("<Button-1>", openLink)
    
    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=10)

def openLink(event):
    webbrowser.open_new(r"https://github.com/mesph/yt-dlp-simple-gui")

def checkFiles():
    return os.path.isfile("yt-dlp.exe") and os.path.isfile("ffmpeg.exe")

def missingFiles():
    console.config(state="normal")
    console.delete("1.0", tk.END)
    console.insert(tk.END, f"One or both of these files are missing: 'yt-dlp.exe' and 'ffmpeg.exe'\nDownload them from the internet and place them inside the directory:\n{roaming}\nClick 'Refresh' when you're done")
    console.config(state="disabled")

    disableAll()
    download_button.pack_forget()
    update_button.pack_forget()
    about_button.pack_forget()
    refresh_button.pack(side=tk.LEFT, padx=5)
    about_button.pack(side=tk.LEFT, padx=5)

def loadConfig():
    if os.path.exists(config):
        with open(config, "r") as file:
            return json.load(file)
    return {"saveto": f"{os.path.expanduser("~")}\\Downloads\\yt-dlp"}

def enableAll():
    url_entry.config(state="normal")
    filename_entry.config(state="normal")
    saveto_entry.config(state="normal")
    audio_radio.config(state="normal")
    videof_radio.config(state="normal")
    videop_radio.config(state="normal")
    download_button.config(state="normal")
    update_button.config(state="normal")

    if type_selected == "videop":
        start_entry.config(state="normal")
        end_entry.config(state="normal")
    
    if type_selected == "audio":
        opus_radio.config(state="normal")
        mp3_radio.config(state="normal")

    if type_selected != "audio":
        webm_radio.config(state="normal")
        mp4_radio.config(state="normal")

def disableAll():
    url_entry.config(state="readonly")
    filename_entry.config(state="readonly")
    saveto_entry.config(state="readonly")
    audio_radio.config(state="disabled")
    videof_radio.config(state="disabled")
    videop_radio.config(state="disabled")
    start_entry.config(state="readonly")
    end_entry.config(state="readonly")
    opus_radio.config(state="disabled")
    mp3_radio.config(state="disabled")
    webm_radio.config(state="disabled")
    mp4_radio.config(state="disabled")
    download_button.config(state="disabled")
    update_button.config(state="disabled")

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
    opus_radio.config(state=new_state)
    mp3_radio.config(state=new_state)

    if type_selected != "audio":
        new_state = "normal"
    else:
        new_state = "disabled"
    webm_radio.config(state=new_state)
    mp4_radio.config(state=new_state)

def selectAudioFormat():
    global audio_format_selected
    audio_format_selected = audio_format.get()

def selectVideoFormat():
    global video_format_selected
    video_format_selected = video_format.get()

root = tk.Tk()
root.title("yt-dlp Simple GUI")
root.geometry("640x480")

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

# saveto frame
saveto_frame = tk.Frame(root)
saveto_frame.pack(anchor=tk.W)

saveto_label = tk.Label(saveto_frame, text="Save to:     ")
saveto_entry = tk.Entry(saveto_frame, width=94)

saveto_label.pack(side=tk.LEFT)
saveto_entry.pack(side=tk.LEFT)

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

audio_format = tk.StringVar(value="opus")
audio_format_selected = "opus"

video_format = tk.StringVar(value="webm")
video_format_selected = "webm"

audio_format_label = tk.Label(format_frame, text="Audio format:  ")
opus_radio = tk.Radiobutton(format_frame, text="Opus", variable=audio_format, value="opus", command=selectAudioFormat)
mp3_radio = tk.Radiobutton(format_frame, text="MP3", variable=audio_format, value="mp3", command=selectAudioFormat)

video_format_label = tk.Label(format_frame, text="  Video format:  ")
webm_radio = tk.Radiobutton(format_frame, text="WebM", variable=video_format, value="webm", command=selectVideoFormat)
mp4_radio = tk.Radiobutton(format_frame, text="MP4", variable=video_format, value="mp4", command=selectVideoFormat)

audio_format_label.pack(side=tk.LEFT)
opus_radio.pack(side=tk.LEFT)
mp3_radio.pack(side=tk.LEFT)

video_format_label.pack(side=tk.LEFT)
webm_radio.pack(side=tk.LEFT)
mp4_radio.pack(side=tk.LEFT)

webm_radio.config(state="disabled")
mp4_radio.config(state="disabled")

# buttons frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(anchor=tk.W)

download_button = tk.Button(buttons_frame, text="Download", command=download)
update_button = tk.Button(buttons_frame, text="Update yt-dlp", command=update)
refresh_button = tk.Button(buttons_frame, text="Refresh", command=refresh)
about_button = tk.Button(buttons_frame, text="About", command=about)

download_button.pack(side=tk.LEFT, padx=5)
update_button.pack(side=tk.LEFT, padx=5)
about_button.pack(side=tk.LEFT, padx=5)

# console frame
console_frame = tk.Frame(root, padx=10, pady=10)
console_frame.pack(anchor=tk.W)

console = tk.Text(console_frame, height=16, width=77)
console.pack(side=tk.LEFT)

if __name__ == "__main__":
    roaming = os.path.join(os.getenv("APPDATA"), "yt-dlp-simple-gui")
    config = f"{roaming}\\config.json"
    saveto_entry.insert(0, loadConfig()["saveto"])

    if not os.path.exists(roaming):
        os.mkdir(roaming)

    os.chdir(roaming)

    if checkFiles():
        console.insert(tk.END, "Ready")
        console.config(state="disabled")
    else:
        missingFiles()

    root.mainloop()