import requests
import endpoints
import time

class Cache(object):
    last_update = None
    last_stop_update = None
    current_routes = None
    routes_of_interest = None
    bus_bounds = None
    last_vehicle_update = None

    def safety(func):
        """
        Wrap the function calls dealing with requests in a safety mechanism
        I don't know what the decoding error is
        """
        def func_wrapper(cls):
            try:
                return func(cls)
            except endpoints.BadRequest:
                return func(cls,cache=True)
        return func_wrapper

    @classmethod
    #@safety
    def get_current_routes(cls,force=False, cache=False):
        if cache:
            return cls.current_routes
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

    @classmethod
    #@safety
    def get_routes_of_interest(cls,cache = False):
        if cache:
            return cls.routes_of_interest
        if cls.last_update is None:
            cls.routes_of_interest = endpoints.get_routes_of_interest()
            cls.last_update = time.time()
            return cls.routes_of_interest
        else:
            diff = time.time() - cls.last_update
            if diff > 15:
                cls.routes_of_interest = endpoints.get_routes_of_interest()
                cls.update_stops(force=True)
                cls.last_update = time.time()
                return cls.routes_of_interest
            else:
                return cls.routes_of_interest
    @classmethod
    def update_routes_of_interest(cls):
        pass

    @classmethod
    #safety
    def update_stops(cls,force=False,cache=False):
        if cache:
            return
        if cls.last_stop_update is None or force:
            for key,route in cls.routes_of_interest.items():
                for stop in route.route_stops:
                    stop.update_estimated_times()
            cls.last_stop_update = time.time()
        diff = time.time() - cls.last_stop_update

        if diff > 20:
            for key,route in cls.routes_of_interest.items():
                for stop in route.route_stops:
                    stop.update_estimated_times()
            cls.last_stop_update = time.time()

    @classmethod
    #safety
    def update_vehicle_locations(cls, force=False,cache=False):
        if cache:
            return cls.bus_bounds
        vechicles = {}
        vechicles_h = endpoints.get_vechicles()
        if cls.last_vehicle_update is None or force:
            for vechicle in vechicles_h:
                vechicles[vechicle['route_id']] = vechicle['position']
            cls.last_vehicle_update = time.time()
            cls.bus_bounds = vechicles
            return vechicles
        diff = time.time() - cls.last_vehicle_update
        if diff > 2:
            for vechicle in vechicles_h:
                vechicles[vechicle['route_id']] = vechicle['position']
            cls.last_vehicle_update = time.time()
            cls.bus_bounds = vechicles
            return cls.bus_bounds
        else:
            return cls.bus_bounds



class Route(object):
    route_id = None
    route_name = None

    def __init__(self,name,route_id,alias,color,active):
        super().__init__()
        self.name = name
        self.route_id = route_id
        self.route_stops = []
        self.alias = alias
        self.color = color
        self.active = active
        self.busCordinates = (0,0)

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
    next_arrival_time = None

    def __init__(self, id, route_id):
        self.id = id
        self.route_id = route_id

    def get_estimated_times(self):
        return endpoints.full_stop_request(self.agency,self.id)

    def update_estimated_times(self):
        stop_times = self.get_estimated_times()
        if stop_times is not None:
            if stop_times['arrivals']:
                stop_time  = stop_times['arrivals'][0]
                if stop_time:
                    if stop_time['route_id'] == self.route_id:
                        self.next_arrival_time = stop_time['timestamp']


if __name__ == "__main__":
    pass
