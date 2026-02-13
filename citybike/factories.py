
from datetime import datetime
from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
)

def create_bike(data: dict) -> Bike:
    #Create a Bike (ClassicBike or ElectricBike) from a data dictionary.
    bike_type = data.get("bike_type", "").lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )
    else:
        raise ValueError(f"Unknown bike_type: {bike_type!r}")


def create_user(data: dict) -> User:
    #Create a User (CasualUser or MemberUser) from a data dictionary.   
    user_type = data.get("user_type", "casual").lower()

    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            day_pass_count=int(data.get("day_pass_count", 0)),  
        )
    elif user_type == "member":
        membership_start = data.get("membership_start")
        membership_end = data.get("membership_end")

        if membership_start:
            membership_start = datetime.fromisoformat(membership_start)
        if membership_end:
            membership_end = datetime.fromisoformat(membership_end)

        tier=data.get("tier", "basic").lower()
        return MemberUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],    
            membership_start=membership_start,
            membership_end=membership_end,
            tier=tier,
        )

    else:
        raise ValueError(f"Unknown user_type: {user_type}")
