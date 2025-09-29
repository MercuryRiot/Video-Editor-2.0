# Video-Editor-2.0

A Python-based video editor that enables fast and flexible video editing via the command line. It offers features such as video/audio merging, subtitles, color filters, transitions, watermarking, PiP (picture-in-picture), and more. Powered by [MoviePy](https://zulko.github.io/moviepy/) and [ImageMagick](https://imagemagick.org/) for advanced video/text rendering.

---

## Features

- **Video Editing:** Load and process video files (MP4).
- **Audio Overlay:** Add external audio tracks, set volume, fade in/out.
- **Subtitles:** Add styled subtitles (custom colors).
- **Filters:** Apply effects (black & white, sepia, blur, sharpen, invert, edge, vignette).
- **Transitions:** Fade and crossfade between clips.
- **Watermark:** Add text watermark to videos.
- **PiP (Picture-in-Picture):** Overlay a secondary video in the corner.
- **Intro Animation:** Generate a simple animated intro segment.
- **Custom Resolution:** Output videos at user-specified resolutions.
- **Speed Control:** Change video playback speed.
- **Command-line UI:** Prompts for all major options.

---

## Technologies Used

- **Python 3.7+** (tested for Python 3.13.0)
- **[MoviePy](https://zulko.github.io/moviepy/):** Video editing and compositing.
- **[ImageMagick](https://imagemagick.org/):** Required for rendering text and effects (set path in script).
- **Standard Python Libraries:** `os`, `sys`

---

## Installation

1. **Install Python** (>=3.7, recommended 3.13.0).
2. **Install dependencies:**
   ```bash
   pip install moviepy
   ```
3. **Install ImageMagick** and note the installation path. Update `IMAGEMAGICK_BINARY` in `VE_magick3.py` if needed.

---

## Usage

Run the main script:
```bash
python VE_magick3.py
```
You will be prompted for:
- Video path
- Audio path (optional)
- Watermark text (optional)
- Output folder and filename
- Subtitle text and color
- Filter, transition, speed, volume, fade options
- PiP video path (optional)
- Output resolution


