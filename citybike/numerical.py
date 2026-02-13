
import numpy as np

# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def station_distance_matrix(
    latitudes: np.ndarray, longitudes: np.ndarray
) -> np.ndarray:
    #Compute pairwise distance matrix between stations using lat/lon.

    #compute pairwise latitude differences
    lat_diff = latitudes[:, np.newaxis] - latitudes[np.newaxis, :]

    # compute pairwise longitude differences
    lon_diff = longitudes[:, np.newaxis] - longitudes[np.newaxis, :]

    # combine with Euclidean formula
    distance_matrix = np.sqrt(lat_diff**2 + lon_diff**2)
    return distance_matrix


# ---------------------------------------------------------------------------
# Trip statistics
# ---------------------------------------------------------------------------

def trip_duration_stats(durations: np.ndarray) -> dict[str, float]:
    #Calculate summary statistics for trip durations.
    return {
        "mean": float(np.mean(durations)),
        "median": float(np.median(durations)),
        "std": float(np.std(durations)),
    
        "p25": float(np.percentile(durations, 25)),
        "p75": float(np.percentile(durations, 75)),
        "p90": float(np.percentile(durations, 90)),
    }

# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    #Detect outliers in *values* using Z-score method.
    mean = np.mean(values)
    std = np.std(values)
    if std == 0:
        return np.zeros_like(values, dtype=bool)  
    z = (values - mean) / std
    return np.abs(z) > threshold

# ---------------------------------------------------------------------------
# Vectorized fare calculation
# ---------------------------------------------------------------------------

def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    #Calculate fares for trips using vectorized NumPy operations.
    return unlock_fee + per_minute * durations + per_km * distances
