# Uni-Magic
  Uniqueizer for video. Bypasses blocking and shadow bans in social media.
The repository contains scripts for Uni-Magic to work, as well as the Telegram bot code. Video rendering is supported on NVIDIA technologies and on the processor **(later support for AMD technologies will appear)**.

## How to install all required dependencies
### Others
If you do not have an NVIDIA video card, then the univ.py and main.py files are suitable for you. For the code to work, in addition to everything that is in the repository, you need to download ffmpeg from the official website and add it to Path in the windows environment variables. Follow the instructions strictly and you will succeed!

For Windows: https://www.wikihow.com/Install-FFmpeg-on-Windows

For Linux: https://www.tecmint.com/install-ffmpeg-in-linux/

### NVIDIA
If you own a video card from NVIDIA, you will need to install NVIDIA CUDA from the developer’s website, and you should also make sure that your video card supports this technology. Here are the installation instructions *generated by ChatGPT-4o for Windows.
Step 1: Install NVIDIA and CUDA Drivers
Compatibility check:

Make sure your graphics card supports CUDA. This can be checked on the official [NVIDIA page](https://www.nvidia.com/Download/index.aspx).
Download and install NVIDIA drivers:

Go to the official NVIDIA website, select your video card and operating system, and download the drivers.
Install the drivers following the installer's instructions.
Download and install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).

Go to the CUDA Toolkit download page.
Select the operating system (Windows), architecture (x86_64), version (for example, 10 or 11), and installer type (exe (local)). Download and run the installer and follow the instructions. Set up environment variables for CUDA: Open System -> Advanced System Settings -> Environment Variables. In the System Variables section, find and edit the Path variable, adding the CUDA paths: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11. 4\libnvvp Step 2: Install cuDNN Download cuDNN: Go to the cuDNN download page and sign in to your [NVIDIA Developer account](https://developer.nvidia.com/cudnn).
Select the version of CUDA you have installed and download the corresponding cuDNN file.
Unpack and install cuDNN:

Unpack the downloaded cuDNN archive.
Copy the files from the unpacked archive to the appropriate CUDA directories:
```sh
copy <path_to_unpacked_archive>\bin\* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin
```
```sh
copy <path_to_unpacked_archive>\include\* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\include
```
```sh
copy <path_to_the_unpacked_archive>\lib\x64\* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\lib\x64
```

Step 3: Install FFmpeg with NVENC support
Download FFmpeg with NVENC support:

Go to FFmpeg builds and download the [FFmpeg build with NVENC support](https://ffmpeg.org/download.html).
Unpack FFmpeg and add it to PATH:

Unpack the downloaded archive to a convenient location (for example, C:\ffmpeg).
Add the paths to the FFmpeg executables to your environment variables:

Step 4: Checking Settings
Enter these commands one by one into the terminal:
```sh
nvidia-smi
```
```sh
nvcc --version
```
```sh
ffmpeg -encoders | grep nvenc
```
If there are no errors, then everything is fine and you can continue reading this text.

## How to use
  You have a choice: if you need to process a lot of video at a time, then you can run the univ.py or univ_NVIDIA.py file (depending on your PC components). Before working with these scripts, which are located in the "scripts" folder, you need to create a folder and call it "vidin", into which you need to upload the videos that you want to process. Then you can run the script itself, select how many copies you need to create for each video and wait (univ.py on average renders one video per minute, which is very slow, so if you have an NVIDIA video card, then run univ_NVIDIA.py). The video is saved in the "vidout" folder (create it manually, just in case). 
  
  The second use option means that you don’t need to process so much video at a time, and the Telegram bot is perfect for this; write “/help” to the bot and it will help you figure it out. In the bot you can also change render settings, namely: speed, mirroring and noise. That is, even if you don’t need all the functionality of the bot, it will still be useful to you as a convenient shell for changing settings. This is what it looks like:
  
![/set command](https://github.com/n1mply/Uni-Magic/assets/140534843/2a744e54-eaab-4040-a943-d3468fd8014e)

P.S. do not forget to indicate your tg-api-key in the file along the path: jsons/config.json.

If you don’t want to change the settings even through a bot, then this is what the json file that needs to be changed looks like (path: jsons/setting.json)

```json
{
"speed": [1, 1], 
"mirror?": 0, 
"noise": [0.3, 0.4]
}
```

(The ranges from and to are transmitted in square brackets, and the values ​​in the "mirror?" key whether to mirror the video or not, where 0 is no, and 1 is yes).

## TO DO
1. Add support for AMD technologies.(In progress...)
2. Add uniqueness to images, similar to videos.
3. Add at least some kind of interface for console versions of scripts.
