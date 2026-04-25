from typing import Tuple, Optional, List


def convert_time_value(time_ma: float, uncertainty_ma: Optional[float] = None) -> Tuple[float, Optional[float], str]:
    if time_ma >= 1000:
        return time_ma/1000, uncertainty_ma/1000 if uncertainty_ma is not None else None, "Ga"
    elif time_ma >= 1:
        return time_ma, uncertainty_ma if uncertainty_ma is not None else None, "Ma"
    return time_ma*1000, uncertainty_ma*1000 if uncertainty_ma is not None else None, "ka"


def format_description_representation(time_ma: float, uncertainty_ma: float) -> str:
    time_converted, uncertainty_converted, time_unit = convert_time_value(time_ma, uncertainty_ma)

    if time_converted == 0.0:
        return "present"

    description_parts = [f"{time_converted:.3f}".rstrip("0").rstrip(".")]

    if uncertainty_converted not in (None, 0.0):
        description_parts.append(f"± {str(uncertainty_converted).rstrip('0').rstrip('.')}")

    description_parts.append(time_unit)

    return " ".join(description_parts)


def format_duration_representation(duration_ma: float) -> str:
    duration_converted, _, time_unit = convert_time_value(duration_ma)
    return f"{duration_converted:.3f} {time_unit}"
