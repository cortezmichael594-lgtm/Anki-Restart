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

from typing import Final

ADDON_MODULE: Final[str] = __name__.split(".", 1)[0]

CONFIG_KEY_RESTART_ENABLED: Final[str] = "restart_enabled"
CONFIG_KEY_RESTART_SHORTCUT: Final[str] = "restart_shortcut"
CONFIG_KEY_CLOSE_ENABLED: Final[str] = "close_enabled"
CONFIG_KEY_CLOSE_SHORTCUT: Final[str] = "close_shortcut"

DEFAULT_RESTART_ENABLED: Final[bool] = True
DEFAULT_SHORTCUT_RESTART: Final[str] = "Ctrl+R"
DEFAULT_CLOSE_ENABLED: Final[bool] = True
DEFAULT_SHORTCUT_CLOSE: Final[str] = "Ctrl+W"

# --- AnkiCraft branding -----------------------------------------------------

ADDON_NAME: Final[str] = "Quick Restart"
ADDON_DISPLAY_NAME: Final[str] = (
    "Quick Restart — restart or close Anki with a shortcut (by Ankicraft)"
)
ADDON_VERSION: Final[str] = "1.0.0"
AUTHOR_NAME: Final[str] = "AnkiCraft"

ANKIWEB_ID: Final[str] = "226292503"
ANKIWEB_PAGE_URL: Final[str] = f"https://ankiweb.net/shared/info/{ANKIWEB_ID}"
ANKIWEB_REVIEW_URL: Final[str] = f"https://ankiweb.net/shared/review/{ANKIWEB_ID}"

URL_KOFI: Final[str] = "https://ko-fi.com/ankicraft"
URL_PATREON: Final[str] = "https://www.patreon.com/cw/Ankicraft594"
URL_REPORT_BUG: Final[str] = ANKIWEB_PAGE_URL

LOGO_FILENAME: Final[str] = "logo.png"
LOGO_SIZE_PX: Final[int] = 72

COLOR_ACCENT: Final[str] = "#7C5CE0"
COLOR_KOFI_BG: Final[str] = "#29ABE0"
COLOR_KOFI_HOVER: Final[str] = "#1E8FBF"
COLOR_PATREON_BG: Final[str] = "#FF424D"
COLOR_PATREON_HOVER: Final[str] = "#E0313C"
COLOR_RATE_BG: Final[str] = "#F5A623"
COLOR_RATE_HOVER: Final[str] = "#D98E12"

CONFIG_KEY_META: Final[str] = "_meta"
META_KEY_WELCOME_SHOWN: Final[str] = "welcome_shown"
WELCOME_DELAY_MS: Final[int] = 2000
