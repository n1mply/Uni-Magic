import os
import json
import asyncio
import shutil
import random
import cv2
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from moviepy.editor import VideoFileClip, ImageSequenceClip, vfx
import ffmpeg
import uuid
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from set import s
class HowMuch(StatesGroup):
    video = State()
    count = State()

def generate_random_metadata():
    metadata = {
        "title": f"Video_{uuid.uuid4()}",
        "artist": f"Artist_{random.randint(1, 1000)}",
        "album": f"Album_{random.randint(1, 1000)}",
        "date": (datetime.now() - timedelta(days=random.randint(0, 3650))).strftime("%Y-%m-%d")
    }
    return metadata

with open('jsons/settings.json', 'r') as file:
    data = json.load(file)

def add_gaussian_noise(image, mean=0, sigma=random.uniform(data['noise'][0], data['noise'][1])):
    gauss = np.random.normal(mean, sigma, image.shape).astype('uint8')
    noisy_image = cv2.add(image, gauss)
    return noisy_image

def add_noise_to_frame(frame):
    return add_gaussian_noise(frame)

def add_noise_to_frames(frames, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        noisy_frames = list(executor.map(add_noise_to_frame, frames))
    return noisy_frames

with open('jsons/config.json', 'r') as file:
    cfg = json.load(file)

print('IT WORKS!')
bot = Bot(token=cfg['tg-api'])
dp = Dispatcher()
dp.include_router(s)
input_folder = "vidin"
output_folder = "vidout"

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Hello, let's get to work!\nWrite the /uni command and start working with the 'Uniqueizer'\nFor help: /help")

@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer("How to work with the bot?\nFirst of all, write the /set command to configure the 🤖bot. There will be default 📋 values, but if they don’t suit you, you can always change them. Now, regarding the work of the 🦄/uni team. Before you start using it, you need to upload a video to the 'vidin' 📽️ directory, which will be the original, for other videos. Next, run the command (/uni). Enter the number of video copies 👁️ (video processing speed depends on your hardware, but despite this, it’s better not to make more than 10 copies at a time). Now we wait... Aaaand.. Done! Videos will be saved in ⚙️'vidout'")
    
@dp.message(Command('uni'), StateFilter(None))
async def uni(message: types.Message, state: FSMContext):
    await message.answer("Send me a video of what you will be working with")
    await state.set_state(HowMuch.video)

@dp.message(HowMuch.video)
async def univ(message: types.Message, state: FSMContext):
    file_id = message.video.file_id  
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "vidin/video.mp4") 
    await message.answer('Now enter the number of copies of the video')
    await state.set_state(HowMuch.count)

@dp.message(HowMuch.count)
async def unic(message: types.Message, state: FSMContext):
    count = int(message.text)
    await message.answer("I'm getting to work...")
    await message.answer("🦄")
    shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    videos = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
    for video in videos:
        input_path = os.path.join(input_folder, video)

        for i in range(count):
            with open('jsons/settings.json', 'r') as file:
                data = json.load(file)
            await message.answer('I apply basic settings...')
            clip = VideoFileClip(input_path)
            if data['mirror?'] == 1:
                clip = clip.fx(vfx.mirror_x)
                print('mirrored')

            speed = random.uniform(data['speed'][0], data['speed'][1])
            clip = clip.fx(vfx.speedx, speed)
            await message.answer('Adding and resizing noise to video...')
            frames = list(clip.iter_frames(dtype="uint8"))
            noisy_frames = add_noise_to_frames(frames)
            noisy_clip = ImageSequenceClip(noisy_frames, fps=clip.fps)
            await message.answer('Saving audio...')
            noisy_clip = noisy_clip.set_audio(clip.audio)
            codec = 'h264_nvenc'
            output_file = os.path.join(output_folder, f"unique_video_{i+1}.mp4")
            noisy_clip.write_videofile(output_file, codec=codec, preset='fast', ffmpeg_params=['-crf', '28'])
            metadata = generate_random_metadata()
            await message.answer('Generating metadata...')
            temp_file = os.path.join(output_folder, f"temp_unique_video_{i+1}.mp4")
            (
                ffmpeg
                .input(output_file)
                .output(temp_file,
                        **{
                            'metadata': f"title={metadata['title']}",
                            'metadata': f"artist={metadata['artist']}",
                            'metadata': f"album={metadata['album']}",
                            'metadata': f"date={metadata['date']}"
                        })
                .run(overwrite_output=True)
            )
            os.replace(temp_file, output_file)
            await message.answer('Preparing the video for sending...')
            await message.answer_video(video=types.FSInputFile(path=f'vidout/unique_video_{i+1}.mp4'), 
                                        caption=f'✅Video #{i+1} ready!')
    shutil.rmtree(input_folder)
    os.makedirs(input_folder, exist_ok=True)
    await state.clear()

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Action was canceled.", reply_markup=types.ReplyKeyboardRemove())

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
