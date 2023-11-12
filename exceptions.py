import rich


class DottyFileException(Exception):
    def __init__(self, file: str, message: str):
        super().__init__(message)
        rich.print("[red bold]ERROR[/red bold]: Cannot add file")
        rich.print(f"'[blue]{file}[/blue]' [[red]{message}[/red]]")
        exit(1)
