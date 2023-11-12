import rich


class DottyFileException(Exception):
    def __init__(self, file: str, message: str):
        super().__init__(message)
        rich.print("❌ [red bold]ERROR[/red bold]: Cannot add file")
        rich.print(f"'[blue]{file}[/blue]' [[red]{message}[/red]]")
        exit(1)


class DottyConfigException(Exception):
    def __init__(self, message: str):
        super().__init__()
        rich.print("❌ [red bold]ERROR[/red bold]: Cannot load config")
        rich.print(f"[blue]{message}[/blue]")
        exit(1)
