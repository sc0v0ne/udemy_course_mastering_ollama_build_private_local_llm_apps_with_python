class ModelFile:
    def __init__(self, model: str, name_custom: str, system: str, temp: float = 0.1) -> None:
        self.__model = model
        self.__name_custom = name_custom
        self.__system = system
        self.__temp = temp

    @property
    def name_custom(self):
        return self.__name_custom

    def get_description(self):
        return (
            f"FROM {self.__model}\n"
            f"SYSTEM {self.__system}\n"
            f"PARAMETER temperature {self.__temp}\n"
        )