from ..infrastructure.schemas.base_out import BaseM, Out


def exit_json(state: int, data: dict) -> BaseM:
    if state < 0 or state > 1:
        raise ValueError("Output only set 1 o 0")
    msg = "success" if state == 1 else "error"
    output = Out(state=state, msg=msg)
    output.data = data
    salida_model = BaseM(**output.__dict__)
    return salida_model.dict()
