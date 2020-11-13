from typing import List, Dict


def limit_intent(raw_data: List[Dict[str, str]], intent: str, max_qty: int) -> List[Dict[str, str]]:
    """
    Limit the number of examples of the specified intent-class in the dataset to the maximum quantity defined.

    Parameters
    -----------
    - **raw_data**: the dataset to be changed.
    - **intent**: the intent class to be limited
    - **max_qty**: the maximum numbers of example of that class allowed.

    Return
    ----------
    A new dataset but with the limited amount of examples for the specified intent class.
    """
    current = 0
    output = []
    for message in raw_data:
        if message["intent"] == intent:
            if current < max_qty:
                current += 1
                output.append(message)
        else:
            output.append(message)
    return output
