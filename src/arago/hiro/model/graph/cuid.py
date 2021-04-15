class Cuid(str):
    # de.arago.graphit.server.api.graph.GraphIdGenerator
    # https://github.com/ericelliott/cuid
    # https://github.com/prisma/cuid-java
    # https://github.com/necaris/cuid.py

    @property
    def valid(self) -> bool:
        if self.identifier != 'c':
            raise ValueError(f"""Expected first char 'c'; got '{self.identifier}'""")
        if len(self) != 25:
            raise ValueError(f'Expected len() == 25; got {len(self)}')
        if not self.isascii():
            raise ValueError(f'Expected only ASCII chars')
        if not self.isalnum():
            raise ValueError(f'Expected only ASCII alpha numeric chars')
        return True

    @property
    def identifier(self) -> str:
        return self[0:1]  # 1

    @property
    def timestamp(self) -> int:
        return int(self[1:9], 36)  # 8

    @property
    def counter(self) -> int:
        return int(self[9:13], 36)  # 4

    @property
    def fingerprint(self) -> int:
        return int(self[13:17], 36)  # 4

    @property
    def random(self) -> int:
        return int(self[17:25], 36)  # 8


def is_valid(cuid: str) -> bool:
    identifier = cuid[0:1]
    if identifier != 'c':
        return False
    if len(cuid) != 25:
        return False
    if not cuid.isascii():
        return False
    if not cuid.isalnum():
        return False
    return True


def validate(cuid: str) -> bool:
    identifier = cuid[0:1]
    if identifier != 'c':
        raise ValueError(f"""Expected first char 'c'; got '{identifier}'""")
    if len(cuid) != 25:
        raise ValueError(f'Expected len() == 25; got {len(cuid)}')
    if not cuid.isascii():
        raise ValueError(f'Expected only ASCII chars')
    if not cuid.isalnum():
        raise ValueError(f'Expected only ASCII alpha numeric chars')
    return True
