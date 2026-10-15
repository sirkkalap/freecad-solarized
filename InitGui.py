# SPDX-License-Identifier: LGPL-2.1-or-later
"""FreeCAD GUI addon entry point."""
import FreeCADGui as Gui
from solarized import theme


class ThemeCommand:
    def __init__(self, restore=False):
        self.restore = restore

    def GetResources(self):
        return {'MenuText': 'Restore previous colors' if self.restore else 'Apply Solarized Dark',
                'ToolTip': 'Restore saved appearance' if self.restore else
                           'Apply Solarized viewport colors and model-tree selection'}

    def IsActive(self):
        return True

    def Activated(self):
        (theme.restore if self.restore else theme.apply)()


Gui.addCommand('Solarized_Apply', ThemeCommand())
Gui.addCommand('Solarized_Restore', ThemeCommand(restore=True))


class SolarizedWorkbench(Gui.Workbench):
    MenuText = 'Solarized'
    ToolTip = 'Solarized colors and readable selection for FreeCAD'

    def Initialize(self):
        commands = ['Solarized_Apply', 'Solarized_Restore']
        self.appendMenu('Solarized', commands)
        self.appendToolbar('Solarized', commands)

    def GetClassName(self):
        return 'Gui::PythonWorkbench'


Gui.addWorkbench(SolarizedWorkbench())
theme.resume()
