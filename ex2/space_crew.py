"""Demonstrat Complex Pydantic."""
from enum import Enum
from pydantic import (BaseModel, Field, model_validator,
                      field_validator, ValidationError)
from datetime import datetime
from typing import Any


class Rank(Enum):
    """Class Rank."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Class Crew Member."""

    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """Class Space Mission."""

    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @field_validator('crew', mode='before')
    @classmethod
    def ft_crew(cls, list_crew) -> list[CrewMember]:
        """Create self crew."""
        crew: list[CrewMember] = []
        for crew_data in list_crew:
            crew_object = CrewMember(**crew_data)
            crew.append(crew_object)
        return crew

    @model_validator(mode='after')
    def Validation_rules(self) -> Any:
        """Check rules."""
        if not self.mission_id.startswith("M"):
            raise ValueError(
                "Mission ID must have a 'M' on the beginning")
        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
            if member.rank == Rank.CAPTAIN or member.rank == Rank.COMMANDER:
                return self
            else:
                raise ValueError(
                    "Mission must have at least one Commander or Captain")
        if self.duration_days > 365:
            cadet_number: int = sum(1 for member in self.crew if
                                    member.rank == Rank.CADET)
            if cadet_number > (len(self.crew) / 2):
                raise ValueError(
                    "Mission must have greather than half exprement memeber")
        return self


def main(data) -> None:
    """Demonstrat Complex Pydantic."""
    print("=========================================")

    try:
        mission = SpaceMission(**data)
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crez size: {len(mission.crew)}")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value})"
                  f" - {member.specialization}")
        print()
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(str(error["msg"]).split(", ")[1])


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    mission_1: dict = {
                     "mission_id": "M2024_TITAN",
                     "mission_name": "Solar Observatory Research Mission",
                     "destination": "Solar Observatory",
                     "launch_date": "2024-03-30T00:00:00",
                     "duration_days": 451,
                     "crew": [
                       {
                         "member_id": "CM001",
                         "name": "Sarah Williams",
                         "rank": "captain",
                         "age": 43,
                         "specialization": "Mission Command",
                         "years_experience": 19,
                         "is_active": True
                       },
                       {
                         "member_id": "CM002",
                         "name": "James Hernandez",
                         "rank": "captain",
                         "age": 43,
                         "specialization": "Pilot",
                         "years_experience": 30,
                         "is_active": True
                       },
                       {
                         "member_id": "CM003",
                         "name": "Anna Jones",
                         "rank": "cadet",
                         "age": 35,
                         "specialization": "Communications",
                         "years_experience": 15,
                         "is_active": True
                       },
                       {
                         "member_id": "CM004",
                         "name": "David Smith",
                         "rank": "commander",
                         "age": 27,
                         "specialization": "Security",
                         "years_experience": 15,
                         "is_active": True
                       },
                       {
                         "member_id": "CM005",
                         "name": "Maria Jones",
                         "rank": "cadet",
                         "age": 55,
                         "specialization": "Research",
                         "years_experience": 30,
                         "is_active": True
                       }
                     ],
                     "mission_status": "planned",
                     "budget_millions": 2208.1}
    mission_2: dict = {
                     "mission_id": "M2024_TITAN",
                     "mission_name": "Solar Observatory Research Mission",
                     "destination": "Solar Observatory",
                     "launch_date": "2024-03-30T00:00:00",
                     "duration_days": 451,
                     "crew": [
                       {
                         "member_id": "CM001",
                         "name": "Sarah Williams",
                         "rank": "cadet",
                         "age": 43,
                         "specialization": "Mission Command",
                         "years_experience": 19,
                         "is_active": True
                       },
                       {
                         "member_id": "CM002",
                         "name": "James Hernandez",
                         "rank": "cadet",
                         "age": 43,
                         "specialization": "Pilot",
                         "years_experience": 30,
                         "is_active": True
                       },
                       {
                         "member_id": "CM003",
                         "name": "Anna Jones",
                         "rank": "cadet",
                         "age": 35,
                         "specialization": "Communications",
                         "years_experience": 15,
                         "is_active": True
                       },
                     ],
                     "mission_status": "planned",
                     "budget_millions": 2208.1}
    main(mission_1)
    main(mission_2)
