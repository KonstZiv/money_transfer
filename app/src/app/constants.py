from enum import IntEnum, unique


@unique
class Role(IntEnum):
    """
    describes possible roles in the system (as castomer/operator/administrator)
    """

    ADMIN = 1
    OPERATOR = 2
    CUSTOMER = 3
