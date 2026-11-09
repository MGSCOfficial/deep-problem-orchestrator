import json
import sys

# ANSI Colors for Human Console
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[38;2;40;200;64m"
RED = "\033[38;2;230;40;40m"
YELLOW = "\033[38;2;240;180;30m"
CYAN = "\033[38;2;30;200;240m"
GRAY = "\033[38;2;140;140;140m"
PURPLE = "\033[38;2;180;100;250m"


def emit_agent(payload: dict) -> None:
    """
    Emite una respuesta de ultra-alta densidad en JSON compacto (1 sola línea)
    diseñada para consumir menos de 25 tokens por parte de los agentes IA.
    """
    print(json.dumps(payload, separators=(',', ':'), ensure_ascii=False))


def emit_human(title: str, message: str, status: str = "INFO", details: dict = None) -> None:
    """
    Renderiza un dashboard visual legible para operadores humanos en consola con colores ANSI.
    """
    status_colors = {
        "INFO": (CYAN, "[INFO]"),
        "SUCCESS": (GREEN, "[OK]"),
        "WARNING": (YELLOW, "[WARN]"),
        "ERROR": (RED, "[ERROR]"),
        "LOCK": (PURPLE, "[LOCK]"),
    }
    color, tag = status_colors.get(status, (GRAY, f"[{status}]"))

    print(f"{color}{BOLD}{tag} {title}{RESET}")
    if message:
        print(f"  {message}")
    if details:
        for k, v in details.items():
            print(f"  {GRAY}•{RESET} {BOLD}{k}:{RESET} {v}")
    print()
