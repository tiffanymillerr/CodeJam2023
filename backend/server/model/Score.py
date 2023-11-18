COST_PER_MILE = 1.38

def calculate_distance(point1, point2):
    # Placeholder for a function that calculates the distance between two points
    return abs(point1 - point2)

def score(load, driver):
    distance_to_load = calculate_distance(driver.location, load.origin)
    deadhead_cost = distance_to_load * COST_PER_MILE
    profit = load.price - deadhead_cost

    # Adjust score based on equip type and trip length preference
    if driver.equip_type != load.equipment_type:
        return 0

    if load.mileage >= 200:
        trip_length = 'Long' 
    else:
        trip_length ='Short'
    
    if driver.trip_length_preference != trip_length:
        profit *= 0.5  # Half the score if trip length preference doesn't match

    return profit

def minScore(t_i, t_f, driver, predict_loads):
    loads_predicted = predict_loads(t_i, t_f)
    valid_scores = []
    # Append valid scores only
    for load in loads_predicted:
        if score(load, driver) > 0:
            valid_scores.append(score(load, driver))

    valid_scores.sort()
    # Calculate 80th percentile
    index = int(0.8 * len(valid_scores)) - 1
    
    if valid_scores:
        percentile_score = valid_scores[index]
    else:
        percentile_score = 0

    return percentile_score

def onLoadEvent(load, current_time, driver, predict_loads):
    # Current_time +1 to rep every 1 hour
    min_score = minScore(current_time, current_time + 1, driver, predict_loads)
    if score(load, driver) > min_score:
        notify(driver)  # Notify driver
    else:
        pass

# Note: missing 'calculate_distance', 'predict_loads', and 'notify' fcns

