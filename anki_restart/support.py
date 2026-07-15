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

import os

from aqt import mw
from aqt.qt import (
    QDesktopServices,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPixmap,
    QPushButton,
    Qt,
    QTimer,
    QUrl,
    QVBoxLayout,
    QWidget,
)

from . import constants
from .settings import is_welcome_shown, mark_welcome_shown
from .strings import tr


def _brand_button(text: str, bg: str, hover: str) -> QPushButton:
    button = QPushButton(text)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: {bg};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        """
    )
    return button


class WelcomeDialog(QDialog):
    def __init__(self) -> None:
        super().__init__(mw)
        self.setWindowTitle(
            tr("welcome_title", name=constants.ADDON_NAME, version=constants.ADDON_VERSION)
        )

        layout = QVBoxLayout(self)

        logo_path = os.path.join(os.path.dirname(__file__), constants.LOGO_FILENAME)
        if os.path.isfile(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label = QLabel()
                logo_label.setPixmap(
                    pixmap.scaled(
                        constants.LOGO_SIZE_PX,
                        constants.LOGO_SIZE_PX,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                logo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                layout.addWidget(logo_label)

        title_label = QLabel(
            tr("version_line", name=constants.ADDON_NAME, version=constants.ADDON_VERSION)
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {constants.COLOR_ACCENT};"
        )
        layout.addWidget(title_label)

        author_label = QLabel(f"by {constants.AUTHOR_NAME}")
        author_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        author_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(author_label)

        body_label = QLabel(tr("welcome_body"))
        body_label.setWordWrap(True)
        body_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(8)
        layout.addWidget(body_label)

        note_label = QLabel(tr("welcome_support_note"))
        note_label.setWordWrap(True)
        note_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        note_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addSpacing(6)
        layout.addWidget(note_label)

        layout.addSpacing(10)
        button_row = QHBoxLayout()

        if constants.ANKIWEB_ID:
            rate_button = _brand_button(
                tr("rate_button"), constants.COLOR_RATE_BG, constants.COLOR_RATE_HOVER
            )
            rate_button.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl(constants.ANKIWEB_REVIEW_URL))
            )
            button_row.addWidget(rate_button)

        kofi_button = _brand_button(
            tr("kofi_button"), constants.COLOR_KOFI_BG, constants.COLOR_KOFI_HOVER
        )
        kofi_button.setToolTip(tr("kofi_tooltip"))
        kofi_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(constants.URL_KOFI)))
        button_row.addWidget(kofi_button)

        patreon_button = _brand_button(
            tr("patreon_button"), constants.COLOR_PATREON_BG, constants.COLOR_PATREON_HOVER
        )
        patreon_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(constants.URL_PATREON))
        )
        button_row.addWidget(patreon_button)

        layout.addLayout(button_row)

        close_button = QPushButton(tr("welcome_close"))
        close_button.setDefault(True)
        close_button.clicked.connect(self.accept)
        layout.addSpacing(6)
        layout.addWidget(close_button)
        close_button.setFocus()

        self.setMinimumWidth(360)


def build_support_row(parent: QWidget) -> QWidget:
    row = QWidget(parent)
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)

    info_label = QLabel(
        f'{constants.ADDON_NAME} v{constants.ADDON_VERSION} · '
        f'<a href="{constants.URL_REPORT_BUG}">{tr("report_button")}</a>'
    )
    info_label.setOpenExternalLinks(True)
    info_label.setStyleSheet("color: gray; font-size: 10px;")
    layout.addWidget(info_label)
    layout.addStretch(1)

    kofi_button = QPushButton(tr("kofi_button"))
    kofi_button.setToolTip(tr("kofi_tooltip"))
    kofi_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(constants.URL_KOFI)))
    layout.addWidget(kofi_button)

    patreon_button = QPushButton(tr("patreon_button"))
    patreon_button.clicked.connect(
        lambda: QDesktopServices.openUrl(QUrl(constants.URL_PATREON))
    )
    layout.addWidget(patreon_button)

    if constants.ANKIWEB_ID:
        rate_button = QPushButton(tr("rate_button"))
        rate_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(constants.ANKIWEB_REVIEW_URL))
        )
        layout.addWidget(rate_button)

    return row


def _show_welcome_dialog() -> None:
    WelcomeDialog().exec()


def maybe_show_welcome() -> None:
    if is_welcome_shown():
        return
    # Se marca ANTES de mostrarse para que un cierre inesperado durante el
    # diálogo no deje el flag a medias y lo repita en el siguiente arranque.
    mark_welcome_shown()
    QTimer.singleShot(constants.WELCOME_DELAY_MS, _show_welcome_dialog)
