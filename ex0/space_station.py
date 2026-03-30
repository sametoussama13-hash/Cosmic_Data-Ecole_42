"""Test Pydantic validator."""
from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    """Class Space Station."""

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0, le=100)
    oxygen_level: float = Field(..., ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=True, max_length=200)


def main(data) -> None:
    """Test Pydantic validator."""
    print("========================================")
    try:
        station = SpaceStation(**data)
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size}")
        print(f"Power: {station.power_level}")
        print(f"Oxygen: {station.oxygen_level}")
        status: str = ("Operational" if station.is_operational
                       else "Not Operational")
        print(f"Status: {status}")
        print()
    except ValueError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    print("Space Station Data Validation")
    space_station_1: dict = {"station_id": "ISS001",
                             "name": "International Space Station",
                             "crew_size": 6, "power_level": 85.5,
                             "oxygen_level": 92.3,
                             "last_maintenance": "2024-01-15T10:30:00",
                             "is_operational": True
                             }
    space_station_2: dict = {"station_id": "ISS001",
                             "name": "International Space Station",
                             "crew_size": 25, "power_level": 85.5,
                             "oxygen_level": 92.3,
                             "last_maintenance": "2024-01-15T10:30:00",
                             "is_operational": True
                             }
    main(space_station_1)
    main(space_station_2)
