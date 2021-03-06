import nextbus

def get_all_routes():
    routes = nextbus.get_all_routes_for_agency('sf-muni')
    list = []
    for route in routes:
        route_dict = {}
        route_dict['tag'], route_dict['title'] = route.tag, route.title
        list.append(route_dict)
    return list

def get_all_directions(route_tag):
    route = nextbus.get_route_config('sf-muni',route_tag)
    directions = route.directions
    dir = []
    for each in directions:
        dir_dict = {}
        dir_dict['tag'], dir_dict['title'] = each.tag, each.title
        dir.append(dir_dict)
    return dir

def get_predictions_for_stop(stop_id, route_tag):
    predictions = nextbus.get_predictions_for_stop('sf-muni',stop_id)

    list_prediction = []
    for prediction in predictions.predictions:
        if prediction.direction.route.tag == route_tag:
            list_prediction.append(prediction)
    return list_prediction


def get_all_stops(route_tag, direction_tag):
    route = nextbus.get_route_config('sf-muni', route_tag)
    directions = route.directions
    stop_list = []
    for each in directions:
        if each.tag == direction_tag:
            stops = each.stops
            for stop in stops:
                stop_dict = {}
                stop_dict['tag'] = stop.tag
                stop_dict['title'] = stop.title
                stop_dict['stop_id'] = stop.stop_id
                stop_list.append(stop_dict)
    return stop_list
