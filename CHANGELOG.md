# Changelog

## Unreleased — 2026-10-31

- Author starts on Select, and Escape goes back to Select from any tool.
- A new rectangle is filled `#f7f4ee` with a `#071428` outline. It had no fill and a black outline.
- Rounded places a rounded rectangle (`kind: roundrect`, `radius: 8`). Foolbook draws it from Foolbook#23 on.
- Polygon is clicked out: each click is a point, double-click or Enter closes it, and Escape drops it with nothing left on the page. It used to be a rectangle you dragged.
- Curve is clicked out like Polygon and stays open. It stores `kind: curve` and its points. Foolbook draws it from Foolbook#26 on.
- A new arc stores `start: 0` and `sweep: 180`, the top half of its bounds, instead of two endpoints. Foolbook draws it from Foolbook#28 on. An arc read from a `.tbk` keeps its endpoints.
- Pie places a filled slice (`kind: pie`, `start: 0`, `sweep: 90`). Foolbook draws it from Foolbook#29 on.
- Chord places a filled chord (`kind: chord`, `start: 0`, `sweep: 180`). Foolbook draws it from Foolbook#30 on.
- Type into a field on the page. A new Field opens for typing, and a double-click with Select reopens one. Several lines are kept as lines. Escape or a click away keeps them.
- Picture embeds the file as base64 PNG by default, or links it beside the book as `src`. A file over 20 MB, or one that is not a picture, is refused with a sentence instead of a crash.
- Hotspot places a `kind: hotspot` with no fill. Author draws its outline so it can be found. Foolbook does not draw it, from Foolbook#31 on, and follows its item.
- A Properties pane sets the selected object's name, text, fill, outline, and line width (`stroke`, default 1). Bad input keeps the old value. Foolbook draws `stroke` from Foolbook#25 on.
- The Properties pane sets font face, size, bold, italic, underline, and alignment (left, center, right). Foolbook reads underline and named alignment from Foolbook#32 and #35 on.
- A colour well of eight plain colours sits under the Properties pane. A click sets the fill and a right-click sets the outline. Typed `#rrggbb` still works.
- No fill, or an empty Fill box, stores `fill: ""` and the object is drawn with nothing inside. A button with no fill saves and draws that way.
- A Visible check box in the Properties pane. An object with `visible: false` is drawn ghosted on the stage, its colours washed toward white, and Foolbook still skips it.

## 0.4.0 — 2026-10-24

- Page and Background are separate. The list and a new object follow the one that is selected. The picture still shows both, background first.
- Line, Ellipse, Polygon, Arc, and Picture place a shape Foolbook draws. Fill and Line set the colour of the selected object. Front and Back move it within its own layer.

## 0.3.5 — 2026-10-24

- Select drags the object under the pointer. The four squares on a selected object pull its corners, and the opposite corner stays put.

## 0.3.4 — 2026-10-24

- The Author window opens large enough for three panes. The picture is the middle one. The page list and the object list cannot push it off the screen.

## 0.3.3 — 2026-10-24

- The desktop window is what opens. `--browser` is the other one.
- Button, Field, and Rectangle place an object where you drag on the picture. Select still picks the object under the pointer.

## 0.3.2 — 2026-10-24

- The browser editor, which is what starts with no `--desktop` flag, now has the page in the middle. Pages stay on the left. Objects and the object script stay on the right. A `.tbk` is read through Foolbook, so the picture is the book's objects.

## 0.3.1 — 2026-10-24

- The middle of Author is the page Foolbook draws. Pages stay on the left and the object script stays on the right. A click on the picture selects the object. Opening a `.tbk` reads it through Foolbook.

## 0.3.0 — 2026-10-24

- Author lists the objects on the selected page, in book order. A field Reader hides is still in the list. The selected object's script can be edited. Save still writes an `.fbk`.

## 0.2.3 — 2026-10-22

- The conversion note that said bitmaps are missing is gone. A button picture is in the `.fbk` once Foolbook 1.0.5r15 has read it.

## 0.2.2 — 2026-10-22

- No loader of its own. A `.tbk` converted after Foolbook 1.0.5r13 keeps the object store: page order, field text, polygon outlines, the background colour, and button bitmaps.
