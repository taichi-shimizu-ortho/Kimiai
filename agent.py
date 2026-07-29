import sys
from pathlib import Path
from kimi_client import ask_kimi
from tools.file_tools import read_file, write_file, list_files
from tools.shell_tools import run_shell
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def load_system_prompt():
    prompt_path = Path("prompts/system_prompt.md")
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a helpful coding assistant."

def main():
    system_prompt = load_system_prompt()

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    console.print("[bold green]Kimi Coding Agent started.[/bold green]")
    console.print("Commands:")
    console.print("  [cyan]/files[/cyan]           - List files in workspace")
    console.print("  [cyan]/read <path>[/cyan]     - Read a file from workspace")
    console.print("  [cyan]/test <command>[/cyan]  - Run a shell command in workspace")
    console.print("  [cyan]/exit[/cyan]            - Exit the agent")
    console.print("\nType your request or use a command.")

    while True:
        try:
            user_input = console.input("\n[bold blue]You>[/bold blue] ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break

        if user_input == "/files":
            files = list_files(".")
            if not files:
                console.print("[yellow]No files found in workspace.[/yellow]")
            else:
                console.print("\n".join(files))
            continue

        if user_input.startswith("/read "):
            path = user_input.removeprefix("/read ").strip()
            content = read_file(path)
            console.print(f"\n[bold]Content of {path}:[/bold]\n")
            console.print(content)
            continue

        if user_input.startswith("/test "):
            command = user_input.removeprefix("/test ").strip()
            console.print(f"[dim]Running: {command}[/dim]")
            result = run_shell(command)
            console.print(f"returncode: {result['returncode']}")
            if result["stdout"]:
                console.print(f"[green]stdout:[/green]\n{result['stdout']}")
            if result["stderr"]:
                console.print(f"[red]stderr:[/red]\n{result['stderr']}")
            continue

        # Normal chat
        messages.append({"role": "user", "content": user_input})
        
        with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
            answer = ask_kimi(messages)
            
        messages.append({"role": "assistant", "content": answer})

        console.print("\n[bold magenta]Agent>[/bold magenta]")
        console.print(Markdown(answer))

if __name__ == "__main__":
    main()
