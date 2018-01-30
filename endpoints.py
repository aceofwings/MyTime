import time
import requests
import routeinfo
#get routes for buses
routes_url = "https://feeds.transloc.com/3/routes?agencies=643"
#get current vechicle Statuses
vechiles_url = "https://feeds.transloc.com/3/vehicle_statuses?agencies=643"
#Route Ids and there stops
route_stops_url = "https://feeds.transloc.com/3/stops?include_routes=true&agencies=643"

#parkpointArrivals = "https://feeds.transloc.com/3/arrivals?agencies=643&stop_id=4209570"

routes_of_interest = ["Perkins Green","The Province", "Park Point","Evening Eastside", "Weekend Retail"]
route_abreviations = ["PG", "TP" , "PP" , "EE" , "WR"]
stops_of_interest = [4177288,4197450,4209570]

def get_current_time():
    return time.now()

def get_all_routes():
    """All routes regardless of activity"""
    return requests.get(routes_url).json()['routes']

def get_current_routes():
    """Routes  that are currently active"""
    routes = {}
    req =  requests.get(routes_url).json()
    for route in req['routes']:
        if route['is_active']:
            routes[route['id']]  = routeinfo.Route(route['long_name'], route['id'])
    return routes
def get_routes_of_interest():
    routes = get_all_routes()
    raw_routes = []
    for route in routes:
        for index,route_name in enumerate(routes_of_interest):
            if route['long_name'] == route_name:
                route['alias'] = route_abreviations[index]
                raw_routes.append(route)
    routes_infos = {}
    for rr in raw_routes:
        routes_infos[rr['id']] = routeinfo.Route(rr['long_name'],rr['id'], rr['alias'], rr['color'], rr['is_active'])

    stops  = get_assosciated_stops()
    for stop in stops:
        for soi in stops_of_interest:
            if soi in stop['stops']:
                if (stop['id'] == 4010148 or stop['id']  == 4010122)  and  soi != 4209570:
                    pass
                else:
                    try:
                        routes_infos[stop['id']].add_stop(soi)
                    except KeyError:
                        pass
    return routes_infos

def get_vechicles():
    request = requests.get(vechiles_url)
    if request.status_code == 200:
        return request.json()['vehicles']


def get_assosciated_stops():
    request = requests.get(route_stops_url)
    if request.status_code == 200:
        return request.json()['routes']
    else:
        raise BadRequest()


def gets_stops():
    request = requests.get(route_stops_url)
    if request.status_code == 200:
        return request.json()['stops']
    else:
        raise BadRequest()

def full_stop_request():
    request = requests.get(vechiles_url)
    if request.status_code == 200:
        return request.json()
    else:
        raise BadRequest()

def full_stop_request(agency,id):
    request = requests.get("https://feeds.transloc.com/3/arrivals",{'agencies' : agency , 'stop_id' : id})
    if request.status_code == 200:
        return request.json()
    else:
        raise BadRequest()

def print_stops(route=None):
    stops = requests.get(route_stops_url).json()['stops']
    for stop in stops:
        print (stop)

def print_routes():
    routes = get_all_routes()
    print("   Long Name   :  ID   ")
    for route in routes:
        print(route['long_name'] + " : " + str(route['id']) )

if __name__ == "__main__":
    routes = get_routes_of_interest()
    for key,route in routes.items():
        for stop in route.route_stops:
            print(stop.get_estimated_times())

class BadRequest(Exception):
    pass
