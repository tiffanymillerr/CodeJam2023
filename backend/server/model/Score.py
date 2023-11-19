from model.Predictor import Predictor
from geopy.distance import geodesic
from model.Driver import Driver
from model.Load import Load
from typing import Tuple, List

COST_PER_MILE = 1.38

NN_PRED = Predictor('nn')
NN_PRED.load('data/model.h5')

RF_PRED = Predictor('rf')
RF_PRED.load('data/model.rf')

def predict(location: Tuple[float, float], hour: int, minute: int, day_of_week: int, is_weekend: bool) -> List[Load]:
    data = [location[0], location[1], hour, minute, day_of_week, is_weekend]
    allLoads = []
    for x in range(5, 65, 5):
        timedData = data
        # Increment time by x minutes (if over 60, loop around in next hour)
        if timedData[4] + x < 60:
            timedData[4] += x
        else:
            timedData[4] = timedData[4] + x - 60
            timedData[3] += 1

        # Predict a single load from RF
        rf_load = RF_PRED.predict(timedData, 1)         # 1 load
        allLoads.append(Load(
            0, rf_load[0], rf_load[1], rf_load[2], location[0], location[1], None, None
        ))
        # Predict 5 loads from NN
        nn_loads = NN_PRED.predict(timedData, 5)        # 5 loads (list)
        for nn_load in nn_loads:
            allLoads.append(Load(
            0, nn_load[0], nn_load[1], nn_load[2], location[0], location[1], None, None
        ))
    return allLoads

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    # Placeholder for a function that calculates the distance between two points
    return geodesic(point1, point2).miles

def calc_profit(load: Load, driver: Driver):
    distance_to_load = calculate_distance(driver.location, load.origin)
    deadhead_cost = distance_to_load * COST_PER_MILE
    profit = load.price - deadhead_cost
    return profit

def score(load: Load, driver: Driver) -> float:

    profit = calc_profit(load, driver)

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

def minScore(time: Tuple[int, int, int, int], driver: Driver) -> float:
    loads_predicted = predict(driver.location, *time)
    valid_scores = []
    # Append valid scores only
    for load in loads_predicted:
        s = score(load, driver)
        if s > 0:
            valid_scores.append(s)

    valid_scores.sort()
    # Calculate 80th percentile
    index = int(0.8 * len(valid_scores)) - 1

    if valid_scores:
        percentile_score = valid_scores[index]
    else:
        percentile_score = 0

    return percentile_score

def onLoadEvent(load: Load, current_time: Tuple[int, int, int, int], driver: Driver) -> bool:
    # Current_time +1 to rep every 1 hour

    min_score = minScore(current_time, driver)
    return score(load, driver) > min_score

# Note: missing 'calculate_distance', 'predict_loads', and 'notify' fcns
