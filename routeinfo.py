import requests
import endpoints
import time

class Cache(object):
    last_update = None
    current_routes =None
    @classmethod
    def get_current_routes(cls,force=False):
        if cls.last_update is None:
            cls.current_routes = endpoints.get_current_routes()
            cls.last_update = time.time()
            return cls.current_routes
        else:
            diff = time.time() - cls.last_update
            if diff > 30:
                cls.current_routes = endpoints.get_current_routes()
                cls.last_update = time.time()
                return cls.current_routes
            else:
                return cls.current_routes

class Route(object):
    route_id = None
    route_name = None

    def __init__(self,name,route_id):
        super().__init__()
        self.name = name
        self.route_id = route_id
        self.route_stops = []

    def __eq__(self, other):
        return self.route_id == other.route_id

    def __str__(self):
        return self.name

    def add_stop(self,id):
        self.route_stops.append(Stop(id,self.route_id))

    def is_active(self):
        currents = Cache.get_current_routes()
        if self.route_id in currents:
            return True
        else:
            return False

#{"arrivals": [{"distance": 5364.36, "route_id": 4010148, "stop_id": 4209570, "timestamp": 1516463100, "type": "vehicle-based", "vehicle_id": 4012847}], "success": true}
class Stop(object):
    agency = 643
    next_arrival_times = []

    def __init__(self, id, route_id):
        self.id = id
        self.route_id = route_id

    def get_estimated_times():
        return requests.get("https://feeds.transloc.com/3/arrivals",{'agencies' : self.agency , 'stop_id' : self.id})

    def update_estimated_times():
        stop_times = endpoints.get_estimated_times()
        for stop in stop_times:
            pass

if __name__ == "__main__":
    routes = endpoints.get_routes_of_interest()
    for key, value in routes.items():
        print(value.is_active())
