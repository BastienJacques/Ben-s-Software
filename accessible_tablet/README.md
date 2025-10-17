Refactor notes

- This is a refactor skeleton of the original comm-v10.py (source). The refactor
splits responsibilities into modules: menu, services (TTS + URL server), storage, utils, and app.
- The original file provided many platform-specific helpers; they are preserved in utils.py
and services but simplified for clarity.
- Next steps:
* Implement the rest of Menu pages (LibraryMenu, EpisodeListMenu, etc.) using MenuFrame.
* Add unit tests and run mypy/pylint. Use Python 3.10+.
