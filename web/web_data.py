from web import web_visit
import requests
from collections import *
from nearby import googleMapsApi


# ------------------------------------------- Train Station Wikipedia Info ---------------------------------------------
def station_information(station_name):
    station_name_lower = station_name.replace("Station", "station")
    station_name = station_name_lower.replace(" ", "_").replace("&", "%26")
    url = "https://en.wikipedia.org/w/api.php?action=query&generator=search&utf8=1&gsrsearch={0}&prop=extracts" \
          "&exintro=&explaintext=&format=json".format(station_name)
    wiki_api_response = requests.get(url)
    wiki_dict = wiki_api_response.json()
    text_summary = wiki_dict['query']['pages']
    for item in text_summary:
        match = text_summary[item]['title']
        if match == station_name_lower:
            extract = text_summary[item]['extract']
            return extract
    return ""
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------- Local Crime Data ---------------------------------------------------
def crime(post_code):

    api_key = "AIzaSyDnB2ber8l-M2NuVDfT30PHDT9B6hbJNMw"
    api_response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(post_code, api_key))
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        address = "https://data.police.uk/api/locate-neighbourhood?q={},{}".format(latitude, longitude)

        police_api = requests.get(address)
        police_api_dict = police_api.json()
        force_name = police_api_dict['force']
        force_id = police_api_dict['neighbourhood']
        crime_area_info(force_name, force_id, post_code)
        crime_performance(force_name, force_id)


# Nearest Police Station
def crime_area_info(force_name, force_id, post_code):
    area_info_api = requests.get('https://data.police.uk/api/{0}/{1}'.format(force_name, force_id))
    area_info_api_dict = area_info_api.json()
    print(area_info_api_dict['locations'][0]['name'])
    print(area_info_api_dict['locations'][0]['address'])
    print(area_info_api_dict['locations'][0]['postcode'])
    lat = area_info_api_dict['centre']['latitude']
    lng = area_info_api_dict['centre']['longitude']
    lat_lang = lat + " " + lng
    print("Distance: ", googleMapsApi.distance_calc(post_code, lat_lang))


# Crime Summary
def crime_performance(force_name, force_id):
    web_visit.soup_setup()
    performance_address = "https://www.police.uk/{0}/{1}/performance/compare-your-area/".format(force_name, force_id)
    soup_performance_web_page = web_visit.soup_visit(performance_address)
    print(soup_performance_web_page.find("div", {"class": "summary"}).text.strip())

    tb_name_list = []
    tb_data_list = []
    table = soup_performance_web_page.find("table", {"id": "msg_csp_table"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        tb_name = row.find('th')
        text = tb_name.renderContents().decode('utf-8')
        trimmed_text = text.strip()
        tb_name_list.append(trimmed_text)

        td_name = row.find('td')
        text = td_name.renderContents().decode('utf-8')
        trimmed_text = text.strip()
        tb_data_list.append(trimmed_text)

    table_dict = OrderedDict(zip(tb_name_list, tb_data_list))
    print(table_dict)


# station_information("Chalfont & Latimer Station")
# crime("HP6 6SW")
# ----------------------------------------------------------------------------------------------------------------------
