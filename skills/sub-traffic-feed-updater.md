---
name: sub-traffic-feed-updater
description: Refresh real-time traffic/weather and re-optimize sensitive legs.
---

## Role
Sub-skill of `last-mile-delivery-route-optimizer`. Refresh real-time traffic/weather and re-optimize sensitive legs.

## Inputs
- Solution object from sub-scoring-engine
- Current timestamp for traffic/weather queries
- Geographic bounding box of delivery area
- Route segments identified as "sensitive" (tight time windows, high congestion risk)

## Procedure

### Step 1: Identify Re-optimization Candidates

1. **Analyze initial solution for sensitivity:**
   - **Tight time windows:** 
     - Identify stops where (latest_time - earliest_time) < 30 minutes
     - Flag routes with >2 tight-window stops as high-sensitivity
   - **High-traffic corridors:**
     - Identify routes through urban centers or major highways
     - Use known congestion patterns from traffic databases
   - **Long legs:**
     - Flag individual route legs > 15 km (more vulnerable to traffic variation)
   - **Weather-sensitive routes:**
     - Identify outdoor/long-exposure routes vulnerable to weather

2. **Prioritize re-optimization:**
   - Priority 1: Routes with tight windows AND high traffic exposure
   - Priority 2: Routes with tight windows only
   - Priority 3: Routes with high traffic exposure only
   - Priority 4: All other routes (baseline monitoring only)

### Step 2: Traffic Data Integration

#### Real-time Traffic Sources (Priority Order):
1. **Google Maps Traffic API (if available):**
   - Query: `GET https://maps.googleapis.com/maps/api/directions/json`
   - Parameters: origin, destination, departure_time=now, traffic_model=best_practices
   - Parse: `duration_in_traffic` field vs. `duration` base
   - Compute: traffic_factor = duration_in_traffic / duration

2. **TomTom Traffic API (if available):**
   - Query: `GET https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/tile/{z}/{x}/{y}`
   - Parse: `currentSpeed` vs. `freeFlowSpeed`
   - Compute: congestion_factor = freeFlowSpeed / currentSpeed

3. **INRIX Traffic (if available):**
   - Query regional traffic index for target area
   - Parse: `score` field (0-100 scale, 100 = free flow)
   - Compute: factor = score / 100

4. **Fallback: Historical traffic patterns:**
   - Use time-of-day profiles (morning peak: 7-9 AM, evening peak: 4-6 PM)
   - Apply multipliers: peak=1.8, off-peak=1.0, mid-day=1.2

#### Traffic Integration Procedure:
1. **For each prioritized route:**
   - Extract route leg coordinates (start_point, end_point)
   - Query traffic API for each leg
   - Collect travel time ratios (current / free_flow)

2. **Compute route-level traffic factor:**
   - Distance-weighted average of leg factors
   - Formula: 
     ```
     traffic_factor = Σ(leg_distance × leg_factor) / Σ(leg_distance)
     ```

3. **Classify congestion level:**
   - Free flow: factor < 1.2 (green)
   - Moderate: 1.2 ≤ factor < 1.5 (yellow)
   - Heavy: 1.5 ≤ factor < 2.0 (orange)
   - Severe: factor ≥ 2.0 (red)

### Step 3: Weather Data Integration

#### Weather Sources:
1. **OpenWeatherMap API (if available):**
   - Query: `GET https://api.openweathermap.org/data/2.5/weather`
   - Parse: `weather.main`, `weather.description`, `visibility`, `wind.speed`

2. **NOAA/NWS APIs (US region):**
   - Query weather alerts and conditions
   - Parse: severity, affected area, duration

3. **Fallback: Seasonal/historical averages:**
   - Apply safety factors by season/weather condition

#### Weather Impact Factors:
1. **Precipitation:**
   - Light rain: speed factor 0.9, visibility factor 0.95
   - Moderate rain: speed factor 0.8, visibility factor 0.85
   - Heavy rain: speed factor 0.7, visibility factor 0.7

2. **Snow/Ice:**
   - Light snow: speed factor 0.75, visibility factor 0.8
   - Moderate snow: speed factor 0.6, visibility factor 0.6
   - Heavy snow: speed factor 0.4, visibility factor 0.4

3. **Wind:**
   - Crosswind > 30 km/h: speed factor 0.9, stability factor 0.95
   - Head/tailwind: minimal impact for urban speeds

4. **Visibility:**
   - Fog/haze: reduce speed factor proportionally
   - Visibility < 200m: speed factor 0.5 or consider service suspension

5. **Extreme events:**
   - Severe thunderstorm, tornado, hurricane: recommend service suspension
   - Flag for manual review

#### Weather Integration Procedure:
1. **For each route:**
   - Determine route geographic center
   - Query weather API for current conditions
   - Compute weather factor = speed_factor × visibility_factor

2. **Apply combined impact:**
   - `combined_factor = traffic_factor × weather_factor`
   - Cap combined_factor at maximum 3.0 (avoid unrealistic extremes)

### Step 4: Re-optimization Execution

#### Trigger Conditions:
1. **Automatic re-optimization triggers:**
   - Combined factor ≥ 1.5 for any tight-window route leg
   - Combined factor ≥ 2.0 for any route leg
   - Weather factor < 0.7 (severe conditions)
   - Traffic alert from API (accident, road closure)

