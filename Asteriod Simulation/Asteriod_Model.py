import math
import numpy as np
import matplotlib.pyplot as plt

def crater_diameter(impactor_diameter, velocity, density, angle_deg, target_density=2500):
    """Estimates crater diameter using Holsapple's scaling laws with angle effect."""
    g = 9.81  # Gravity (m/s^2)
    scaling_factor = 1.3
    angle_rad = math.radians(angle_deg)
    angle_factor = math.cos(angle_rad) ** 0.3  # shallower = smaller crater
    return scaling_factor * (impactor_diameter ** 0.78) * ((velocity ** 0.44) / (g ** 0.22)) * ((density / target_density) ** 0.3) * angle_factor

def ejecta_mass(impactor_diameter, velocity, density, angle_deg):
    """Estimates mass of ejected material based on impact energy and angle."""
    volume = (4/3) * math.pi * (impactor_diameter / 2) ** 3
    impact_energy = 0.5 * density * volume * velocity ** 2
    angle_rad = math.radians(angle_deg)
    ejecta_factor = 0.2 * math.cos(angle_rad)  # Less ejecta for shallow impacts
    return ejecta_factor * impact_energy


def temperature_drop(ejecta_mass):
    """Estimates temperature drop due to dust blocking sunlight."""
    cooling_factor = 1e-14
    return cooling_factor * ejecta_mass

def simulate_cooling(temp_drop, years=50):
    """Simulates global temperature recovery over time."""
    recovery_rate = 0.1  # Rate of temperature recovery per year
    time = np.arange(0, years, 1)
    temps = temp_drop * np.exp(-recovery_rate * time)
    return time, temps

def main():
    try:
        impactor_diameter = float(input("Enter asteroid diameter (m): "))
        velocity = float(input("Enter impact velocity (m/s): "))
        density = float(input("Enter asteroid density (kg/m^3): "))
        angle_deg = float(input("Enter impact angle (degrees from horizontal, e.g. 90 = vertical): "))

        
        if impactor_diameter <= 0 or velocity <= 0 or density <= 0:
            raise ValueError("All values must be positive numbers.")
        
        crater_size = crater_diameter(impactor_diameter, velocity, density, angle_deg)
        ejecta = ejecta_mass(impactor_diameter, velocity, density, angle_deg)
        temp_change = temperature_drop(ejecta)
        time, temps = simulate_cooling(temp_change)
        
        
        print(f"\nImpact Simulation Results:")
        print(f"Crater Diameter: {crater_size:.2f} m")
        print(f"Ejecta Mass: {ejecta:.2e} kg")
        print(f"Initial Global Temperature Drop: {temp_change:.2f}°C")
        
        plt.figure(figsize=(8, 5))
        plt.plot(time, temps, label="Temperature Drop Recovery", color='b')
        plt.xlabel("Years After Impact")
        plt.ylabel("Temperature Drop (°C)")
        plt.title("Global Cooling Recovery After Impact")
        plt.legend()
        plt.grid()
        plt.show()
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
