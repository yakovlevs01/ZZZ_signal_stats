class LogFileNotFoundError(FileNotFoundError):
    def __init__(self, message: str = "Failed to locate log file") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidDataError(Exception):
    def __init__(self, message: str = "Got some wrond data") -> None:
        self.message = message
        super().__init__(self.message)


class HoYoAPIError(Exception):
    def __init__(self, message: str = "idk smth gone wrong") -> None:
        self.message = message
        super().__init__(self.message)
