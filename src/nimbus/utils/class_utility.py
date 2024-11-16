from typing import Union

class ClassUtility():
    @staticmethod
    def to_dict(obj) -> Union[dict, list]:
        if not hasattr(obj, "__dict__"):
            return obj
        result = {}
        for key, value in obj.__dict__.items():
            if isinstance(value, list):
                result[key] = [ClassUtility.to_dict(item) for item in value]
            elif isinstance(value, dict):
                result[key] = {k: ClassUtility.to_dict(v) for k, v in value.items()}
            else:
                result[key] = ClassUtility.to_dict(value)
        return result