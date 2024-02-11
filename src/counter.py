from flask import Flask
from src import status

app = Flask(__name__)

COUNTERS = {}


# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Updates a counter"""
    app.logger.info(f"Request to update counter: {name}")
    global COUNTERS
    COUNTERS[name] = COUNTERS[name] + 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/read/<name>', methods=['get'])
def get_counter(name):
    """Gets a counter"""
    app.logger.info(f"Request to get counter: {name}")
    global COUNTERS
    if name not in COUNTERS:
        return {"message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND
    return {"message": f"Counter: {name} reads at: {COUNTERS[name]}"}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['delete'])
def delete_counter(name):
    """Deletes a counter"""
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS
    del COUNTERS[name]
    return {}, status.HTTP_204_NO_CONTENT
