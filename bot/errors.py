class AppError(Exception):
    def __init__(self, reason: str, message: str) -> None:
        super().__init__(f' {reason}')
        self.reason = reason
        self.message = message


class IncorrectCmdError(AppError):
    def __init__(self, cmd: str, text: str, message: str) -> None:
        super().__init__(f'incorrect command: [{cmd}] {text}', message)
        self.cmd = cmd
        self.text = text


class IncorrectAddCmdError(IncorrectCmdError):
    def __init__(self, text: str) -> None:
        super().__init__('/addproduct', text, 'Неправильная команда, пример `addproduct;Массаж;мастер Андрей`')


class EmptyDBError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__('В базе данных пусто:', message)


class DubleDBProductError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__('В базе данных повтор продуктов:', message)


class DubleDBCategoriesError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__('В базе данных повтор категорий:', message)
