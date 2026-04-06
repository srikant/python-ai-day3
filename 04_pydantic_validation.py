from pydantic import BaseModel, Field

# Simple Pydantic model
class Alert(BaseModel):
    name: str
    severity: int
    
# Pydantic model with field constraints
class AlertCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    severity: int = Field(..., ge=1, le=5)
    message: str | None = None
    
if __name__ == "__main__":
    alert = AlertCreate(name="Disk full", severity=3)
    print(f"Valid: {alert}")

    try:
        invalid_alert = AlertCreate(name="", severity=6)
    except Exception as e:
        print(f"Invalid: {e}")