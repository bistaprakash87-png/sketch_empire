# Crown & Collapse: VideoExpress History Documentary Agent

This is a browser-agent workflow that turns a history question into a finished, narrated 7–9 minute documentary in the Crown & Collapse paper-diorama style. It also produces a ready-to-paste YouTube package. It was restructured from the earlier stickman story agent, using the channel's video [How Ireland Survived Hitler's WWII Invasion Plans](https://youtu.be/b_57voAnZzw) as the format target.

## How to use
1. Copy [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md) into a browser-capable agent with web search.
2. Sign into VideoExpress in that browser.
3. Send a request like [examples/example-request.md](examples/example-request.md). Only the topic is required. The defaults are 16:9, 7–9 minutes and the Beau Whitaker narrator.

## The pipeline
| Phase | Output | Where |
|---|---|---|
| 1. Research | A sourced fact sheet, with each claim's date, source and confidence | [templates/script-template.md](templates/script-template.md) |
| 2. Script | Hook, setup, 4–6 chapters and a thesis ending, at one sentence per line | same |
| 3. Shot list | One shot per line, typed MAP, FIGURE, SCENE, ARTIFACT or LANDSCAPE | [templates/shot-list.csv](templates/shot-list.csv) |
| 4. References | A cast sheet of recurring historical figures and the recurring sets | VideoExpress My AI Images |
| 5. Production | Image, narration and video per shot, up to 5 in parallel, saved chapter by chapter | VideoExpress |
| 6. Finish | Timeline, Auto Align, captions, music bed, save, MP4 export | VideoExpress editor |
| 7. YouTube | Titles, description with real chapters, tags, thumbnail prompt, sources | [templates/youtube-package.md](templates/youtube-package.md) |

The visual look and reusable prompt blocks are in [style/STYLE_BIBLE.md](style/STYLE_BIBLE.md). The QA list is in [evals/acceptance-checklist.md](evals/acceptance-checklist.md). [examples/ireland-ww2-breakdown.md](examples/ireland-ww2-breakdown.md) breaks down the reference video and lists what the workflow now fixes.

## What changed from the stickman agent
- **Style.** The stickman fiction style is replaced with the paper-diorama documentary style, using period-accurate figures and relief maps.
- **References.** The single master character is replaced with a cast sheet, one reference per recurring figure, plus fixed set references.
- **Research.** A research and fact-check phase was added, and every factual line traces to a source.
- **Script structure.** There is a fixed documentary structure, with no repeated arguments and varied transitions.
- **Shots.** Every narration line is one 4–7 s shot, and shot types rotate.
- **Batching.** Production works chapter by chapter, with a save after each one, so long runs can resume.
- **Finishing.** Captions and a music bed were added at the finishing stage.
- **YouTube.** A YouTube package is now built from the final script and timeline, with no placeholder chapters.
- **Kept from before.** The VideoExpress route, integrated CloneVoice narration, concurrency limits, retry limits, authorisation scope and export verification all carry over.

## Notes
- Real historical figures are drawn as stylised paper-doll figures. Nazi symbols appear only where historically necessary and are never a thumbnail focal point.
- Captions and music depend on what the VideoExpress editor offers on your plan. If they aren't available, the agent reports it.
- Never commit credentials or session data.
