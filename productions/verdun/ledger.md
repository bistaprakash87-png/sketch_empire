# Production ledger: Verdun

Settings: Landscape 16:9 · Image Type **Other** · Creative OFF · image enhance OFF · video prompt enhance OFF (hidden checkbox, forced off; `enhanceVideoPrompt=0` confirmed in requests) · public gallery OFF · Advanced OFF · Lipsync OFF · Narration Video ON.
Narration: built-in Text to Speech, **Christopher Multilingual**, en-US, speed 1 (CloneVoice still returns "enter the API key in your user profile").

## References (My AI Images)
| Ref | Image uuid | Media ID | Notes |
|---|---|---|---|
| Falkenhayn | eab29543-27a4-481b-860f-b4b0e75c6819 | 46376941 | 1st attempt |
| Pétain | 2f300fb6-f502-4f21-bae4-affc136dc7b6 | 46377105 | 2nd attempt; 1st had olive trousers |
| Raynal | 5dd89cb2-96af-4bdd-b1d4-6b572904c2bd | 46377115 | 1st attempt; olive trousers (compromise) |

Set references were not generated as separate images; set layouts are fixed in text and repeated in every prompt (compromise to keep the run tractable).

## Method
Driven by page JS helpers (`vx.*`) over the UI: carousel `slideTo` the shot's image before Create Video, then the `uuid=` of every image2video request is compared with the approved image (stored as `ok`).

## Production
- All 113 shots produced (113 completed clips, unique source image and unique narration audio per clip; every image2video `uuid` matched the approved image; every narration audio's library name matched its line).
- Cast references were made, but Consistent Character was dropped: pair-candidate slides would not submit to Create Video, so the 12 figure shots (Falkenhayn, Pétain, Raynal) were regenerated as normal images with the cast description repeated in the prompt. Likeness between shots is therefore by description, not by reference image.
- Regenerated before animating: S022, S024, S025, S027 (stray civilians; prompts for no-people shots now say "No people"), S028 (no arrow), S054 (hills looked like volcanoes).
- Redone after the source check: S010, S035 (submitted with another shot's image by an overlapping run; superseded clips 230bef8e…, 05b5bea8… stay unused in My AI Videos).
- Video prompt enhancement was on for S001 and S007 only.
- Image checks: S001–S067 checked visually in batches. The built-in browser pane was hidden from about 13:55, so images for S068–S113 and the 12 figure shots were **not** visually checked before animating.
- Image generation hit repeated "Error. Please try again later" responses after ~18–20 images; resumed after a pause. Video queue limit: 5 in parallel, ~3–5 min per clip.

## Assembly and export
- New project, ID 451915, "Verdun: The Battle Designed to Bleed France White" (the editor was on an unsaved project with ID 0, so nothing was overwritten).
- 113 clips added to track 1 in script order via the editor's own Add-to-Timeline event, each add verified (+1). Auto Align run: 0 gaps, 0 overlaps, 0 order mismatches.
- Export warned that projects over 10:00 are truncated (10:07.6). S043 (labour battalions) and S088 (offensive called off) were removed; final timeline 111 clips, 598.55 s (9:58.6).
- Captions: `verdun-captions.srt` built from the narration and measured clip times (VideoExpress Automatic Captions opens an outside service).
- Music: none added (stock audio only has nature ambience on this plan, per the Lusitania run).
- Export verified: My Videos item 749907, "Verdun: The Battle Designed to Bleed France White", 27/10/2026 14:50, 304.81 MB, MP4 1920×1080, 598.54 s. Metadata loads; full playback not verified.

## v2 (opening fix after vidIQ pre-publish forecast)
- Forecast flagged near-silence in the first seconds. Measured: narration starts at 0.1 s, but S001 had a 0.5 s pause (2.3–2.8 s, after "In February 1916,") and 0.3 s of silence at its end.
- S001 regenerated (new image 2f30b573…, clip 1de98783…, audio 46407171) with the line read without the comma; new clip has no frame below −52 dB. Swapped in at 0:00, Auto Align: 111 clips, 0 gaps, 598.55 s.
- Saved project 451915 and exported as "Verdun: The Battle Designed to Bleed France White (v2)", MP4 1080 High.
- Subtitles rebuilt as `verdun-subtitles-en.srt`: 323 cues of ≤7 words / ≤42 characters, each line's cues ending when its narration ends (measured per clip). Replaces `verdun-captions.srt`.
- v2 export verified: My Videos item 750230, 27/10/2026 17:46, 304.82 MB, MP4 1920×1080, 598.54 s. Use this one for upload.
