from typing import (
    Any,
    Dict,
)


def convert_to_context_dict(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    context = {}

    for index, arg in enumerate(args):
        context[f"arg_{index + 1}"] = arg

    context.update(kwargs)

    return context
