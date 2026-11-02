# Changelog

## 0.50.0
- New interaction model for the mini over a game: it only reacts while the QAM is open (normal touch); with the QAM closed it is locked (padlock). With the QAM open, Left from the main column focuses the mini (D-pad moves, A pauses, L1/R1 size, B returns). With no game running it behaves normally. Experimental: game detection and main-column detection.
- Closing (X) in normal mode now ends everything: pauses audio, destroys the view and stops the daemon. The Steam shortcut opens it again.
- Animated loading card in the app's style and an in-page splash; faster open (polling every 0.5 s).
- Elegant notice when launched in desktop mode (no Steam Big Picture / CEF).
- `report`: diagnostic report with redacted data (nothing is sent). Crash capture in `crashes/`.
- `update`: apply a zip or download the latest GitHub release; keeps your configuration; no need to run install.sh again.
- `key` and `page` commands for Shorts experiments; up/down buttons in mini with vertical video; `mini_shorts` (experimental).
- Launcher, messages, report and docs in English; Spanish command names kept as aliases.

## 0.49
- Per-window `fit` quality, touch-drag in move mode.
