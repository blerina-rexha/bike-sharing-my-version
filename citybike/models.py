

from abc import ABC, abstractmethod
from datetime import datetime

# ---------------------------------------------------------------------------
# Abstract Base Class
# ---------------------------------------------------------------------------

class Entity(ABC):
    ## Base class for all entities in the system, providing common attributes and methods.    

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        """Return the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return the creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        ...


# ---------------------------------------------------------------------------
# Bike hierarchy
# ---------------------------------------------------------------------------

class Bike(Entity):
    # Base class for a bike in the system.

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(
        self,
        bike_id: str,
        bike_type: str,
        status: str = "available",
    ) -> None:
        super().__init__(id=bike_id)
        if bike_type not in ("classic", "electric"):
            raise ValueError(f"Invalid bike_type: {bike_type}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        return self._bike_type

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self) -> str:
        return f"Bike({self.id}, {self.bike_type}, {self.status})"

    def __repr__(self) -> str:
        return (
            f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, "
            f"status={self.status!r})"
        )


class ClassicBike(Bike):

    def __init__(
        self,
        bike_id: str,
        gear_count: int = 7,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)
        if gear_count <= 0:
            raise ValueError("gear_count must be positive")
        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike({self.id}, gears={self.gear_count})"

    def __repr__(self) -> str:
        return (
            f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, "
            f"status={self.status!r})"
        )


class ElectricBike(Bike):

    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="electric", status=status)

        if not (0 <= battery_level <= 100):
            raise ValueError("battery_level must be between 0 and 100")
        self._battery_level = battery_level

        if max_range_km <= 0:
            raise ValueError("max_range_km must be positive")
        self._max_range_km = max_range_km


    @property
    def battery_level(self) -> float:
        return self._battery_level
    
    @battery_level.setter
    def battery_level(self, value: float) -> None:
        if not (0 <= value <= 100):
            raise ValueError("battery_level must be between 0 and 100")
        self._battery_level = value

    @property
    def max_range_km(self) -> float:
        return self._max_range_km
    
    @max_range_km.setter
    def max_range_km(self, value: float) -> None:
        if value <= 0:
            raise ValueError("max_range_km must be positive")
        self._max_range_km = value

    def __str__(self) -> str:
       
        return f"ElectricBike(id={self.id}, battery_level={self.battery_level}, max_range_km={self.max_range_km})"

    def __repr__(self) -> str:
       
        return f"ElectricBike(bike_id={self.id!r}, battery_level={self.battery_level!r}, max_range_km={self.max_range_km!r}, status={self.status!r})"


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class Station(Entity):

    def __init__(
        self,
        station_id: str,
        name: str,
        capacity: int,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(id=station_id, created_at=None)
        self.name = name
        self.station_id = station_id

        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity

        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = latitude

        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = longitude

    @property
    def capacity(self) -> int:
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = value  

    @property
    def latitude(self) -> float:
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: float) -> None:
        if not (-90 <= value <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        if not (-180 <= value <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = value

    def __str__(self) -> str:
    
        return f"Station({self.id}, name={self.name}, capacity={self.capacity}, latitude={self.latitude}, longitude={self.longitude})"

    def __repr__(self) -> str:
        
        return f"Station(station_id={self.id!r}, name={self.name!r}, capacity={self.capacity!r}, latitude={self.latitude!r}, longitude={self.longitude!r})"


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User(Entity):

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        user_type: str,
    ) -> None:
        super().__init__(id=user_id)
       
        self.name = name
        self.user_type = user_type
        if "@" not in email:
            raise ValueError("Invalid email format")    
        self._email = email

        @property
        def email(self) -> str:
            return self._email
        
        @email.setter
        def email(self, value: str) -> None:
            if "@" not in value:
                raise ValueError("Invalid email format")
            self._email = value
        

    def __str__(self) -> str:
    
        return f"User({self.id}, name={self.name}, user_type={self.user_type})"

    def __repr__(self) -> str:
        
        return f"User(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, user_type={self.user_type!r})"


class CasualUser(User):

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        day_pass_count: int = 0,
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="casual")
        
        if day_pass_count < 0:
            raise ValueError("day_pass_count must be non-negative")
        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        return self._day_pass_count

    @day_pass_count.setter
    def day_pass_count(self, value: int) -> None:
        if value < 0:
            raise ValueError("day_pass_count must be non-negative")
        self._day_pass_count = value

    def __str__(self) -> str:
        
        return f"CasualUser({self.id}, name={self.name}, day_pass_count={self})"

    def __repr__(self) -> str:
        
        return f"CasualUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, day_pass_count={self.day_pass_count!r})"


class MemberUser(User):

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime = None,
        membership_end: datetime = None,
        tier: str = "basic",
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="member")
        
        if membership_start is None:
            membership_start = datetime.now()
        if membership_end is None:
            membership_end = membership_start

        if membership_end <= membership_start:
            raise ValueError("membership_end must be after membership_start")
        self._membership_start = membership_start
        self._membership_end = membership_end

        if tier not in ("basic", "premium"):
            raise ValueError("tier must be 'basic' or 'premium'")
        self._tier = tier

    @property
    def membership_start(self):
         return self._membership_start
        
    @property
    def membership_end(self): 
        return self._membership_end  
            
        
    @property
    def tier(self):
         return self._tier
        
    @tier.setter
    def tier(self, value: str) -> None:
        if value not in ("basic", "premium"):
            raise ValueError("tier must be 'basic' or 'premium'")
        self._tier = value

    def __str__(self) -> str:
        
        return f"MemberUser(id={self.id}, tier={self.tier}, membership_start={self.membership_start}, membership_end={self.membership_end})"

    def __repr__(self) -> str:
        
        return f"MemberUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, membership_start={self.membership_start!r}, membership_end={self.membership_end!r}, tier={self.tier!r}   )"


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class Trip:

    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:

        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station  
        self.end_station = end_station
        
        if end_time < start_time:
            raise ValueError("end_time must be after start_time")
        
        self.end_time = end_time
        self.start_time = start_time

        if distance_km < 0:
            raise ValueError("distance_km must be non-negative")
        self._distance_km = distance_km        

    @property
    def distance_km(self) -> float:
        return self._distance_km
    
    @property
    def duration_minutes(self) -> float:
        """Calculate trip duration in minutes from start and end times."""
    
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 60

    def __str__(self) -> str:
        
        return f"Trip({self.trip_id}, distance_km={self._distance_km}, duration_minutes={self.duration_minutes})"

    def __repr__(self) -> str:
        
        return f"Trip(trip_id={self.trip_id!r}, user={self.user!r}, bike={self.bike!r}, start_station={self.start_station!r}, end_station={self.end_station!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, distance_km={self._distance_km!r})"


# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class MaintenanceRecord:

    VALID_TYPES = {
        "tire_repair",
        "brake_adjustment",
        "battery_replacement",
        "chain_lubrication",
        "general_inspection",
    }

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:
        
        self.record_id = record_id
        self.bike = bike
        self.date = date

        if maintenance_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid maintenance_type: {maintenance_type}")   
        self.maintenance_type = maintenance_type

        if cost < 0:
            raise ValueError("cost must be non-negative")   
        self.cost = cost
        
        self.description = description

    @property
    def maintenance_type(self) -> str:  
        return self._maintenance_type
    
    @property
    def cost(self) -> float:
        return self._cost

    def __str__(self) -> str:
        
        return f"MaintenanceRecord(id={self.record_id}, bike_id={self.bike.id}, type={self.maintenance_type}, cost={self.cost}$)"

    def __repr__(self) -> str:
        
        return f"MaintenanceRecord(record_id={self.record_id!r}, bike={self.bike!r}, date={self.date!r}, maintenance_type={self.maintenance_type!r}, cost={self.cost!r}, description={self.description!r})"

if __name__ == "__main__":
    print("Models.py loaded successfully")
