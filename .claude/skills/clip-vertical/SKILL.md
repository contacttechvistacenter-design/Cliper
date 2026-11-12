---
name: clip-vertical
description: >
  Make a 9:16 (1080x1920) promo clip for TikTok/Facebook from a long video, in a fixed layout: hook text on top,
  the video strip, the channel watermark, captions in their own band, and the video's thumbnail at the bottom.
  Use when the user asks for a clip "como el anterior", "mismo formato", "formato TikTok", or sends a new
  channel/video to promote in this style. The channel (watermark, thumbnail, language) is a parameter, never fixed.
---

# Vertical promo clip

Same look every time; only the inputs change. Renderer: `clips/tools/render_clip.py CONFIG.json OUT.mp4`
(run from the repo root; ffmpeg only). Example config: `clips/juancar/perro_01.json`.

## Inputs to ask for (once, if missing)
- Source video file and where it may be downloaded from. Respect any "do not open X" rule the user gives.
- **Channel watermark** (logo + channel name, transparent PNG) and the **thumbnail** for that video. Use the ones the
  user sends for this channel; never reuse another channel's.
- Hook language = language of the video. Captions same language.

## Layout (1080x1920)
| y | what |
|---|------|
| 0-330 | blurred copy of the video + **hook** (white box, black bold text, 2 lines, whole clip) |
| 330-819 | video strip (crop 1160x525 from a 1280x720 source) |
| 838 | channel watermark, centered, 560 wide |
| ~1000 | captions, 3 words max, current word yellow, own band |
| 1085-1693 | thumbnail 1080x608 |
| 1693-1920 | left empty for TikTok's own UI |

## Rules
- **Captions and hook never cover a face**: they live in their own bands, not over the video or the thumbnail.
- Crop the source so it carries no other platform UI: clock, Twitch logos, burned-in subs (measure how often they
  show; if under ~50% of the time, crop them out and caption everything yourself).
- Clip is 30-60 s, cut from the best moments, dead air removed, and still makes sense alone.
- Hook is a question or tease that stays true to the clip (exaggerate if it helps, never invent).
- **Never first person** ("entramos", "nos dieron", "le compramos"): the person posting is not the creator and would be
  impersonating them. Use a question, or the creator's name in third person ("Juanca entra a la cocina...").
- No CapCut/OpusClip marks, no full-screen unedited video, no repeating the same cut twice.
- Output H.264 1080x1920, loudnorm -14 LUFS. Quality is capped by the source resolution; say so if the source is 720p.

## Steps
1. Get the source; frame grid of the candidate part (look before cutting).
2. Transcribe with Whisper `small` for that part only, `language` set, `initial_prompt` = any transcript the user has,
   `word_timestamps=True`. Fix the text from the user's transcript where they differ.
3. Pick ranges (seconds) and cues; write the config JSON; render; check 4 frames (hook, captions, watermark, thumbnail).
4. Give the user the clip plus a description that names the channel and says to search it on YouTube.
5. Make one clip, get the user's OK, then make more with different moments, never the same cut.
