from dataclasses import dataclass, is_dataclass, fields, asdict
from enum import Enum
from typing import Sequence


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class ExtraDataclass:
    @classmethod
    def from_dict(cls, data: dict):
        """ Create dataclass from dict ignoring extra arguments. """
        cl_fields = set([f.name for f in fields(cls)])
        filtered_data = dict()
        for k, v in data.items():
            if k in cl_fields:
                filtered_data[k] = v
        return cls(**filtered_data)

    @classmethod
    def from_list(cls, ent_list: Sequence[dict]) -> list:
        """ Create list of dataclass instances from list of dicts. """
        return [cls.from_dict(ent) for ent in ent_list]

    def to_dict(self) -> dict:
        """ Returns dict with not None values """
        return asdict(
            self, dict_factory=lambda d: {k: v for k, v in d if v is not None}
        )


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class ConstEnum(str, Enum):
    """
    Class is used for gathering string constants in one place.
    Attribute values are generated from attribute names.
    All attributes values will be considered as strings.
    Class name is omitted from attribute value.

    >>> Booze = ConstEnum("Booze", "Whiskey Beer Vodka")
    >>> Booze.Beer
    Beer
    >>> print(Booze.Beer)
    Beer
    >>> type(Booze.Vodka)
    <enum 'Booze'>
    >>> repr(Booze.Whiskey)
    'Whiskey'

    Also could be used with usual class creation:
    >>> from enum import auto
    >>> class NotBooze(ConstEnum):
    >>>     Juice = auto()
    >>>     Tea = auto()
    >>>     Coffee = auto()

    >>> repr(NotBooze.Tea)
    'Tea'
    """

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
