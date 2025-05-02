from typing import Any

from src.shared.domain.base_out import BaseM, Out


def exit_json(state: int, data: dict) -> dict[str, Any]:
    """
    Creates a standardized JSON response with state and data information.

    This function generates a consistent JSON response structure for success or error states.

    Args:
        state (int): Status indicator - must be 0 or 1 (0=error, 1=success).
        data (dict): Data payload to include in the response.

    Returns:
        dict[str, Any]: A dictionary containing:
            - state (int): The original state value.
            - msg (str): "success" if `state` is 1, "error" if `state` is 0.
            - data (dict): The original data payload.

    Raises:
        ValueError: If `state` is not 0 or 1.

    Examples:
        >>> exit_json(1, {"user": "john"})
        {'state': 1, 'msg': 'success', 'data': {'user': 'john'}}
        >>> exit_json(0, {"error": "not found"})
        {'state': 0, 'msg': 'error', 'data': {'error': 'not found'}}
    """
    if state < 0 or state > 1:
        raise ValueError("Output only accepts 0 or 1 as state values.")
    msg = "success" if state == 1 else "error"
    output = Out(state=state, msg=msg)
    output.data = data
    salida_model = BaseM(**output.__dict__)
    return salida_model.dict()
