import requests

class Route(object):
    route_id = None
    route_name = None

    def __init__(self,name,route_id):
        super().__init__()
        self.name = name
        self.route_id = route_id
        self.route_stops = []

    def add_stop(self,id):
        self.route_stops.append(Stop(id,self.route_id))

class Stop(object):
    agency = 643
    next_arrival_times = []

    def __init__(self, id, route_id):
        self.id = id
        self.route_id = route_id

    def get_estimated_times():
        return requests.get("https://feeds.transloc.com/3/arrivals",{'agencies' : self.agency , 'stop_id' : self.id})

    def update_estimated_times():
        stop_times = get_estimated_times()
        for stop in stop_times:
            pass
