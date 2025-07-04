from functools import wraps
from importlib import import_module
from inspect import iscoroutinefunction, signature
from typing import Any, Callable, Self

_refs = {}
_group_name = 'default'


class _Builder:

    def __init__(self, name: str):
        self.name = name
        self._refs = _refs

    def add_ref(self, ref: Callable[..., Any] | type) -> Self:
        self.add_named_ref(ref.__name__, ref)

        return self

    def add_named_ref(self, name: str, ref: Any) -> Self:
        if self.name not in self._refs:
            self._refs[self.name] = {}

        self._refs[self.name][name] = ref

        return self

    def lazy_add_ref(self, ref_name: str) -> Self:
        self.add_named_ref(ref_name, import_module(ref_name))

        return self


def builder(name: str = 'default') -> _Builder:
    return _Builder(name)


def using(name: str) -> Any:
    group_name = _group_name
    return _refs[group_name][name]


def group(group_name: str, func: Callable[..., Any]) -> Callable[..., Any]:
    if iscoroutinefunction(func):

        @wraps(func)
        async def async_inner(*args: list[Any], **kwargs: dict[str, Any]):
            global _group_name

            original_group_name = _group_name
            _group_name = group_name
            value = await func(*args, **kwargs)
            _group_name = original_group_name
            return value

        async_inner.__signature__ = signature(func)
        return async_inner

    @wraps(func)
    def inner(*args: list[Any], **kwargs: dict[str, Any]):
        global _group_name

        original_group_name = _group_name
        _group_name = group_name
        value = func(*args, **kwargs)
        _group_name = original_group_name
        return value

    inner.__signature__ = signature(func)
    return inner
