# Copyright (C) 2026 AnkiCraft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QKeySequence,
    QKeySequenceEdit,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from . import constants
from .logic import reload_shortcuts
from .settings import AddonSettings, load_settings, save_settings
from .strings import tr
from .support import build_support_row


class _ShortcutRow:
    def __init__(self, checkbox_text: str, enabled: bool, sequence: str) -> None:
        self._saved_sequence = sequence
        self.checkbox = QCheckBox(checkbox_text)
        self.checkbox.setChecked(enabled)
        self.edit = QKeySequenceEdit(QKeySequence(sequence))
        self.edit.setMaximumSequenceLength(1)
        self.edit.setClearButtonEnabled(True)
        self.edit.setEnabled(enabled)
        self.checkbox.toggled.connect(self.edit.setEnabled)

    def apply(self, enabled: bool, sequence: str) -> None:
        self.checkbox.setChecked(enabled)
        self.edit.setKeySequence(QKeySequence(sequence))
        self.edit.setEnabled(enabled)

    def is_enabled(self) -> bool:
        return self.checkbox.isChecked()

    def sequence_text(self) -> str:
        # Si la persona deja el campo vacío, se conserva el atajo que ya tenía guardado.
        return self.edit.keySequence().toString() or self._saved_sequence


class ConfigDialog(QDialog):
    def __init__(self) -> None:
        super().__init__(mw)
        self.setWindowTitle(constants.ADDON_DISPLAY_NAME)
        settings = load_settings()

        self._restart_row = _ShortcutRow(
            tr("restart_checkbox"), settings.restart_enabled, settings.restart_shortcut
        )
        self._close_row = _ShortcutRow(
            tr("close_checkbox"), settings.close_enabled, settings.close_shortcut
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        restore_button = QPushButton(tr("restore_defaults"))
        restore_button.setAutoDefault(False)
        restore_button.clicked.connect(self._on_restore_defaults)
        buttons.addButton(restore_button, QDialogButtonBox.ButtonRole.ResetRole)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        for row in (self._restart_row, self._close_row):
            layout.addWidget(row.checkbox)
            shortcut_line = QHBoxLayout()
            shortcut_line.addSpacing(24)
            shortcut_line.addWidget(QLabel(tr("shortcut_label")))
            shortcut_line.addWidget(row.edit, stretch=1)
            layout.addLayout(shortcut_line)
            layout.addSpacing(6)
        layout.addWidget(buttons)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addSpacing(10)
        layout.addWidget(separator)
        layout.addWidget(build_support_row(self))

        self.setMinimumWidth(420)
        self._restart_row.checkbox.setFocus()

    def _on_restore_defaults(self) -> None:
        self._restart_row.apply(
            constants.DEFAULT_RESTART_ENABLED, constants.DEFAULT_SHORTCUT_RESTART
        )
        self._close_row.apply(
            constants.DEFAULT_CLOSE_ENABLED, constants.DEFAULT_SHORTCUT_CLOSE
        )

    def _on_accept(self) -> None:
        restart_sequence = self._restart_row.sequence_text()
        close_sequence = self._close_row.sequence_text()
        both_active = self._restart_row.is_enabled() and self._close_row.is_enabled()
        if both_active and restart_sequence and restart_sequence == close_sequence:
            QMessageBox.warning(self, tr("dialog_title"), tr("duplicate_shortcut"))
            return

        save_settings(
            AddonSettings(
                restart_enabled=self._restart_row.is_enabled(),
                restart_shortcut=restart_sequence,
                close_enabled=self._close_row.is_enabled(),
                close_shortcut=close_sequence,
            )
        )
        reload_shortcuts()
        self.accept()


def open_config_dialog() -> None:
    try:
        ConfigDialog().exec()
    except Exception as exc:
        QMessageBox.critical(mw, tr("error_title"), tr("unexpected_error", error=str(exc)))
