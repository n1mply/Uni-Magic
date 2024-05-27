import os
import random
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip, vfx
import moviepy.video.fx.all as vfx
import json
import ffmpeg
import uuid
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


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

def add_noise_to_frames(frames):
    noisy_frames = []
    for frame in frames:
        noisy_frame = add_gaussian_noise(frame)
        noisy_frames.append(noisy_frame)
    return noisy_frames


def unique_video(input_path, output_path, index):            

    with open('jsons/settings.json', 'r') as file:
        data = json.load(file)

    clip = VideoFileClip(input_path)
    if data['mirror?'] == 1:
        clip = clip.fx(vfx.mirror_x)
        print('mirrored')

    speed = random.uniform(data['speed'][0], data['speed'][1])
    clip = clip.fx(vfx.speedx, speed)
    frames = list(clip.iter_frames(dtype="uint8"))
    noisy_frames = add_noise_to_frames(frames)
    noisy_clip = ImageSequenceClip(noisy_frames, fps=clip.fps)
    noisy_clip = noisy_clip.set_audio(clip.audio)
    codec = 'h264_nvenc'
    output_file = os.path.join(output_path, f"unique_video_{index+1}.mp4")
    noisy_clip.write_videofile(output_file, codec=codec, preset='fast', ffmpeg_params=['-crf', '28'])
    metadata = generate_random_metadata()
    temp_file = os.path.join(output_path, f"temp_unique_video_{index+1}.mp4")
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
    print(f"Saved unique video to: {output_file}")


def main():
    input_folder = "vidin"
    output_folder = "vidout"
    num_copies = int(input("Enter the number of unique copies: "))
    os.makedirs(output_folder, exist_ok=True)
    videos = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

    for video in videos:
        input_path = os.path.join(input_folder, video)
        video_name = os.path.splitext(video)[0]
        video_output_folder = os.path.join(output_folder, video_name)
        os.makedirs(video_output_folder, exist_ok=True)
        
        for i in range(num_copies):
            unique_video(input_path, video_output_folder, i)

if __name__ == "__main__":
    main()