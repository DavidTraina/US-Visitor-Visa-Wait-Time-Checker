import json
import requests


def get_wait_time(code) -> int:
    resp = requests.get(
        f"https://travel.state.gov/content/travel/resources/database/database.getVisaWaitTimes.html?cid={code}&aid=VisaWaitTimesHomePage"
    ).text
    days = resp.strip().split(",", 1)[0].split(" ", 1)[0]
    try:
        return int(days)
    except ValueError:
        print(f"invalid: {days}")
        return 1000


def rank_cities():
    with open("./city_codes.json") as f:
        code_and_city_lst = json.load(f)
        code_to_city = {
            code_and_city["code"]: code_and_city["value"]
            for code_and_city in code_and_city_lst["sourceData"]
        }

    codes = code_to_city.keys()

    code_to_days = {code: get_wait_time(code) for code in codes}
    sorted_cities = [
        (code_to_city[code], days)
        for code, days in sorted(code_to_days.items(), key=lambda item: item[1])
    ]
    ranked_cities: str = "\n".join(
        f"{city}: {days} days" for city, days in sorted_cities
    )
    print(ranked_cities)
    with open("ranked_cities.txt", "w") as f:
        f.write(ranked_cities)


if __name__ == "__main__":
    rank_cities()
