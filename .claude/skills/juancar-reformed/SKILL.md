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
- Hook sits low (box top ~190 px): the user said the old, higher one was hard to read under TikTok's top bar.
- Hooks: never first person; say "Juanca ..." or ask a question (user's rule).
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

## Done so far (all from Video 5, cut from the Drive transcript doc `1yV70cutvxvF_MFqD7e860lZmknGRA2SXSPRzMalyDpg`)
Clips live in `clips/juancar/<name>.mp4` with a `<name>.json` config (render: `python clips/tools/render_clip.py cfg.json out.mp4`).
| clip | moment | hook |
|---|---|---|
| perro_01 | 0:19 dog meat | ¿LE DIERON CARNE DE PERRO GRATIS A JUANCA? |
| chico_02 | 6:17 + 7:08, buying food for a scammed guy | JUANCA LE COMPRA COMIDA A UN CHICO ESTAFADO EN CHINA |
| 259_03 | 12:14-13:26, the 259 euro meal | ¿259 € POR UNA COMIDA EN CHINA? |
| hamburguesa_04 | 4:47 + 5:38, spicy Chinese burger | LA HAMBURGUESA CHINA QUE PICA DE LOCOS |
| cocina_05 | 3:01-4:43, the street-food kitchen and the cat | JUANCA ENTRA A LA COCINA DE UN RESTAURANTE BARATO |
| iphone_06 | Video 6, 15:21-16:35, iPhone prices and haggling | ¿CUÁNTO CUESTA UN IPHONE EN CHINA? |
Unused moments (video 5): bamboo ice cream 1:33, hot pot 14:18, restaurant show 15:48, toilet "desodorante" 18:22, Sevilla vs China noodles 17:16.
- Source has burned-in Spanish subs only ~15% of the time plus a Twitch clock/logos: cropped out, own captions.
- Every clip uses the same thumbnail (`clips/juancar/assets/thumb_comida_barata_vs_cara.jpg`, the dog-meat one). The Drive has
  other thumbnails for A/B tests (folder "Vídeo 5"); ask before swapping.

## Video 6 ("Cuánto Gasto en un Día en China", Drive folder "Video 6 (MUY VIRAL)")
- Source `video6.mp4` 1280x720 30fps, 18 min; transcript doc `1ijwOlXa77IpL7bABNCIUk1K8Ggu8UAhvIkYNHKZ0d-4` (timestamps ~match the video).
- Three thumbnails (saved in `clips/juancar/assets/thumb_cuanto_gasto_{1,2,3}.jpg`): 1 = red shirt holding a 1 euro coin + "China";
  2 = shopping bags (Nike/Uniqlo/Adidas) + "China"; 3 = same bags + green "EEE". Chosen for the iPhone clip: 3 (money matches "cuánto gasto").
- Other moments seen: dog-shaped ice cream 0:14, lottery scratch cards 1:10, football shirt haggling 6:41, hand portrait 9:39,
  foot massage 11:00, tourist pack 13:15. Avoid: the replica gun 5:06 and the "reina/loca" vendor banter 4:09 (platform safety).
