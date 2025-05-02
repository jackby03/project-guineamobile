from typing import Any

from src.shared.domain.base_out import BaseM, Out


def exit_json(state: int, data: dict) -> dict[str, Any]:
    """
    Creates a standardized JSON response with state and data information.

    This function generates a consistent JSON response structure for success or error states.
    """
    if state < 0 or state > 1:
        raise ValueError("Output only accepts 0 or 1 as state values.")
    msg = "success" if state == 1 else "error"
    output = Out(state=state, msg=msg)
    output.data = data
    salida_model = BaseM(**output.__dict__)
    return salida_model.dict()
