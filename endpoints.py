import time
import requests
#get routes for buses
routes_url = "https://feeds.transloc.com/3/routes?agencies=643"
#get current vechicle Statuses
vechiles_url = "https://feeds.transloc.com/3/vehicle_statuses?agencies=643"
#Arrivals for parkpoint bus
parkpointArrivals = "https://feeds.transloc.com/3/arrivals?agencies=643&stop_id=4209570"
#Route Ids and there stops
route_stops_url = "https://feeds.transloc.com/3/stops?include_routes=true&agencies=643"

routes_of_interest = ["Weekend Inn & Racquet Club","Colony Manor","Perkins Green","The Province", "Park Point","Evening Eastside"]
stops_of_interest = []

def get_current_time():
    return time.now()

def get_all_routes():
    """All routes regardless of activity"""
    return requests.get(routes_url).json()['routes']

def get_current_routes():
    """Routes  that are currently active"""
    routes = []
    req =  requests.get(routes_url).json()
    for route in req['routes']:
        if route['is_active']:
            routes.append(route)
    return routes

def get_vechicles():
    return request.get(vechiles)

def print_stops(route=None):
    stops = requests.get(route_stops_url).json()
    

def print_routes():
    routes = get_all_routes()
    print("   Long Name   :  ID   ")
    for route in routes:
        print(route['long_name'] + " : " + str(route['id']) )

if __name__ == "__main__":
    print_stops()
