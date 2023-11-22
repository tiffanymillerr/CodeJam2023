# Freight Elite: Optimizing Truck Load Selection
# Inspiration
Our problem motivation is that the trucking industry, vital to the global economy, faces significant inefficiencies in load selection. Our team, inspired by the challenges faced by truckers every day, set out to revolutionize how they interact with load boards. We aimed to create a tool to notify truckers of ideal loads given their location and preferred preferences, all while maximizing profit.

We developed a solution to notify truckers of the best new loads on the marketplace, while keeping the “noise” to a minimum. Hence, Freight Elite was born.

# Our Algorithm
Our algorithm efficiently predicts, scores, and notifies truckers of optimal loads. It starts by predicting potential loads using data patterns, like time and day trends. The core is a dynamic scoring system that asses driver-load compatibility based on profitability, taking into account the trucker's preferences and current location. Incompatibilities in equipment type or trip length significantly impact the profit score.

Every hour, we calculate a minimum score threshold, set at the 80th percentile of predicted loads, to ensure relevance and quality. A trucker is notified only if a load's compatibility score is bigger than the minimum threshold score (calculated by the hourly 80th percentile). Hence streamlining the process and enhancing decision-making efficiency.

Essentially, the incorporated predictive model in our solution anticipates load availability, ensuring our notifications are both timely and relevant.

The frontend, designed for simplicity, ensures truckers can easily specify their preferences and view the most suitable loads.

# How we built it
Freight Elite is built using Python, leveraging MQTT for real-time data communication. To enhance the accuracy of our system, we used TensorFlow and Scikit-learn to develop robust predictive models for load forecasting. Docker was used to run the server.

The frontend, using Flutter, was designed for simplicity. The UI depicts the custom notifications being sent to truckers in real time.

# Challenges Faced
One of the largest challenges was developing an algorithm to ensure truckers don't miss out on more profitable opportunities by balancing the current availability of loads with future projections The complex nature of handling data processing in real-time posed an additional challenge.

It took multiple revisions to ensure our solution was easy for truckers to get notifications, who are frequently on the go and appreciate simple interfaces.

# What's next for Freight Elite
Our project has many future plans. First we aspire to have a functionality that logs whether a trucker accepted a load, and thus that particular load would no longer be available to other truckers once accepted. Additionally, we would have liked to have a log-in page where users can input their preferences. Lastly, another cool idea we had for future development included a page of load prediction graphs for that day to visually demonstrate to the driver how the system is working.
