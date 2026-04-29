from .schemas import SurgeCalculation, WeatherData, SurgeRequest, SurgeResponse

def calculate_surge_multiplier(surge_request: SurgeRequest, weather_data: WeatherData)-> SurgeCalculation:
    multiplier = 1.0
    reason = []
    if surge_request.rider_count == 0:
        multiplier += 0.8
        reason.append("No riders available")
    else:
        ratio = surge_request.active_orders / (surge_request.rider_count)
        if ratio > 1.5:
            multiplier += 0.5
            reason.append("High demand: active orders exceed available riders.")
        elif ratio > 1.0:
            multiplier += 0.2
            reason.append("Moderate demand: active orders are more than half of available riders.")
    
    if weather_data.condition in ["Rain", "Snow","Thunderstorm", "Drizzle"]:
        multiplier += 0.3
        reason.append(f"Adverse weather: {weather_data.condition} conditions.")
    if weather_data.temperature < 5:
        multiplier += 0.2
        reason.append("Cold weather: temperature below 5°C.")
    elif weather_data.temperature > 30:
        multiplier += 0.2
        reason.append("Hot weather: temperature above 30°C.")
    
    final_multiplier = round(min(max(multiplier, 1.0), 3.0), 2)
    
    reason_str = " & ".join(reason) if reason else "Normal Pricing"

    return SurgeCalculation(
        multiplier=final_multiplier,
        reason=reason_str
    )