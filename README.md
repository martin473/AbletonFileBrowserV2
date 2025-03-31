# AbletonFileBrowserV2
Required libraries:
I may be missing a few but this basically runs with abletoolz, pyside6 and a few other packages automatically installed with qt creator on mac

Difference from v1: Used WYSIWYG Editor QT Creator instead of PyQt6 for GUI Development. QT Creator uses Pyside6 which is functionally similar

What this software does:
Select a folder, search for all .als files. Open files directly from this browser. Create a database of every file. Search, sort, favorite, tag and more. Allows for functionality ableton 11 and earlier versions did not have.
![Screenshot 2025-03-30 at 7 02 47 PM](https://github.com/user-attachments/assets/32ea6f71-91b5-4161-9716-7a1c530541f5)
![Screenshot 2025-03-30 at 7 01 47 PM](https://github.com/user-attachments/assets/f7e4ee3c-9892-4133-b8e1-92fe0db63099)

Why it was deprecated:
SDLC for multiplatform consumer software with python and QT Creator is cumbersome. Flutter and a few other modern code paradigms are better suited for this. Ableton Live 12 includes tagging and a few other features. Most of the functionality in this software can be directly replicated or hacked together out of those features. Future development for this type of software would make more sense as a direct plugin or addon to Ableton.

What it uses:
Abletoolz for parsing ableton files and directory trees. The functionality used in abletoolz currently is code I handwrote in v1, so nothing super special about the directory parsing. But Abletoolz is a robust GPL lisence software that can detect broken plugins, broken files, and potentially do automated repair. My goal to add more functionality and make this more of a ableton file multitool but I solved 99% of the problems this software was built for by changing the way I used Ableton.

Future suggestions: It would be nice if ableton had a plugin environment other than max msp. Parsing ableton through max's live tree is less than ideal and doesn't always provide the type of accessibility or overall look you want from a plugin.
