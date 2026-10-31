# Instructor map

Instructor 8.1 is the bar for this editor. This page lists the jobs an author did with it, not the programs that did them. Nothing here is copied from the product. Behavior that is not already written down goes in a note first, and the code is written from the note.

Status is `not started`, `started`, or `done`. Items are the numbers in the editor work order. A pull request that finishes a job, or starts one, changes its line in the same pull request.

| Job | Status | Items | Where it is today |
|---|---|---|---|
| Make a book | started | 1–25, 118–120, 145 | New, Open, Save, and Save as in the Author window. Save writes an `.fbk`. No start window and no templates yet. |
| Make a page | started | 26–34, 122 | Add and Delete under the page list. `author/document.py` adds, deletes, and moves pages. No duplicate, rename, or reorder in the window yet. |
| Make a background | started | 12, 17, 86–88 | The Background layer in Author. Shapes are tagged `layer: background` on each page. No shared background page yet. |
| Place an object | started | 49–61, 125–135 | Button, Field, Rectangle, Line, Ellipse, Polygon, Arc, and Picture place a shape where you drag. No check, radio, list, combo, record, media, or hotword. |
| Set properties | started | 62–71, 124 | Fill and Line set the colour of the selected object. No property pane yet. |
| Write a script | started | 72–80, 141–144 | The selected object's script can be edited and applied. The page script is shown in that pane but not saved from it. Nothing checks a script. No action list. |
| Make a quiz | not started | 81–85 | - |
| Make a menu | not started | 136 | - |
| Import a picture | started | 59, 138–139 | The Picture tool embeds the chosen file as base64 `data`. No size limit, no pixel size shown, no icon preset. |
| Choose a palette | not started | 64, 137 | - |
| Spellcheck | not started | 147 | - |
| Package a catalog | not started | 121, 150–152 | - |
| Run as a student | started | 115, B8 | `python3 -m foolbook book.fbk` opens what the editor saved. No scripted click-through yet. |
| Run as an author | started | 118–119, 122–123 | `python3 -m foolbookeditor` opens the Author window. No start window or right-click menus yet. |

Not on this list, on purpose: an installer, a runtime of our own, and the vendor catalog format. Foolbook is the runtime. A generated `.tbk` shell opening in the vendor runtime is its own milestone and does not block any line here.
