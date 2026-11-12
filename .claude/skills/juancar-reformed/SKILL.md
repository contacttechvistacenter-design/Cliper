---
name: juancar-reformed
description: >
  Campaign rules and assets for promoting the YouTube channel "Juancar Reformed" with clips. Only use when the user
  explicitly asks for Juancar Reformed / "Juancar" clips or invokes /juancar-reformed.
disable-model-invocation: true
---

# Juancar Reformed campaign

Goal: promote the videos so people watch the full original on YouTube. Build clips with the `clip-vertical` skill using:
- watermark `clips/juancar/assets/logo.png` (YouTube logo + "JUANCAR REFORMED"), Spanish hook and captions.
- the thumbnail of the clip's source video (the Drive folder has several; the user may pick one).

## Rules from the client briefing
- **Never open or download the YouTube videos** (confuses the new channel's algorithm). Source = the shared Drive folder
  `15pV1DsMdmgcWWsdT2sO_rcyRTBe-MlEG` (videos, transcripts, thumbnails).
- Required in every clip: interesting moment, subtitles if the part has none, hook text, thumbnail, YouTube logo +
  "Juancar Reformed" watermark (cover the Twitch logo).
- Description must say to watch the full video on YouTube searching **Juancar Reformed**, e.g. "Vídeo completo en
  YouTube: Juancar Reformed". A name is enough; no link needed.
- Allowed: taking things out of context to go viral, if it still makes sense with the clip.
- Not allowed: reactions, full-screen/unedited video, hookless or senseless clips, CapCut/OpusClip marks, the same
  clip uploaded twice without edits, low quality.
- Where to post: the user posts on TikTok and Facebook. The briefing names no platforms; YouTube Shorts is unconfirmed,
  so don't suggest it.

## Drive video map (Drive file id)
| Folder | Video | mp4 id |
|---|---|---|
| Vídeo 1 | Sobreviví 24 Horas Comiendo Solo Comida Callejera en China | 1ksdud0PsofIBuZdREsCeujilb9yoqtxj |
| Vídeo 2 | Nos Colamos en el Mercado ILEGAL Más Grande de CHINA | 1l28akSajh3aNSOfHkAbB_Mpo_Zj9_F_2 |
| Vídeo 3 | En este Lugar tus Padres Deciden con Quien te Casas | 1MmPmvxtQwVexjUievC55z4Ol5SIFn1Fx |
| Vídeo 4 | Probé el Disneyland Más Barato del MUNDO | 1cu3Sff2Mgsy9tgLLzvXWd_gdXoLRG4pV |
| Vídeo 5 (MUY VIRAL) | Comida BARATA Vs CARA en China! | 1PoTaQpP7TUjEn5hDYizRkxmLo_TBLhC_ |
| Video 6 (MUY VIRAL) | Cuánto Gasto en un Día en China | 1tzVODSSQViAJsQQodXvOgAjEvJ6Vdp-c |

Download: `uv run --no-project --with gdown gdown <id> -O file.mp4`. The sandbox allows only listed hosts; Google serves
each file from its own `doc-XX-XX-docs.googleusercontent.com` host, so add the one named in the error to the
environment's allowed hosts. List the folder with `gdown.download_folder`'s internal `_download_and_parse_google_drive_link`
(plain `download_folder` fails on Google Docs).

## Done so far
- Video 5, clip 1: dog meat, 40 s: `clips/juancar/perro_01.mp4` (+ `.json` config, `.txt` description). Waiting for the
  user's OK before making more. Thumbnail used: `clips/juancar/assets/thumb_comida_barata_vs_cara.jpg`.
- Source videos have burned-in Spanish subs only ~15% of the time and a Twitch clock/logos: cropped out, own captions.
