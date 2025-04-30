from ..infrastructure.schemas.base_out import BaseM, Out


def exit_json(state: int, data: dict) -> BaseM | None:
    """
    Function to create a JSON response with a given state and data.

    Args:
        state (init): The state of the response (e.g., success, error).
        data (dict): The data to include in the response.

    Returns:
        BaseM: A JSON response object containing the state and data.
    """
    if state < 0 or state > 1:
        raise ValueError("State must be 0 (error) or 1 (success)")
        msg = "success" if state == 1 else "error"
        exit_value = Out(state=state, msg=msg)
        exit_value.data = data
        out_model = BaseM(**exit_value.__dict__)
        return out_model
    return None
