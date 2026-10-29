# BMO Desktop Pet

A friendlier BMO for the ChatGPT desktop companion: **Pong while work is running, mouse-aware eyes while idle, and quicker, natural blinks.** A little pixel buddy to keep you company while you work. 💚

![BMO animation preview](https://github.com/tarelturk/bmo-desktop-pet/raw/main/media/bmo-preview.gif)

## What it does

- Keeps the Pong animation looping for the full running state.
- Lets BMO glance toward the pointer while idle.
- Shortens the closed-eye frames so blinking feels crisp.
- Leaves the original sprite artwork intact.

## Compatibility

This experimental patch targets one specific Linux desktop build of ChatGPT. It checks the original app archive's SHA-256 before changing anything and stops if it sees a different build. App updates can replace the patch.

On Wayland, the included launcher tries XWayland because Electron's global pointer-position API is unavailable on Wayland. Pointer tracking can vary with the compositor and XWayland setup.

## Install

1. Install the matching ChatGPT desktop build and keep its original app archive backup.
2. Clone this repository.
3. Build a patched archive locally:

   ```bash
   python3 build_patch.py
   ```

4. Review the patch and install instructions before proceeding. The guarded installer needs administrator access.
5. Start ChatGPT through `bash restart-x11.sh`.

The full ChatGPT application is **not** included or redistributed. The patch is built on your own computer from your installed app. See [SECURITY.md](SECURITY.md) and [LICENSE](LICENSE).

## Restore

Use the installer's restore option, then start ChatGPT normally from your applications menu.

## Preview

The preview shows the custom sprite animation. It is a sample of the frames, not a recording of the live desktop app.

## Disclaimer

Unofficial community project. Not affiliated with or endorsed by OpenAI or Cartoon Network. ChatGPT and BMO remain the property of their respective owners. Use only with software you are authorized to modify; you are responsible for complying with applicable license terms.

## Contributing

Bug reports and compatibility notes are welcome. Please include your Linux desktop session type, ChatGPT app build, and the exact animation behavior you observed. Never attach credentials, account data, or a full app archive.
