from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.table import Table

console = Console()

def render_user(text: str):
    console.print(f"\n[bold cyan]You:[/] {text}")

def render_assistant_streaming(token_iter) -> str:
    buf = ""
    console.print("\n[bold green]Assistant:[/]")
    with Live(Markdown("▌"), refresh_per_second=20, console=console) as live:
        for tok in token_iter:
            buf += tok
            live.update(Markdown(buf + "▌"))
    return buf

def render_session_list(sessions: list[dict]):
    if not sessions:
        console.print("[yellow]No sessions found.[/]")
        return
    t = Table(title="Saved Sessions", show_lines=True)
    t.add_column("ID", style="cyan")
    t.add_column("Last Updated", style="green")
    t.add_column("Turns", style="magenta", justify="right")
    for s in sessions:
        t.add_row(s["id"], s["updated"][:19], str(s["turns"]))
    console.print(t)