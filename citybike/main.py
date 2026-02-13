
import pandas as pd
from analyzer import BikeShareSystem
from visualization import plot_duration_by_user_type, plot_monthly_trend, plot_trips_per_station, plot_duration_histogram

def main() -> None:
    """Run the complete CityBike analytics pipeline."""

    system = BikeShareSystem()

    # Load data
    print("\n>>> Loading data …")
    system.trips = pd.read_csv("data/trips.csv")
    system.stations = pd.read_csv("data/stations.csv")
    system.maintenance = pd.read_csv("data/maintenance.csv")

    # Inspect
    print("\n>>> Inspecting data …")
    system.inspect_data()

    # Clean
    print("\n>>> Cleaning data …")
    system.clean_data()

    system.generate_summary_report()

    # Analytics
    print("\n>>> Running analytics …")
    summary = system.total_trips_summary()
    print(f"  Total trips      : {summary['total_trips']}")
    print(f"  Total distance   : {summary['total_distance_km']} km")
    print(f"  Avg duration     : {summary['avg_duration_min']} min")

    # TODO: implement pricing once pricing.py is ready

    #Visualizations
    print("\n>>> Generating visualizations …")
    plot_trips_per_station(system.trips, system.stations)
    # TODO: call remaining plot functions
    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # Step 6 — Report
    # TODO: system.generate_summary_report()

    print("\n>>> Done! Check output/ for results.")


if __name__ == "__main__":
    main()