2. **Manual review triggers:**
   - Weather factor < 0.5 (extreme conditions)
   - Uncertain traffic data (API failure, stale data)
   - Combined factor > 3.0 (data quality suspect)

#### Re-optimization Process:
1. **Update distance/time matrix:**
   - Multiply affected leg travel times by combined_factor
   - Keep distances unchanged (physical geometry unchanged)
   - Propagate time window adjustments through network

2. **Re-run solver for affected routes:**
   - Use same solver strategy as initial solve
   - With updated time matrix
   - Time limit: reduced (10 seconds vs 30 seconds) for responsiveness

3. **Extract re-optimized solution:**
   - Compare vs. original: new routes, new sequences, new timings
   - Compute delta: distance change, time change, fuel impact

4. **Validate re-optimized solution:**
   - Check all constraints still satisfied
   - Ensure no time windows newly violated
   - Verify no degradation in other routes

### Step 5: Sensitive Leg Identification and Handling

#### Sensitive Leg Classification:
1. **Critical legs (must re-optimize):**
   - Tight time window (< 30 min) AND high traffic factor (> 1.3)
   - Single failure point (only one route option to cluster)
   - High fuel consumption leg (> 5% total route fuel)

2. **Important legs (monitor and adjust):**
   - Moderate time window (30-60 min) AND moderate traffic (1.1-1.3)
   - Legs through known congestion zones

3. **Standard legs (monitor only):**
   - Wide time windows (> 60 min)
   - Low traffic exposure (< 1.1 factor)

#### Handling Strategies:
1. **For critical legs with severe traffic:**
   - Explore alternative routes via OSRM (avoid high-traffic segments)
   - Consider pre-pone or post-pone time window by 15-30 minutes (if negotiable)
   - Flag for human dispatcher intervention if alternative unavailable

2. **For weather-critical legs:**
   - If weather_factor < 0.5, recommend delay until conditions improve
   - If weather_factor < 0.7, add buffer time (20% additional travel time estimate)
   - If extreme event alert, flag route for potential cancellation

3. **For time-critical legs:**
   - Compute probability of on-time arrival: P(on_time) based on traffic distribution
   - If P(on_time) < 0.8, recommend departure time advance
   - If P(on_time) < 0.5, flag for customer notification of potential delay

### Step 6: Output Structure
Return a traffic-updated solution object:

```json
{
  "traffic_weather_summary": {
    "query_timestamp": "ISO-8601",
    "data_sources": [string],
    "coverage_percent": number,
    "overall_congestion_level": "FREE_FLOW|MODERATE|HEAVY|SEVERE"
  },
  "route_updates": [
    {
      "vehicle_id": integer,
      "reoptimized": boolean,
      "traffic_factor": number,
      "weather_factor": number,
      "combined_factor": number,
      "sensitive_legs": [
        {
          "leg_index": integer,
          "from_stop": integer,
          "to_stop": integer,
          "original_time_minutes": number,
          "updated_time_minutes": number,
          "factor": number,
          "sensitivity": "CRITICAL|IMPORTANT|STANDARD"
        }
      ],
      "delta_vs_original": {
        "distance_km_change": number,
        "time_minutes_change": number,
        "fuel_liters_change": number,
        "new_time_window_violations": integer
      }
    }
  ],
  "aggregate_impacts": {
    "total_fuel_change_liters": number,
    "total_time_change_minutes": number,
    "newly_late_stops": integer,
    "improved_on_time_stops": integer,
    "routes_reoptimized": integer
  },
  "alerts": [
    {
      "severity": "INFO|WARNING|CRITICAL",
      "type": "TRAFFIC|WEATHER|TIME_WINDOW",
      "route_id": integer,
      "message": string,
      "recommended_action": string
    }
  ],
  "degradation_notes": [string]
}
```

### Step 7: Quality Gate Self-Check
Before returning control to the harness, verify:
- ✓ Traffic/weather data sources are cited
- ✓ Coverage percentage is stated (what % of routes had live data)
- ✓ All sensitive legs are identified and classified
- ✓ Re-optimization triggers are documented with rationale
- ✓ Output structure is complete and valid JSON
- ✓ Degradation notes explicitly state fallbacks used

## Outputs
- Traffic-weather updated solution object consumed by the next stage (sub-improvement-roadmap)
- Alerts for dispatcher attention
- Degradation notes for audit trail

## Tools
WebSearch (for weather/traffic status), WebFetch (for API queries), Read (for SECOND-KNOWLEDGE-BRAIN), Write (for intermediate outputs), Bash (for external API calls if configured)

## Quality Gate
- **Schema validity:** All required fields present with valid types
- **Framework grounding:** Traffic integration cites TomTom/INRIX/Google or fallback framework
- **Evidence linkage:** Each factor cites source API or fallback method
- **Completeness:** Both aggregate impacts and per-vehicle details provided
- **Transparency:** Degradation notes explicitly state when data unavailable

## Error Handling and Degradation
- If traffic APIs unavailable, use historical patterns with explicit note
- If weather APIs unavailable, use seasonal averages with explicit note
- If re-optimization fails, return original solution with traffic factors applied (static adjustment)
- If data coverage < 50%, flag solution as low-confidence and recommend manual review
