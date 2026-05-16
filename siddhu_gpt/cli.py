import typer
from dotenv import load_dotenv
from siddhu_gpt.chat import get_client, pick_model, chat_stream, chat_once, list_providers
from siddhu_gpt.memory import load_session, save_session, list_sessions
from siddhu_gpt.ui import render_user, render_assistant_streaming, render_session_list, console

load_dotenv()
app = typer.Typer(help="siddhu-gpt: your personal AI assistant")

@app.command()
def chat(
    provider: str = typer.Option("groq", help="Provider: groq or ollama"),
    model: str = typer.Option(None, help="Override default model"),
    session_id: str = typer.Option("default", help="Session name"),
):
    """Start an interactive chat session."""
    client = get_client(provider)
    mdl = model or pick_model(provider)
    messages = load_session(session_id)

    console.print(f"[bold]siddhu-gpt[/] | provider=[cyan]{provider}[/] model=[green]{mdl}[/] session=[yellow]{session_id}[/]")
    console.print("Type [bold]/quit[/] to exit.\n")

    while True:
        try:
            user = typer.prompt(">")
        except (KeyboardInterrupt, EOFError):
            break
        if user.strip() in {"/quit", "/exit", "quit", "exit", ""}:
            break
        messages.append({"role": "user", "content": user})
        render_user(user)
        text = render_assistant_streaming(chat_stream(client, messages, mdl))
        messages.append({"role": "assistant", "content": text})
        save_session(session_id, messages)

@app.command()
def sessions():
    """List all saved sessions."""
    render_session_list(list_sessions())

@app.command()
def summary(session_id: str = typer.Argument("default")):
    """Summarize a saved session using the LLM."""
    msgs = load_session(session_id)
    if not msgs:
        console.print(f"[red]No session found:[/] {session_id}")
        raise typer.Exit(1)
    client = get_client("groq")
    model = pick_model("groq")
    prompt = [{"role": "user", "content": f"Summarize this conversation in 3 bullet points:\n\n{msgs}"}]
    result = chat_once(client, prompt, model)
    console.print(f"\n[bold]Summary of '{session_id}':[/]")
    from rich.markdown import Markdown
    console.print(Markdown(result))

@app.command()
def providers():
    """Show which providers have valid keys configured."""
    for p in list_providers():
        console.print(f"[green]✓[/] {p}")