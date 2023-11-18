score(load, driver) --> integer

minScore(t_i, t_f, driver):
    1. Predict all loads within time [t_i, t_f]
        --> returns loadPredicted (list of loads)
    2. Calc score from loc (of driver) to each of the predicted loads from above
        for l in loadPredicted:
            score(l, driver)
    3. Return --> Figure out the 80th percentile of scores calculated

onLoadEvent => (load) {
    s = minScore(curTime, curTime + 1 hour, driver)
    if ( score(load, driver) > s) {
        notify(driver)
    } else {
        nothing
    }
}