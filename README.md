# FreeCAD Solarized

Standalone appearance addon extracted from our FreeCAD color configuration.
Independent of Constraint Inspector. Requires FreeCAD GUI with bundled PySide;
no pip dependencies or build step. Intended for FreeCAD 1.1.x; the packaged
addon has not yet been tested in an installed FreeCAD session.

## Installation and use

Find the user directory with `print(App.getUserAppDataDir())` in FreeCAD's Python
console. Symlink this entire project into its `Mod/FreeCADSolarized` directory,
then restart FreeCAD. On this Mac:

```sh
ln -s /Users/petes/proj/freecad-mcp-test/freecad-solarized \
  "$HOME/Library/Application Support/FreeCAD/v1-1/Mod/FreeCADSolarized"
```

Select the **Solarized** workbench, then **Solarized → Apply Solarized Dark**.
Switch back to Sketcher to continue working. Reopen sketches to reload axis
colors. The model-tree selection style is reapplied automatically after restart
once the addon has been explicitly enabled. It does not style the entire UI.

## Palette

Uses the original [Solarized HEX values](https://ethanschoonover.com/solarized/):

| Role | Color |
| --- | --- |
| Background | base03 `#002b36` |
| Geometry | base0 `#839496` |
| Selection | base3 `#fdf6e3` |
| Hover | violet `#6c71c4` |
| Fully constrained | green `#859900` |
| Construction / Z axis | blue `#268bd2` |
| X / Y axes | red `#dc322f` / green `#859900` |
| Tree selection | base02 background, base3 text, yellow border |

Other constraint colors are defined in `solarized/palette.py`. Colors apply to
FreeCAD preferences globally, not just the active document. Icons retain their
original artwork and colors.

## Restore and uninstall

**Solarized → Restore previous colors** restores the preferences captured before
the first apply and removes the tree styling. Repeated apply preserves that
baseline. Settings and the baseline are stored in FreeCAD user parameters under
`BaseApp/Preferences/Mod/Solarized`. Restore before removing the installation
symlink and restarting FreeCAD. Current pre-existing Solarized customizations
are the baseline if they were already active when applying this addon.

## Development

`InitGui.py` delegates startup to `solarized/gui.py`, which registers the workbench; `solarized/theme.py` applies and restores
preferences; `solarized/palette.py` contains the palette. No automated tests
have been added. Run and inspect UI behavior inside FreeCAD when requested.
The addon never edits CAD geometry or saves documents.

## License

The addon implementation is licensed under LGPL-2.1-or-later; see
[LICENSE](LICENSE). The upstream Solarized material retains its MIT license.

## Attribution and third-party license

[Solarized](https://ethanschoonover.com/solarized/) was created by
**Ethan Schoonover**. Copyright (c) 2011 Ethan Schoonover.

This addon adapts the Solarized palette for FreeCAD. Its cream selection,
violet hover and model-tree styling are this project's choices; the color
values come from Solarized. This is an independent port.

Solarized is distributed under the MIT license. The original copyright,
permission notice and warranty disclaimer are reproduced in
[LICENSES/Solarized-MIT.txt](LICENSES/Solarized-MIT.txt), from the
[upstream license](https://github.com/altercation/solarized/blob/master/LICENSE).
Keep that file with redistributed copies of the addon. Redistributing the
addon implementation must also comply with its LGPL license.
