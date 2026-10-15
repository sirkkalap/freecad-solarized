# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit apply/restore commands; imports do not change preferences."""
import json

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

from .palette import COLORS, FLAGS

VIEW = 'User parameter:BaseApp/Preferences/View'
STATE = 'User parameter:BaseApp/Preferences/Mod/Solarized'
STYLE = '''
QTreeWidget::item:selected, QTreeWidget::item:selected:!active {
    background-color: #073642;
    color: #fdf6e3;
    border: 1px solid #b58900;
}
'''
_timer = None
_trees = []


def _style_trees():
    for tree in Gui.getMainWindow().findChildren(QtWidgets.QTreeWidget):
        if tree.metaObject().className() != 'Gui::TreeWidget':
            continue
        if not tree.property('solarizedStyleApplied'):
            tree.setProperty('solarizedOriginalStyle', tree.styleSheet())
            tree.setProperty('solarizedStyleApplied', True)
            tree.setStyleSheet(tree.styleSheet() + STYLE)
            _trees.append(tree)


def _start_tree_style():
    global _timer
    if _timer is None:
        _timer = QtCore.QTimer(Gui.getMainWindow())
        _timer.timeout.connect(_style_trees)
    _style_trees()
    _timer.start(1000)


def apply():
    """Save a baseline once, apply colors, and enable persistence on startup."""
    view, state = App.ParamGet(VIEW), App.ParamGet(STATE)
    if not state.GetString('Backup', ''):
        existing = {name: value for kind, name, value in view.GetContents()}
        backup = {name: {'present': name in existing, 'value': existing.get(name)}
                  for name in list(COLORS) + list(FLAGS)}
        state.SetString('Backup', json.dumps(backup))
        App.saveParameter()
    for name, color in COLORS.items():
        view.SetUnsigned(name, (int(color[1:], 16) << 8) | 255)
    for name, value in FLAGS.items():
        view.SetBool(name, value)
    state.SetBool('Enabled', True)
    App.saveParameter()
    _start_tree_style()
    App.Console.PrintMessage('Solarized applied. Reopen sketches to refresh axis colors.\n')


def restore():
    """Restore values captured before the first apply, preserving absent keys."""
    view, state = App.ParamGet(VIEW), App.ParamGet(STATE)
    raw = state.GetString('Backup', '')
    if not raw:
        App.Console.PrintMessage('No Solarized preference backup is available.\n')
        return
    backup = json.loads(raw)
    for name, old in backup.items():
        if name not in COLORS and name not in FLAGS:
            continue
        if old['present']:
            setter = view.SetBool if name in FLAGS else view.SetUnsigned
            setter(name, old['value'])
        else:
            remover = view.RemBool if name in FLAGS else view.RemUnsigned
            remover(name)
    state.SetBool('Enabled', False)
    App.saveParameter()
    if _timer is not None:
        _timer.stop()
    for tree in _trees:
        try:
            if tree.property('solarizedStyleApplied'):
                tree.setStyleSheet(tree.property('solarizedOriginalStyle') or '')
                tree.setProperty('solarizedStyleApplied', False)
        except RuntimeError:
            pass  # Widget was deleted during a workbench change.
    _trees.clear()
    state.RemString('Backup')
    App.saveParameter()
    App.Console.PrintMessage('Previous colors restored. Reopen sketches to refresh axes.\n')


def resume():
    """Reapply the model-tree style on startup only after explicit activation."""
    if App.ParamGet(STATE).GetBool('Enabled', False):
        _start_tree_style()
