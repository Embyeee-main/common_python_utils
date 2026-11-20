from typing import Any, Optional, Union


def is_builtin(obj):
    return type(obj).__module__ == "builtins"


def get_obj_dict(parent: Any) -> dict[str, Any]:
    buf = {}

    for key, val in parent.__dict__.items():
        if not is_builtin(val):
            buf[key] = get_obj_dict(val)
        else:
            buf[key] = val
    return buf


def _dict_test_func(parent: dict[str, Any], key: str) -> Optional[Any]:
    return parent.get(key)


def _obj_test_func(parent: Any, key: str) -> Optional[Any]:
    return parent.__getattribute__(key) if key in parent.__dict__ else None


def option_chain(parent: Union[Any, dict[str, Any]], *keys: str) -> None:
    if not is_builtin(parent):
        test_func = _obj_test_func
    elif isinstance(parent, dict):
        test_func = _dict_test_func

    cur = parent
    for key in keys:
        cur = test_func(cur, key)
        if cur is None:
            return None
    return cur
