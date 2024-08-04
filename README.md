# yt-dlp-simple-gui

![https://i.imgur.com/zWRxcMl.png](https://i.imgur.com/zWRxcMl.png)

**yt-dlp-simple-gui** is a graphical user interface (GUI) for [yt-dlp](https://github.com/yt-dlp/yt-dlp), created using tkinter for Python.

This program was created with the intent of being as easy as possible to use, and without requiring the knowledge of typing commands into the command prompt.

## Installation

There are two way to install **yt-dlp-simple-gui**:

- Download the **yt-dlp-simple-gui.py** source code file to your computer, and run it using the following command (assuming you have the command prompt open at the same directory as the file): ```python yt-dlp-simple-gui.py```.
- Download the **yt-dlp-simple-gui.exe** executable file from the [Releases](https://github.com/Mesph/yt-dlp-simple-gui/releases) page.

The first option requires the installation of [Python](https://www.python.org/) and tkinter.

You will also need to download **yt-dlp.exe** and **ffmpeg.exe** and place both files in the ```C:\Users\{user}\AppData\Roaming\yt-dlp-simple-gui``` folder, which will be automatically created when you open the program for the first time.

This program only works on Windows 10, however I'm working on a Linux build.

## Usage

![https://i.imgur.com/I8Lz58g.png](https://i.imgur.com/I8Lz58g.png)

First, you'll need to paste a link to the URL box. You can then select a name for the file, and you can also change the save directory.

You can download the video or convert it into audio. It's also possible to download only a section of a video. At the **Start** and **End** boxes, you can use, for example, 2:30 and 2:40, respectively, to download only those 10 seconds of the video. It also works with hours.

For audio, you can choose between two file formats, Opus and MP3. For video, you can choose between WebM and MP4.

When you're done selecting the options you want, all you need to do is press the download button, and the file will be saved to the directory above.

There is also a console, where you can see exactly which command was used to download the file, and the output.

You can also update yt-dlp by pressing the **Update yt-dlp** button.
