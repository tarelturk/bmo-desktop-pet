# BMO Desktop Pet

A tiny mint-green pal with a little game on its screen. 🩵

**Pong while work is running. Curious eyes that follow the mouse while idle. Quick, natural blinks.** A friendly desktop companion with a full set of playful animations.

## BMO in motion

| Idle | Working — Pong | Waiting |
|:---:|:---:|:---:|
| ![BMO idle animation](media/idle.gif) | ![BMO plays Pong](media/running.gif) | ![BMO waiting](media/waiting.gif) |

| Waving | Jumping | Reviewing |
|:---:|:---:|:---:|
| ![BMO waves](media/waving.gif) | ![BMO jumps](media/jumping.gif) | ![BMO reviews](media/review.gif) |

| Blocked | Walking right | Walking left |
|:---:|:---:|:---:|
| ![BMO blocked](media/failed.gif) | ![BMO walks right](media/running-right.gif) | ![BMO walks left](media/running-left.gif) |

| Looking around | Idle and jump |
|:---:|:---:|
| ![BMO looks around](media/look-loop.gif) | ![BMO jumps from idle](media/idle-jump-idle.gif) |

The gallery uses compact, animated previews of the existing sprite frames. 🩵

## What this project changes

- Loops BMO's Pong animation while work is running.
- Tracks pointer movement and turns BMO's gaze while idle.
- Makes blinking snappier with shorter closed-eye frames.
- Preserves the existing BMO sprite artwork.

## Platform support

| Platform | Status |
|---|---|
| Linux (X11) | Patch targets one pinned ChatGPT desktop build. |
| Linux (Wayland) | Experimental; launch through XWayland. Pointer tracking depends on compositor setup. |
| macOS | Not yet ported or tested. |
| Windows | Not yet ported or tested. |

We want to bring this project to macOS and Windows. Each system needs a safe installer and matching app-build checks. Contributions from users with those systems are welcome; include app version and test results.

## Linux install

This experimental patch targets a specific Linux app archive. It checks the original archive hash and stops if it finds another version. App updates may replace the patch.

1. Install the matching app build and preserve the original archive backup.
2. Clone this repository and run `python3 build_patch.py`.
3. Review the generated archive and installer before applying it. Installation needs administrator privileges.
4. Start the app with `bash restart-x11.sh`.

The animated previews show sprite frames, not recordings of the live app. The full app is never distributed here.

## Disclaimer

Unofficial community project. Not affiliated with or endorsed by OpenAI or Cartoon Network. ChatGPT and BMO belong to their respective owners. Use only with software you are authorized to modify. See [LICENSE](LICENSE).
