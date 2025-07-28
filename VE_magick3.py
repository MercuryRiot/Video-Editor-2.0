import os
import sys

if sys.version_info < (3, 7):
    raise RuntimeError("This script requires Python 3.7 or higher.")
if sys.version_info[:3] != (3, 13, 0):
    print("Warning: This script is tested for Python 3.13.0. You are using Python {}.{}.{}".format(*sys.version_info[:3]))

IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
os.environ["IMAGEMAGICK_BINARY"] = IMAGEMAGICK_BINARY

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})

from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, vfx
)

# Feature options
SUBTITLE_COLORS = ["yellow", "white", "black", "red", "blue", "green", "orange", "purple", "gray"]
FILTERS = [
    "none", "blackwhite", "sepia", "blur", "sharpen", "invert", "edge", "vignette"
]
TRANSITIONS = [
    "none", "fade", "crossfade"
]

def prompt_with_options(prompt, options, default=None):
    print(f"{prompt} Options: {', '.join(options)}")
    value = input(f"Choose one [{default if default else options[0]}]: ").strip().lower()
    if not value:
        return default if default else options[0]
    if value not in options:
        print(f"Invalid choice. Using default: {default if default else options[0]}")
        return default if default else options[0]
    return value

def get_user_inputs():
    org_video_path = input("Enter path to video: ").strip()
    while not org_video_path or not os.path.isfile(org_video_path):
        org_video_path = input("Invalid path. Enter path to video: ").strip()

    audio_path = input("Enter path to the audio (or press Enter to skip): ").strip()
    if audio_path and not os.path.isfile(audio_path):
        print("Audio file not found. Skipping audio.")
        audio_path = ""

    watermark = input("Enter the watermark (or press Enter to skip): ").strip()
    final_video_folder = input("Enter path to the output folder: ").strip()
    if not final_video_folder:
        final_video_folder = os.getcwd()
    if not os.path.isdir(final_video_folder):
        os.makedirs(final_video_folder, exist_ok=True)
    final_video_name = input("Enter name for the final video (use only .mp4 extension): ").strip()
    if not final_video_name.endswith(".mp4"):
        final_video_name += ".mp4"
    final_video_path = os.path.join(final_video_folder, final_video_name)

    subtitle_text = input("Enter subtitle text (or press Enter to skip): ").strip()
    subtitle_style = prompt_with_options("Subtitle color", SUBTITLE_COLORS, "yellow")

    filter_choice = prompt_with_options("Apply filter?", FILTERS, "none")
    add_transition = prompt_with_options("Add transition?", TRANSITIONS, "none")

    speed = input("Playback speed (1.0 = normal, 0.5 = half, 2.0 = double) [1.0]: ").strip()
    try:
        speed = float(speed) if speed else 1.0
    except ValueError:
        speed = 1.0

    volume = input("Audio volume (1.0 = normal, 0.5 = half, 2.0 = double) [1.0]: ").strip()
    try:
        volume = float(volume) if volume else 1.0
    except ValueError:
        volume = 1.0

    fade_audio = input("Fade audio in/out? (yes/no) [no]: ").strip().lower()
    fade_audio = fade_audio == "yes"

    pip_path = input("Path to PiP (picture-in-picture) video (or press Enter to skip): ").strip()
    if pip_path and not os.path.isfile(pip_path):
        print("PiP file not found. Skipping PiP.")
        pip_path = ""

    output_res = input("Output resolution (e.g., 1280x720 or press Enter for original): ").strip()

    return (org_video_path, audio_path, watermark, final_video_path, subtitle_text, subtitle_style,
            filter_choice, add_transition, speed, volume, fade_audio, pip_path, output_res)

def apply_filter(clip, filter_choice):
    if filter_choice == "blackwhite":
        return clip.fx(vfx.blackwhite)
    elif filter_choice == "sepia":
        return clip.fx(vfx.colorx, 0.3).fx(vfx.lum_contrast, 0, 50, 128)
    elif filter_choice == "blur":
        return clip.fx(vfx.gaussian_blur, sigma=3)
    elif filter_choice == "sharpen":
        return clip.fx(vfx.lum_contrast, 0, 100, 128)
    elif filter_choice == "invert":
        return clip.fx(vfx.invert_colors)
    elif filter_choice == "edge":
        return clip.fx(vfx.lum_contrast, 0, 100, 128).fx(vfx.painting)
    elif filter_choice == "vignette":
        return clip.fx(vfx.vignette)
    return clip

