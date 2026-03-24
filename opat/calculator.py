from datetime import date, timedelta
 
CIVI = "Continuous infusor (CIVI)"
IVB  = "IV bolus"
PO   = "Oral therapy (PO)"
 
METHODS = [CIVI, IVB, PO]
 
 
def calculate_last_dose(start_date: date, days_of_therapy: int) -> date:
    """Last dose = start date + DOT - 1 day."""
    return start_date + timedelta(days=days_of_therapy - 1)
 
 
def calculate_line_removal(last_dose: date, method: str) -> date | None:
    """Line removal day: last dose + 1 (CIVI), last dose (IVB), N/A (PO)."""
    if method == CIVI:
        return last_dose + timedelta(days=1)
    if method == IVB:
        return last_dose
    return None
