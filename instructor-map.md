# Instructor map

Instructor 8.1 is the bar for this editor. This page lists the jobs an author did with it, not the programs that did them. Nothing here is copied from the product. Behavior that is not already written down goes in a note first, and the code is written from the note.

Status is `not started`, `started`, or `done`. Items are the numbers in the editor work order. A pull request that finishes a job, or starts one, changes its line in the same pull request. "In review" names pull requests that are open and not yet merged. A job is done only when its pull requests are merged.

| Job | Status | Items | Where it is today |
|---|---|---|---|
| Make a book | started | 1–25, 118–120, 145 | New, Open, Save, and Save as in the Author window. Save writes an `.fbk`. In review: start window (#9), new book size and colour (#16), templates (#24), catalog folder (#28), book properties with first page (#114; reader Foolbook#62). |
| Make a page | started | 26–34, 122, 146 | Add and Delete under the page list. In review: page right-click menu (#33), page transition stored and ignored (#115). |
| Make a background | started | 12, 17, 86–88 | The Background layer in Author. Shapes are tagged `layer: background` on each page. No shared background page yet. |
| Place an object | started | 49–61, 125–135 | Button, Field, Rectangle, Line, Ellipse, Polygon, Arc, and Picture place a shape where you drag. In review: label, field, check, radio, list, combo, picture fit, record, media, and hotword tools (#40–#103; reader Foolbook#42–#58), pattern fills (#110; reader Foolbook#60). |
| Set properties | started | 62–71, 124 | Fill and Line set the colour of the selected object. In review: shape right-click menu (#104), undocked property sheet (#105). |
| Write a script | started | 72–80, 141–144 | The selected object's script can be edited and applied. In review: action lists (#111; reader Foolbook#61), write the equivalent script (#112), drag an action onto an object (#113). |
| Make a quiz | not started | 81–85 | - |
| Make a menu | started | 136 | In review: the book's own menu bar, written as an outline (#106; reader Foolbook#59). |
| Import a picture | started | 59, 138–139 | The Picture tool embeds the chosen file as base64 `data`. In review: stored as PNG with its pixel size, non-pictures refused (#108), 32 by 32 icon preset (#109). |
| Choose a palette | started | 64, 137 | In review: the colours the book already uses, as swatches (#107). |
| Spellcheck | started | 147 | In review: a small built-in word list and the book's own words (#116). |
| Package a catalog | started | 121, 150–152 | In review: Publish writes a folder with the `.fbk`, linked files, and a README (#119), and `books.json` (#120). Foolcourse reads it (Foolcourse#1). Print is the PNG export (#118). |
| Run as a student | started | 115, B8 | `python3 -m foolbook book.fbk` opens what the editor saved. No scripted click-through yet. |
| Run as an author | started | 118–119, 122–123 | `python3 -m foolbookeditor` opens the Author window. No start window or right-click menus yet. |

Not on this list, on purpose: an installer, a runtime of our own, and the vendor catalog format. Foolbook is the runtime. A generated `.tbk` shell opening in the vendor runtime is its own milestone and does not block any line here.
