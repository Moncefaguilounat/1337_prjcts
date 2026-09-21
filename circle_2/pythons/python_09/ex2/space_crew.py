from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        senior_ranks = {Rank.commander, Rank.captain}
        has_senior = any(member.rank in senior_ranks for member in self.crew)
        if not has_senior:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        inactive = [m.name for m in self.crew if not m.is_active]
        if inactive:
            raise ValueError(
                f"All crew members must be active. Inactive: {inactive}")

        if self.duration_days > 365:
            experienced = sum(1 for m in self.crew if m.years_experience >= 5)
            ratio = experienced / len(self.crew)
            if ratio < 0.5:
                raise ValueError(
                    "Long missions need at least 50% experienced crew "
                    "(5+ years)"
                )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-06-01T09:00:00",
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=45,
                specialization="Mission Command",
                years_experience=20
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=34,
                specialization="Navigation",
                years_experience=8
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=6
            ),
        ]
    )

    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")
    print("Crew members:")
    for member in valid_mission.crew:
        print(f"  - {member.name} ({member.rank.value}) - ", end="")
        print(f"{member.specialization}")

    print()
    print("=" * 41)

    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Base Alpha",
            destination="Moon",
            launch_date="2024-07-01T09:00:00",
            duration_days=180,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="CM010",
                    name="Bob Martin",
                    rank=Rank.officer,
                    age=28,
                    specialization="Engineering",
                    years_experience=3
                ),
                CrewMember(
                    member_id="CM011",
                    name="Lisa Ray",
                    rank=Rank.cadet,
                    age=22,
                    specialization="Science",
                    years_experience=0
                ),
            ]
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            msg = error["msg"]
            if msg.startswith("Value error, "):
                msg = msg.replace("Value error, ", "")
            print(msg)


if __name__ == "__main__":
    main()