def add_subtitle(clip, subtitle_text, style, fps):
    if not subtitle_text:
        return clip
    color = style if style in SUBTITLE_COLORS else "yellow"
    subtitle = TextClip(subtitle_text, fontsize=40, color=color, bg_color='black', size=(clip.w, 60), method='caption')
    subtitle = subtitle.set_duration(clip.duration).set_fps(fps).set_position(("center", "bottom"))
    return CompositeVideoClip([clip, subtitle])

def add_animated_intro(video_size, fps, audio_clip):
    intro_duration = 5
    intro_text = TextClip("Hello world", fontsize=70, color='white', size=video_size, method='caption')
    intro_text = intro_text.set_duration(intro_duration).set_fps(fps).set_position("center")
    intro_text = intro_text.crossfadein(1).crossfadeout(1)
    if audio_clip:
        intro_music = audio_clip.subclip(25, 30)
        intro_text = intro_text.set_audio(intro_music)
    return intro_text

def add_watermark(clip, watermark, fps):
    if not watermark:
        return clip
    watermark_size = 50
    watermark_text = TextClip(watermark, fontsize=watermark_size, color='black', align='East',
                            size=(clip.w, watermark_size), method='caption')
    watermark_text = watermark_text.set_fps(fps).set_duration(clip.duration)
    watermark_text = watermark_text.margin(left=10, right=10, bottom=2, opacity=0)
    watermark_text = watermark_text.set_position(("bottom"))
    return CompositeVideoClip([clip, watermark_text.set_duration(clip.duration)])

def add_pip(main_clip, pip_path, fps):
    if not pip_path:
        return main_clip
    pip_clip = VideoFileClip(pip_path).resize(width=main_clip.w // 4).set_position(("right", "top")).set_duration(main_clip.duration)
    pip_clip = pip_clip.set_fps(fps)
    return CompositeVideoClip([main_clip, pip_clip])

def main():
    (org_video_path, audio_path, watermark, final_video_path, subtitle_text, subtitle_style,
    filter_choice, add_transition, speed, volume, fade_audio, pip_path, output_res) = get_user_inputs()

    video_clip = VideoFileClip(org_video_path)
    audio_clip = AudioFileClip(audio_path) if audio_path else None
    final_audio = audio_clip.subclip(25, 40).volumex(volume) if audio_clip else None
    if final_audio and fade_audio:
        final_audio = final_audio.audio_fadein(2).audio_fadeout(2)

    # Speed control
    video_clip = video_clip.fx(vfx.speedx, speed)
    if final_audio:
        final_audio = final_audio.fx(vfx.speedx, speed)

    # Output resolution
    if output_res:
        try:
            w, h = map(int, output_res.lower().split('x'))
            video_clip = video_clip.resize(newsize=(w, h))
        except Exception:
            print("Invalid resolution format. Using original resolution.")
            w, h = video_clip.size
    else:
        w, h = video_clip.size

    fps = video_clip.fps

    # Animated intro
    intro_text = add_animated_intro((w, h), fps, audio_clip)

    # Apply filter
    filtered_clip = apply_filter(video_clip, filter_choice)

    # Watermark
    watermarked_clip = add_watermark(filtered_clip, watermark, fps)
    watermarked_clip = watermarked_clip.set_fps(fps)
    if final_audio:
        watermarked_clip = watermarked_clip.set_audio(final_audio)

    # Subtitle
    watermarked_clip = add_subtitle(watermarked_clip, subtitle_text, subtitle_style, fps)

    # PiP
    watermarked_clip = add_pip(watermarked_clip, pip_path, fps)

    # Transitions
    if add_transition == "fade":
        watermarked_clip = watermarked_clip.fadein(1).fadeout(1)
    elif add_transition == "crossfade":
        watermarked_clip = watermarked_clip.crossfadein(1).crossfadeout(1)

    # Concatenate intro and main video
    final_clip = concatenate_videoclips([intro_text, watermarked_clip])
    final_clip = final_clip.set_duration(watermarked_clip.duration + intro_text.duration)

    print("Rendering video, please wait...")
    final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=fps)
    print(f"Video saved to {final_video_path}")

if __name__ == "__main__":
    main()