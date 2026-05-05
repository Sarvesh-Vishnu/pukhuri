# Pukhuri photos

Drop the three JPGs below into this folder. The app loads each as base64 in `utils/theme.py` and degrades gracefully to inline-SVG illustrations if a file is missing — so the build never breaks while you wait to source images.

## Files the app expects

| Filename | Used by | Source / artist | Pexels profile |
|---|---|---|---|
| `hero.jpg` | Home page hero (background) | **Shubham Thakur** — boy jumping in water (silhouette) | <https://www.pexels.com/@shubhamthakur/> |
| `handpump.jpg` | Map & Source page header | **Hamza Awan / themeditators** — pump with people | <https://www.pexels.com/@themeditators/> |
| `dam_cascade.jpg` | Groundwater & Demand page header | **Dhilip Ananthakrishnan** — sky and water from a dam | <https://www.pexels.com/@dhilip-ananthakrishnan-2048683/> |

## How to add them

1. Visit each artist's Pexels profile above.
2. Find the photo (link follows the artist on the chip the user gave us).
3. Click **Download → Original** (Pexels free-use licence, no fee, attribution requested but not required).
4. Save into this folder with the filenames above.
5. `git add assets/photos/*.jpg && git commit -m "Add hero photos" && git push` — HF rebuilds in ~2 min.

## Sizing

The hero is rendered at ~720 px wide on desktop. Page-headers run ~1100 px wide as a banner. **Crop to landscape ~16:9, target ~1600×900 JPG, optimise to ≤300 KB** (TinyJPG / Squoosh). The base64 embed adds about 33% to the byte size in the served HTML — keep originals lean.

## Attribution

Photo credit is rendered next to each image automatically (the `photo_credit` and `photo_credit_url` parameters on `hero()` / `page_header()`). No extra work needed — just keep this README updated if you swap a photo.

## Why no images are bundled here

I deliberately don't ship third-party photos in the repo: copyright/licence terms can change, and the cleanest move is for you to download from Pexels yourself once and own that audit trail.
