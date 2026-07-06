# Chiron council demo — render asset

A self-contained, animated terminal recording of a Chiron council session,
built to be rendered into a deterministic MP4 with
[HeyGen HyperFrames](https://www.hyperframes.dev/).

- **Source of truth:** [`council-demo.html`](./council-demo.html)
- **Render target:** `demo/council-demo.mp4`
- **Composition:** `1280×720`, ~23 s, plays once, holds on a clean tagline
  frame (good poster/thumbnail).

The HTML is the source of truth. Edit it and re-render anytime — the render
step is a pure, deterministic screenshot capture (headless Chrome + FFmpeg),
so the same HTML always yields the same MP4. There is no AI/neural generation
in the render.

---

## How it works

HyperFrames renders an HTML *composition* by loading it in headless Chrome and
seeking a paused timeline frame-by-frame, encoding each frame with FFmpeg. Our
composition is **pure CSS `@keyframes`** on a single deterministic clock
(`--T: 23s`; every reveal is placed with `animation-delay`), so it:

1. **Autoplays once** when opened directly in any browser, and
2. **Seeks deterministically** during a render.

The root element carries the HyperFrames composition attributes:

```html
<div id="root"
     data-composition-id="chiron-council"
     data-start="0" data-duration="23"
     data-width="1280" data-height="720">
```

Duration and dimensions come from these `data-*` attributes, **not** from CLI
flags. A tiny inline adapter registers a seek hook on
`window.__timelines["chiron-council"]` whose `.seek(t)` pins every running CSS
animation's `currentTime` to `t` via the Web Animations API — this is what lets
the renderer land the exact same frame every pass. (If HyperFrames' native CSS
adapter drives `currentTime` itself, the hook is a harmless no-op.)

Everything is inline: no external fonts, CDNs, images, or network calls
(system monospace stack + `local()`-only `@font-face`). Verified with
`hyperframes lint` → **0 errors, 0 warnings**.

---

## Render it

HyperFrames resolves a project by finding a single root **`index.html`**. The
deliverable is named `council-demo.html`, so point the renderer at a copy named
`index.html` in an isolated directory (this also avoids HyperFrames'
`multiple_root_compositions` lint, which fires if two files in the same folder
both declare a `data-composition-id`):

```bash
cd demo

# stage an isolated render dir with the composition as index.html
mkdir -p .render && cp council-demo.html .render/index.html

# render to MP4 (30fps, standard quality are the defaults)
npx hyperframes render .render -o council-demo.mp4

# clean up
rm -rf .render
```

That writes `demo/council-demo.mp4`.

`npx hyperframes` downloads the `hyperframes` CLI on first use (no global
install needed). Useful flags on `render` (all verified against
`hyperframes` **v0.7.37**):

| Flag | Purpose | Default |
|------|---------|---------|
| `-o, --output <path>` | output file | `renders/<name>.mp4` |
| `-f, --fps <n>` | frame rate (24/25/30/60…, or rational like `30000/1001`) | `30` |
| `-q, --quality <q>` | `draft` \| `standard` \| `high` | `standard` |
| `--format <fmt>` | `mp4` \| `webm` \| `mov` \| `gif` \| `png-sequence` | `mp4` |
| `--resolution <preset>` | upscale via higher DPR (`landscape`, `4k`, …); must match aspect | — |
| `--gpu` / `--browser-gpu` | GPU encode / GPU capture | auto |
| `--docker` | deterministic render in Docker | off |
| `--strict` | fail the render on lint errors | off |

Sanity-check the composition without rendering:

```bash
cp council-demo.html .render/index.html && cd .render
npx hyperframes lint       # static checks (→ 0 errors, 0 warnings)
npx hyperframes doctor     # system deps: Chrome, FFmpeg, FFprobe
```

---

## Render status on this machine

The render was **attempted** here and reached the encode step, but did **not**
produce the MP4 because **FFprobe is not installed** on this machine:

```
✗  FFprobe not found
   FFprobe is required to probe media assets. It ships with FFmpeg but was not
   found on PATH.  brew install ffmpeg
```

The rest of the toolchain is present and healthy (`hyperframes doctor`): Node,
headless Chrome (Puppeteer cache), and a standalone FFmpeg at
`~/.local/bin/ffmpeg` — that build just ships without the sibling `ffprobe`
binary. The composition itself lints clean (**0 errors, 0 warnings**) and Chrome
loads it successfully, so the render is not blocked by the HTML.

To produce the MP4, install a full FFmpeg (which bundles `ffprobe`) and re-run
the render command above:

```bash
brew install ffmpeg          # provides ffprobe on PATH
cd demo
mkdir -p .render && cp council-demo.html .render/index.html
npx hyperframes render .render -o council-demo.mp4
rm -rf .render
```

> The `brew install` above was **not** run here — installing global software was
> out of scope for this asset. The HTML + the exact render command are the
> deliverable; the MP4 is one `brew install ffmpeg` away.
