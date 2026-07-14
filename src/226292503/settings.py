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

from dataclasses import dataclass

from aqt import mw

from . import constants


@dataclass(slots=True)
class AddonSettings:
    restart_enabled: bool = constants.DEFAULT_RESTART_ENABLED
    restart_shortcut: str = constants.DEFAULT_SHORTCUT_RESTART
    close_enabled: bool = constants.DEFAULT_CLOSE_ENABLED
    close_shortcut: str = constants.DEFAULT_SHORTCUT_CLOSE


def _read_bool(raw: dict[str, object], key: str, default: bool) -> bool:
    value = raw.get(key, default)
    return value if isinstance(value, bool) else default


def _read_str(raw: dict[str, object], key: str, default: str) -> str:
    value = raw.get(key, default)
    return value if isinstance(value, str) else default


def _get_raw_config() -> dict[str, object]:
    raw: object = mw.addonManager.getConfig(constants.ADDON_MODULE)
    return raw if isinstance(raw, dict) else {}


def load_settings() -> AddonSettings:
    raw = _get_raw_config()
    if not raw:
        return AddonSettings()
    return AddonSettings(
        restart_enabled=_read_bool(
            raw, constants.CONFIG_KEY_RESTART_ENABLED, constants.DEFAULT_RESTART_ENABLED
        ),
        restart_shortcut=_read_str(
            raw, constants.CONFIG_KEY_RESTART_SHORTCUT, constants.DEFAULT_SHORTCUT_RESTART
        ),
        close_enabled=_read_bool(
            raw, constants.CONFIG_KEY_CLOSE_ENABLED, constants.DEFAULT_CLOSE_ENABLED
        ),
        close_shortcut=_read_str(
            raw, constants.CONFIG_KEY_CLOSE_SHORTCUT, constants.DEFAULT_SHORTCUT_CLOSE
        ),
    )


def save_settings(settings: AddonSettings) -> None:
    # Parte del config existente para no destruir "_meta" (welcome_shown, etc.)
    config = _get_raw_config()
    config[constants.CONFIG_KEY_RESTART_ENABLED] = settings.restart_enabled
    config[constants.CONFIG_KEY_RESTART_SHORTCUT] = settings.restart_shortcut
    config[constants.CONFIG_KEY_CLOSE_ENABLED] = settings.close_enabled
    config[constants.CONFIG_KEY_CLOSE_SHORTCUT] = settings.close_shortcut
    mw.addonManager.writeConfig(constants.ADDON_MODULE, config)


def is_welcome_shown() -> bool:
    raw = _get_raw_config()
    meta = raw.get(constants.CONFIG_KEY_META, {})
    if not isinstance(meta, dict):
        return False
    return bool(meta.get(constants.META_KEY_WELCOME_SHOWN, False))


def mark_welcome_shown() -> None:
    config = _get_raw_config()
    meta = config.get(constants.CONFIG_KEY_META, {})
    if not isinstance(meta, dict):
        meta = {}
    meta[constants.META_KEY_WELCOME_SHOWN] = True
    config[constants.CONFIG_KEY_META] = meta
    mw.addonManager.writeConfig(constants.ADDON_MODULE, config)
