
import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    #Central analysis class — loads, cleans, and analyzes bike-share data.

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        #Clean all DataFrames and export to CSV.

        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # --- Remove duplicates ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        print(f"After dedup: {self.trips.shape[0]} trips")
        self.stations = self.stations.drop_duplicates(subset=["station_id"])
        print(f"After dedup: {self.stations.shape[0]} stations")
        self.maintenance = self.maintenance.drop_duplicates(subset=["record_id"])
        print(f"After dedup: {self.maintenance.shape[0]} maintenance records")

        # ---  Parse dates, convert start_time, end_time to datetime ---
       
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])

        # --- Convert numeric columns, ensure they are float ---
        
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors="coerce")
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors="coerce")
                
        # --- Handle missing values ---
        
        self.trips = self.trips.dropna(subset=["start_time", "end_time", "duration_minutes", "distance_km"])
        print(f"After dropping missing values: {self.trips.shape[0]} trips")

        # --- Remove invalid entries, drop rows where end_time < start_time ---

        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]
        if "distance_km" in self.trips.columns:
            self.trips = self.trips[self.trips["distance_km"] >= 0]
        print(f"After removing invalid entries: {self.trips.shape[0]} trips")

        # --- Step 6: Standardize categoricals ---
        # TODO: e.g. self.trips["status"].str.lower().str.strip()

        self.trips["user_type"] = (self.trips["user_type"]).str.lower().str.strip()
        self.trips["bike_type"] = (self.trips["bike_type"]).str.lower().str.strip()
        self.trips["status"] = (self.trips["status"]).str.lower().str.strip()
        print("Standardized categorical columns in trips dataset.")

        # --- Export cleaned datasets ---

        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        #Total trips, total distance, average duration.

        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        #Top *n* most popular start stations.

        counts = self.trips["start_station_id"].value_counts().head(n)
        top_starts = counts.reset_index()
        top_starts.columns = ["station_id", "trip_count"]
        top_starts = top_starts.merge(self.stations[["station_id", "station_name"]], on="station_id", how="left")
        return top_starts.sort_values(by="trip_count", ascending=False)  

    def peak_usage_hours(self) -> pd.Series:
        #Trip count by hour of day.

        hours = self.trips["start_time"].dt.hour
        counts = hours.value_counts().sort_index()
        return counts

    def busiest_day_of_week(self) -> pd.Series:
        #Trip count by day of week.

        days = self.trips["start_time"].dt.day_name()
        counts = days.value_counts()
        return counts

    def avg_distance_by_user_type(self) -> pd.Series:
        """ Average trip distance grouped by user type."""
        avg_dist = self.trips.groupby("user_type")["distance_km"].mean().round(2)
        return avg_dist

    def monthly_trip_trend(self) -> pd.Series:
        #Monthly trip counts over time.

        year_month = self.trips["start_time"].dt.to_period("M")
        monthly_counts = year_month.value_counts().sort_index()
        return monthly_counts


    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        #Top *n* most active users by trip count.

        count=self.trips.groupby("user_id").size().sort_values(ascending=False)
        top_n_df=count.head(n).reset_index(name="trip_count")
        return top_n_df

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        #Total maintenance cost per bike type.

        if self.maintenance is None:
            raise RuntimeError("Maintenance data not loaded")
        total_cost = self.maintenance.groupby("bike_type")["cost"].sum().round(2)
        return total_cost

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        #Most common start→end station pairs.

        route_counts = self.trips.groupby(["start_station_id", "end_station_id"]).size()
        top_routes = route_counts.sort_values(ascending=False).head(n).reset_index(name="trip_count")
        return top_routes

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        #Write a summary text report to output/summary_report.txt.

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        # --- Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")

        # --- Top start stations ---
    
        top_stations = self.top_start_stations()
        lines.append("\n--- Top 10 Start Stations ---")
        lines.append(top_stations.to_string(index=False))

        # --- Peak usage hours ---
        
        hours = self.peak_usage_hours()
        lines.append("\n--- Peak Usage Hours ---")
        lines.append(hours.to_string(index=False))

        # --- Maintenance cost by bike type ---
        
        maint_cost = self.maintenance_cost_by_bike_type()
        lines.append("\n--- Maintenance Cost by Bike Type ---")
        lines.append(maint_cost.to_string())


        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        print(f"Report saved to {report_path}")
