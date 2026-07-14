from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field

from aqt import mw
from aqt.qt import QKeySequence, QLocalServer, QMessageBox, QShortcut

from .settings import load_settings
from .strings import tr


@dataclass(slots=True)
class _AddonState:
    shortcuts: list[QShortcut] = field(default_factory=list)
    restart_pending: bool = False


_state: _AddonState = _AddonState()


def _show_error(message: str) -> None:
    QMessageBox.critical(mw, tr("error_title"), message)


def _resolve_anki_executable() -> str | None:
    executable = sys.executable or ""
    if os.path.basename(executable).lower().startswith("anki"):
        return executable
    if candidate := shutil.which("anki"):
        return candidate
    return executable or None


def _release_single_instance_lock() -> None:
    # Anki reserva un socket local para detectar segundas instancias; si sigue
    # abierto, la nueva instancia se cerraría creyendo que Anki ya está en marcha
    app = mw.app
    server = getattr(app, "_srv", None)
    if isinstance(server, QLocalServer):
        server.close()
    key = getattr(type(app), "KEY", None)
    if isinstance(key, str):
        QLocalServer.removeServer(key)


def _spawn_detached(executable: str) -> None:
    creationflags = 0
    if sys.platform == "win32":
        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )
    subprocess.Popen(
        [executable],
        close_fds=True,
        start_new_session=True,
        creationflags=creationflags,
    )


def _launch_new_instance(executable: str) -> None:
    # se ejecuta al salir: la colección ya está guardada, cerrada y con la copia
    # de seguridad terminada, así que la nueva instancia no puede pisar nada
    try:
        _release_single_instance_lock()
        _spawn_detached(executable)
    except Exception as exc:
        print(f"[quick_restart] no se pudo lanzar la nueva instancia: {exc}")


def restart_anki() -> None:
    try:
        if _state.restart_pending:
            return
        executable = _resolve_anki_executable()
        if not executable:
            _show_error(tr("executable_not_found"))
            return

        _state.restart_pending = True
        mw.app.aboutToQuit.connect(lambda: _launch_new_instance(executable))
        # cierre idéntico al de un cierre normal de Anki: guarda la colección,
        # respeta la sincronización al cerrar y espera a la copia de seguridad
        mw.unloadProfileAndExit()
    except Exception as exc:
        _state.restart_pending = False
        _show_error(tr("unexpected_error", error=str(exc)))


def close_anki() -> None:
    try:
        mw.close()
    except Exception as exc:
        _show_error(tr("unexpected_error", error=str(exc)))


def unregister_shortcuts() -> None:
    for shortcut in _state.shortcuts:
        try:
            shortcut.activated.disconnect()
        except (TypeError, RuntimeError):
            pass
        shortcut.setParent(None)
        shortcut.deleteLater()
    _state.shortcuts.clear()


def register_shortcuts() -> None:
    settings = load_settings()
    entries: list[tuple[bool, str, Callable[[], None]]] = [
        (settings.restart_enabled, settings.restart_shortcut, restart_anki),
        (settings.close_enabled, settings.close_shortcut, close_anki),
    ]
    for enabled, key_sequence, slot in entries:
        if not enabled:
            continue
        sequence = QKeySequence(key_sequence)
        if sequence.isEmpty():
            continue
        shortcut = QShortcut(sequence, mw)
        shortcut.activated.connect(slot)
        _state.shortcuts.append(shortcut)


def reload_shortcuts() -> None:
    unregister_shortcuts()
    register_shortcuts()


def on_main_window_did_init() -> None:
    try:
        register_shortcuts()
    except Exception as exc:
        _show_error(tr("unexpected_error", error=str(exc)))
