# https://www.visualcrossing.com/weather/weather-data-services?pln=plan_GqkYVnzyiNg93X#/timeline
# https://www.visualcrossing.com/weather-api
import requests
import json


# Convert degrees to compass direction
def deg_to_compass(num):
    val = int((num / 22.5) + 0.5)
    arr = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return arr[(val % 16)]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class ApiVisualCrossing:
    def __init__(self):
        self.data = None

    def refresh(self, location="", api_key="", data_units="metric"):
        url = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            f"{location}/today"
            f"?unitGroup={data_units}"
            f"&key={api_key}"
            "&include=fcst%2Ccurrent"
        )

        result = requests.get(url)

        if result.status_code == 200:
            self.data = result.json()
        else:
            self.data = None

    def get_timestamp(self):
        return self.get_element(("currentConditions", "datetime"), "N/A")

    def get_resolved_address(self):
        ret_val = "N/A"
        if self.data is not None:
            ret_val = self.data["resolvedAddress"]
        return ret_val

    def get_temperature(self):
        return self.get_element(("currentConditions", "temp"), "N/A")

    def get_feels_like_temperature(self):
        return self.get_element(("currentConditions", "feelslike"), "N/A")

    def get_low_temperature(self):
        return self.get_element(("days", "tempmin"), "N/A")

    def get_high_temperature(self):
        return self.get_element(("days", "tempmax"), "N/A")

    def get_wind_speed(self):
        return self.get_element(("currentConditions", "windspeed"), "N/A")

    def get_wind_gust(self):
        return self.get_element(("currentConditions", "windgust"), "0")

    def get_wind_direction(self):
        ret_val = self.get_element(("currentConditions", "winddir"), "N/A")
        if is_number(ret_val):
            ret_val = deg_to_compass(ret_val)

        return ret_val

    def get_precip(self):
        return self.get_element(("currentConditions", "precip"), "0")

    def get_precip_prob(self):
        return self.get_element(("currentConditions", "precipprob"), "0")

    def get_element(self, keys, default="", round_val=True):
        ret_val = default

        if self.data is not None:

            ret_val = self.data[keys[0]]

            if isinstance(ret_val, list):
                ret_val = ret_val[0][keys[1]]
            else:
                ret_val = ret_val[keys[1]]

            if ret_val:
                if round and is_number(ret_val):
                    ret_val = round(float(ret_val))
            else:
                ret_val = default

        return ret_val


if __name__ == "__main__":
    api = ApiVisualCrossing()

    api.refresh("32.52402,-97.29605", "")

    print(json.dumps(api.data, indent=4))

    # print('Address: ', api.get_resolved_address())
    # print('Time: ', api.get_timestamp())
    # print('Temperature: ', api.get_temperature())
    # print('Feels Like: ', api.get_feels_like_temperature())
    # print('Low Temperature: ', api.get_low_temperature())
    # print('High Temperature: ', api.get_high_temperature())
    # print('Wind Speed: ', api.get_wind_speed())
    # print('Wind Gust: ', api.get_wind_gust())
    # print('Wind Direction From: ', api.get_wind_direction())
    # print('Precipitation: ', api.get_precip())
    # print('Precipitation Probability: ', api.get_precip_prob())
