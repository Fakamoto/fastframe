import typer
from pathlib import Path
from typing import Annotated, Optional
from shutil import copytree
from importlib.metadata import version
from rich import print


__version__ = version("fastframe")

app = typer.Typer(
    name="fastframe",  # Set the name of the CLI
    no_args_is_help=True,  # Show help message if no arguments are provided
    pretty_exceptions_show_locals=True,  # Do not display local variables when an exception occurs
)


# Version callback
def version_callback(show_version: bool):
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()


# Add a --version option
@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    pass



## Commands

@app.command(help="Creates a FastAPI project directory structure for the given project name in the current directory or optionally in the given directory.")
def init(name: Annotated[str, typer.Argument(help="Name of the project.")], directory: Annotated[Optional[Path], typer.Option(help="destination directory", dir_okay=True, resolve_path=True)] = None):
    project_template = Path(__file__).resolve().parent / "templates" / "project"
    # Check if directory is specified, if not use current directory
    directory = directory or Path.cwd()
    project_dir = directory / name

    if project_dir.exists():
        print(f"[bold red]{project_dir} already exists.[/bold red]")
        raise typer.Exit(1)

    # Create the project directory
    # project_dir.mkdir(parents=True, exist_ok=False)
    
    # Create the project by copying the template
    copytree(project_template, project_dir)

    # replace placeholder with real project name
    for filepath in Path(project_dir).rglob('*'):
        if filepath.is_file():
            content = filepath.read_text()
            content = content.replace("projectname", name)
            filepath.write_text(content)


if __name__ == "__main__":
    app()
