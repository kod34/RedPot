from enum import Enum

class Action(Enum):
    """An action to be done by the NIDS in case of detected packet."""

    ALERT = 1

def action(istr):
    """Return Action corresponding to the string."""
    str = istr.lower().strip()
    if (str == "alert"):
        return Action.ALERT

