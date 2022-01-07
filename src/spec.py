from enum import Enum

# jids
fishery_recommender = {
    "username": "fishery_recommender"
}
client_reporter = {
    "username": "client_reporter"
}
crowd_monitoring = {
    "username": "crowd_monitoring"
}
data_accumulator = {
    "username": "data_accumulator"
}
fish_content_monitoring = {
    "username": "fish_content_monitoring"
}
user = {
    "username": "user"
}
water_monitoring = {
    "username": "water_monitoring"
}
weather_monitoring = {
    "username": "weather_monitoring"
}
password = '1qaz@WSX'
host = "localhost"


class DataType(Enum):
    CROWD = 'Crowd'
    FISH_CONTENT = 'Fish content'
    WATER_QUALITY = 'Water quality'
    WEATHER = 'Weather'
    RECOMMENDATION_REQUEST = 'Recommendation request'
    RECOMMENDATION_RESPONSE = 'Recommendation response'
    DATA_REQUEST = 'Data request'
    DATA_RESPONSE = 'Data response'
