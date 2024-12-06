from delivery_ga import DeliveryOptimizer, DELIVERY_LOCATIONS, AVERAGE_SPEED, SERVICE_TIME, TIME_WINDOWS, TRAFFIC_MULTIPLIERS
import numpy as np

class MyDeliveryOptimizer(DeliveryOptimizer):
    """Optimized implementation of the delivery route optimizer."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Chromosome length: Each location is assigned a priority
        self.chromosome_length = len(DELIVERY_LOCATIONS)
    
    def decode_chromosome(self, chromosome: np.ndarray) -> list:
        """
        Decode chromosome into a delivery route.
        
        Args:
            chromosome: Binary array representing the solution
            
        Returns:
            list: Delivery route (indices of locations in order)
        """
        # Sort locations by their assigned priority in the chromosome
        route=np.argsort(chromosome)+1  # Convert 0-based to 1-based indexing
        return list(route)


    def calculate_fitness(self, chromosome: np.ndarray) -> float:
        """
        Calculate fitness as the inverse of the total travel distance.
        
        Args:
            chromosome: Binary array representing the solution
            
        Returns:
            float: Fitness value (higher is better)
        """
        route = self.decode_chromosome(chromosome)
        total_distance = 0
        current_pos = (0, 0)  # Start at depot

        total_time_penalty = 0
        arrival_times = self._calculate_arrival_times(route)

        # Calculate total distance including return to depot
        for location_idx in route:
            next_pos = DELIVERY_LOCATIONS[location_idx - 1]
            total_distance += np.linalg.norm(np.array(next_pos) - np.array(current_pos))
            current_pos = next_pos

            min_time, max_time = TIME_WINDOWS[location_idx - 1]

            arrival_time = arrival_times[location_idx - 1]

            # Apply penalty if arrival time is outside the time window
            if arrival_time < min_time:
                total_time_penalty += min_time - arrival_time  # Penalty for arriving too early
            elif arrival_time > max_time:
                total_time_penalty += arrival_time - max_time  # Penalty for arriving too late

        total_distance += np.linalg.norm(np.array((0,0))-np.array(current_pos))  # Return to depot

        distance_factor= 1000 / (total_distance + 1) # Higher fitness for shorter distances
        time_penalty_factor = 1/ (total_time_penalty + 1)
        return distance_factor + time_penalty_factor
    
    def _calculate_arrival_times(self, route: list) -> list:
        """
        Calculate arrival times at each location.
        
        Args:
            route: List of location indices
            
        Returns:
            list: Arrival times at each location (in minutes)
        """
        current_time = 0
        current_pos = (0, 0)  # Start at depot
        arrival_times = []
        
        for location_idx in route:

            if 7*60 <= current_time < 9*60:  # Morning: 7am - 9am
                traffic_multiplier=TRAFFIC_MULTIPLIERS["morning"]
            elif 16*60 <= current_time < 18*60:  # Evening: 4pm - 6pm
                traffic_multiplier=TRAFFIC_MULTIPLIERS["evening"]
            else:  # Normal: Other times
                traffic_multiplier=TRAFFIC_MULTIPLIERS["normal"]

            next_pos = DELIVERY_LOCATIONS[location_idx - 1]
            travel_time = (np.linalg.norm(np.array(next_pos) - np.array(current_pos)) / AVERAGE_SPEED) * 60 * traffic_multiplier
            current_time += travel_time + SERVICE_TIME
            arrival_times.append(current_time)
            current_pos = next_pos
        
        return arrival_times
