"""
Custom Exceptions for Graph Project

این فایل خطاهای سفارشی پروژه گراف/شبکه اجتماعی رو تعریف می‌کنه.
هر خطا برای یه وضعیت خاص طراحی شده.
"""


class DuplicateUser(Exception):
    """
    وقتی کاربر تکراری اضافه بشه پرتاب میشه.

    Example:
        >>> raise DuplicateUser("User 1 already exists")
    """
    pass


class UserNotFound(Exception):
    """
    وقتی کاربری وجود نداشته باشه ولی بخوایم ازش استفاده کنیم.

    Example:
        >>> raise UserNotFound("User 999 does not exist")
    """
    pass


class DuplicateEdge(Exception):
    """
    وقتی رابطه/دوستی تکراری بسازیم.

    Example:
        >>> raise DuplicateEdge("Friendship between 1 and 2 already exists")
    """
    pass


class InvalidEdge(Exception):
    """
    وقتی رابطه نامعتبر باشه (مثلاً کسی با خودش دوست بشه).

    Example:
        >>> raise InvalidEdge("A user cannot connect to itself!")
    """
    pass