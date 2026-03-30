from enum import Enum
from pydantic import BaseModel, model_validator, Field
from datetime import datetime


class ContactType(Enum):
    """Enum Contact Type"""

    RADIO = "radio"
    VISUEL = "visuel"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Class Alien Contact."""

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float | None = Field(default=None, ge=0, le=10)
    duration_minutes: int | None = Field(default=None, ge=1, le=1440)
    witness_count: int | None = Field(default=None, ge=1, le=1000)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool | None = False

    @model_validator(mode='after')
    def ft_validation(self) -> ContactType:
        """valid Type contact."""
        if not self.contact_id.startswith("AC"):
            raise ValueError("Alien contact misses AC at the beginning")
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
           ):
            raise ValueError(
                f"Alien {self.contact_type} contact is not verified")
        elif self.contact_type == ContactType.RADIO.value:
            if self.signal_strength <= 7:
                raise ValueError(
                    f"Alien signal {self.contact_type} is not strength")
            elif self.signal_strength > 7 and not self.message_received:
                raise ValueError(
                    f"Alien signal {self.contact_type} is strength"
                    " but he don't have a message")
        elif (
              self.contact_type == ContactType.TELEPATHIC
              and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        elif (self.contact_type == ContactType.TELEPATHIC and
              self.duration_minutes < 3):
            raise ValueError(
                f"Alien visuel time {self.duration_minutes} is not enough")
        return self


def main(data) -> None:
    """Check Alien Contact."""
    print("======================================")
    try:
        alien = AlienContact(**data)
        print("Valid contact report:")
        print(f"ID: {alien.contact_id}")
        print(f"Type: {alien.contact_type}")
        print(f"Location: {alien.location}")
        print(f"Signal: {alien.signal_strength}/10")
        print(f"Duration: {alien.duration_minutes} minutes")
        print(f"Witnesses: {alien.witness_count}")
        if alien.message_received:
            print(f"Message: '{alien.message_received}'")
        print()
    except ValueError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    alien: dict = {"radio": {"contact_id": "AC_2024_001",
                             "timestamp": "2024-01-15T10:30:00",
                             "location": "Area 51, Nevada",
                             "contact_type": ContactType.RADIO.value,
                             "signal_strength": 8.5,
                             "duration_minutes": 45,
                             "witness_count": 5,
                             "message_received": "’Greetings from Zeta Reticuli",
                             "is_verified": False},
                   "physical": {"contact_id": "AC_2024_001",
                                "timestamp": "2024-01-15T10:30:00",
                                "location": "Area 51, Nevada",
                                "contact_type": ContactType.PHYSICAL.value,
                                "signal_strength": None,
                                "duration_minutes": 45,
                                "witness_count": 5,
                                "message_received": "’Greetings from Zeta Reticuli",
                                "is_verified": True},
                   "telepathic": {"contact_id": "AC_2024_001",
                                  "timestamp": "2024-01-15T10:30:00",
                                  "location": "Area 51, Nevada",
                                  "contact_type": ContactType.TELEPATHIC.value,
                                  "signal_strength": 8.5,
                                  "duration_minutes": 45,
                                  "witness_count": 2,
                                  "message_received": "",
                                  "is_verified": False}}
    for type, data in alien.items():
        main(type, data)
