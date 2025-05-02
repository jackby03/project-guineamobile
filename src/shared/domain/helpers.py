from typing import Any

from src.shared.domain.base_out import BaseM, Out


def exit_json(state: int, data: dict) -> dict[str, Any]:
    """
    Creates a standardized JSON response with state and data information.
    Args:
        state (int): Status indicator - must be 0 or 1 (0=error, 1=success)
        data (dict): Data payload to include in response
    Returns:
        dict[str, Any]: Dictionary containing:
            - state: Original state value
            - msg: "success" if state=1, "error" if state=0
            - data: Original data payload
    Raises:
        ValueError: If state is not 0 or 1
    Examples:
        >>> exit_json(1, {"user": "john"})
        {'state': 1, 'msg': 'success', 'data': {'user': 'john'}}
        >>> exit_json(0, {"error": "not found"})
        {'state': 0, 'msg': 'error', 'data': {'error': 'not found'}}
    """

    if state < 0 or state > 1:
        raise ValueError("Output only set 1 o 0")
    msg = "success" if state == 1 else "error"
    output = Out(state=state, msg=msg)
    output.data = data
    salida_model = BaseM(**output.__dict__)
    return salida_model.dict()
