import rich


class DottyFileException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        rich.print(f"❌ [red]Cannot add file: {message}[/red].")
        exit(1)


class DottyConfigException(Exception):
    def __init__(self, message: str):
        super().__init__()
        rich.print("❌ [red]Cannot load config[/red].")
        rich.print(f"[blue]{message}[/blue]")
        exit(1)
