'''
    api.py
    Katrina Li, Lily Li, Wenlai Han,
    10 November 2020
    Last update: 23 November 2020

    A comprehensive Flask API to support the Lilian Natural Disaster web application.
    Endpoints that we have, in the order of code, are:
        get_countries() -- line 44,
        get_country_ids() -- line 76,
        get_disaster_ids() -- line 110,
        get_natural_disaster_full_info_year(year) -- line 122,
        get_cumulative_country_cases(disaster_type_id, country_id) -- line 201,
        get_country_disaster_intensity(country_id) -- line 260,
        get_country_disaster_intensity_all() -- line 350

    
'''
import sys
import flask
import json
import config
import psycopg2
import collections

########### Initializing Flask ###########
api = flask.Blueprint('api', __name__)


########### Utility function ###########
def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)


########### The API endpoints ###########


@api.route('/countries')
def get_countries():
    '''
    Returns all countries that have disasters in the following form:
    {name_of_country1 : country_id, name_of_country2 : country_id...}
    like
    {'Afghanistan': 3, 'Albania': 4, ...}

    Raises exceptions on network connection errors and on data
    format errors.
    '''
    query = '''SELECT disasters.country_id, country.id, country.name FROM disasters,
    country WHERE country.id = disasters.country_id'''

    countries = {}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            country_name = row[2][0: 1] + row[2][1:].lower()
            if country_name not in countries.keys():
                countries[country_name] = row[0]
        countries = collections.OrderedDict(sorted(countries.items()))
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(countries)


@api.route('/country_id_converter')
def get_country_ids():
    '''

    Returns all countries that have disasters in the following form:
    {country_id1:name_of_country1, country_id2: name_of_country2, ...}
    like
    [{ '3': 'Afghanistan',  '4': 'Albania', ...}]

    Raises exceptions on network connection errors and on data
    format errors.

    '''
    query = '''SELECT disasters.country_id, country.id, country.name FROM disasters,
    country WHERE country.id = disasters.country_id'''

    countries = {}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            country_id = row[1]
            if country_id not in countries.keys():
                countries[country_id] = row[2][0: 1] + row[2][1:].lower()
        countries = collections.OrderedDict(sorted(countries.items()))
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps([countries])


@api.route('/disaster_id_converter')
def get_disaster_ids():
    '''
    Returns the following dictionary in a list. We figured out that this is the 
    cleanest way for coding and understanding and hopefully still easy 
    for maintainance considerations, as there would not be a lot of types
    of disasters.
    '''

    return json.dumps([{"0": "Earthquake", "1": "Tsunami", "2": "Volcanic eruption"}])


@api.route('/natural_disaster_full_info/year/<year>')
def get_natural_disaster_full_info_year(year):
    '''
    Returns a list of dictionaries which each contains a disaster
    in the following form
    [
        {"disaster_id": 0, "country_id": 1, ...  "intensity_or_magnitude": 1, ...},
        {"disaster_id"...}, 
        {"disaster_id"...},
        ...
    ]
    In each dictionary, we have keys in the following order:
    "disaster_id", "country_id", "disaster_type_id", "longitude", "latitude",
    "death", "hour", "intensity_or_magnitude", "year".

    The year parameter must be an integer between 1950 to 2020 
    (js would judge this, so we did not do "%" + year + "%").

    Raises exceptions on network connection errors and on data
    format errors.
    '''

    earthquake_query = f'''SELECT disasters.id, disasters.country_id,
                        disasters.disaster_type_id, 
                        longitude, latitude, deaths, hour,
                        earthquake_data.disaster_id, 
                        magnitude, 
                        CAST(Extract(YEAR FROM disasters.date) AS INT) 
                        FROM disasters, earthquake_data 
                        WHERE disasters.disaster_type_id = 0 
                        AND disasters.id = earthquake_data.disaster_id 
                        AND Extract(YEAR FROM disasters.date) = {year}'''

    tsunami_query = f'''SELECT disasters.id, disasters.country_id, 
                     disasters.disaster_type_id, 
                     longitude, latitude, deaths, hour, 
                     tsunami_data.disaster_id, 
                     max_water_height_meter, 
                     CAST(Extract(YEAR FROM disasters.date) AS INT)
                     FROM disasters, tsunami_data 
                     WHERE disasters.disaster_type_id = 1 
                     AND disasters.id = tsunami_data.disaster_id 
                     AND Extract(YEAR FROM disasters.date) = {year}'''

    volcano_query = f'''SELECT disasters.id, disasters.country_id,
                     disasters.disaster_type_id, 
                     longitude, latitude, deaths, hour, 
                     volcano_eruption_data.disaster_id, 
                     volcanic_explosivity_index, 
                     CAST(Extract(YEAR FROM disasters.date) AS INT)
                     FROM disasters, volcano_eruption_data 
                     WHERE disasters.disaster_type_id = 2 
                     AND disasters.id = volcano_eruption_data.disaster_id 
                     AND Extract(YEAR FROM disasters.date) = {year}'''

    queries = [earthquake_query, tsunami_query, volcano_query]
    natural_disaster_full_info = []
    try:
        connection = get_connection()

        for query in queries:  # will loop 3 times
            cursor = connection.cursor()
            cursor.execute(query)
            for row in cursor:
                event = {"disaster_id": row[0], "country_id": row[1],
                         "disaster_type_id": row[2], "longitude": row[3],
                         "latitude": row[4], "death": row[5],
                         "hour": row[6], "intensity_or_magnitude": row[8],
                         "year": row[9]
                         }

                natural_disaster_full_info.append(event)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return json.dumps(natural_disaster_full_info)


@api.route('/cumulative_country_cases/<disaster_type_id>/<country_id>')
def get_cumulative_country_cases(disaster_type_id, country_id):
    ''' Returns a JSON list of dictionaries, 
        each containing the year and the sum of cases before that year:
        Example:
        REQUEST: cumulative_country_cases/1(that indicates tsunami)/10(whatever country it is)
        If there are 10 cases in 1970, 15 in 1971, 20 in 1972, then
        [{1970: 10},{1971:25},{1972:45}]

        The disaster_type_id parameter must be an integer between 0 to 2 inclusive.
        The country_id parameter is an integer between 0 to about 200.

        JavaScript takes care of calling this function by asking the user with dropdown lists,
        and all the data would directly come from JavaScript dropdown lists.
        However, if the user mess up with url such as making disaster_type_id = 5, 
        then the response would either be zeros in dictionary values or empty lists.

        we don't have to worry about user messing up with the data, since if
        the user mess up with url, the response would either be zeros in 
        dictionary values or empty lists.

        Therefore using f-string here to extract user input does not cause
        injection issues.

        Raises exceptions on network connection errors and on data
        format errors.
    '''
    query = f'''SELECT CAST(Extract(YEAR FROM disasters.date) AS INT), 
            disasters.country_id, disasters.disaster_type_id 
            FROM disasters 
            WHERE disasters.country_id = {country_id} 
            AND disasters.disaster_type_id = {disaster_type_id}'''

    cumulative_country_case_datalist = []  # [{1970: 10},{1971:25},{1972:45}]
    cumulative_country_case_temp = {}  # {1970:10,1971:15,1972:15...}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (disaster_type_id, country_id))
        for row in cursor:
            year = row[0]
            cumulative_country_case_temp[year] = cumulative_country_case_temp.get(
                year, 0) + 1

        sum_cases = 0
        for empty_year in range(1950, 2021):
            if empty_year not in cumulative_country_case_temp.keys():
                cumulative_country_case_temp[empty_year] = 0
        for year in sorted(cumulative_country_case_temp.keys()):
            sum_cases += cumulative_country_case_temp.get(year)
            cumulative_country_case_datalist.append({year: sum_cases})
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(cumulative_country_case_datalist)


@api.route('/country_disaster_intensity/<country_id>')
def get_country_disaster_intensity(country_id):
    '''
    Returns a JSON dictionary of three keys which values are dictionaries, 
    each being a disaster event set for earthquake, tsunami, and volcano eruption,
    with all the corresponding disaster magnitude/intensity in them.
    Attributes:
    disaster_type_id -- (integer) disaster id that represents a disaster type
    case_frequency --(integer) that represents the sum of all cases between 1950-2020.

    Example:
    {
        earthquake: {   4.0: 0, 
                        4.3: 1, 
                        5.0: 3, 
                        5.5: 0, 
                        6.0: 4, 
                        7.5: 2    },
        tsunami: {3.0: 0, 3.2: 1, 3.3: 3, 3.6: 0}, 
        volcano_eruption: {1.0: 0, 2.0:1, 3.0: 4, 3.5: 2}
    }

    The country_id parameter is an integer between 0 to about 200.
    JavaScript takes care of calling this function by asking the user
    the relative country name with dropdown lists, so all the data would
    directly come from JavaScript dropdown lists. It would also group
    the data with ranges and ignore extreme values.

    we don't have to worry about user messing up with the data, since if
    the user mess up with url, the response would either be zeros in 
    dictionary values or empty lists.

    Therefore using f-string here to extract user input does not cause
    injection issues.

    Raises exceptions on network connection errors and on data
    format errors.

    '''

    earthquake_query = f'''SELECT disasters.country_id, disasters.id,
                        earthquake_data.disaster_id, magnitude 
                        FROM disasters, earthquake_data 
                        WHERE earthquake_data.disaster_id = disasters.id 
                        AND disasters.country_id = {country_id} 
                        AND disasters.disaster_type_id = 0 '''

    tsunami_query = f'''SELECT disasters.country_id, disasters.id, 
                     tsunami_data.disaster_id, max_water_height_meter
                     FROM disasters, tsunami_data
                     WHERE tsunami_data.disaster_id = disasters.id 
                     AND disasters.country_id = {country_id} 
                     AND disasters.disaster_type_id = 1 '''

    volcano_query = f'''SELECT disasters.country_id, disasters.id, 
                     volcano_eruption_data.disaster_id, volcanic_explosivity_index
                     FROM disasters, volcano_eruption_data
                     WHERE volcano_eruption_data.disaster_id = disasters.id 
                     AND disasters.country_id = {country_id} 
                     AND disasters.disaster_type_id = 2 '''

    # initialization of output dictionary
    intensity_dict = {"earthquake": {}, "tsunami": {}, "volcano": {}}
    queries = [earthquake_query, tsunami_query, volcano_query]
    try:
        connection = get_connection()
        index = 0
        for disaster_type in intensity_dict.keys():
            cursor = connection.cursor()
            cursor.execute(queries[index])
            index += 1
            for row in cursor:
                key_list = intensity_dict[disaster_type].keys()
                if row[3] == None:  # magnitude, max_water_height_meter, etc
                    continue
                x_axis_value = int(row[3])  # String int issues here (solved)
                if x_axis_value not in key_list:
                    intensity_dict[disaster_type][x_axis_value] = 1
                else:
                    intensity_dict[disaster_type][x_axis_value] += 1
            cursor.close()
            intensity_dict[disaster_type] = collections.OrderedDict(
                sorted(intensity_dict[disaster_type].items()))
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(intensity_dict)


@api.route('/country_disaster_intensity/all')
def get_country_disaster_intensity_all():
    '''

    Returns a JSON dictionary of three keys which values are dictionaries,
    each being a disaster event set for earthquake, tsunami, and volcano eruption,
    with all the corresponding disaster magnitude/intensity in them.

    (Equivalent to get_country_disaster_intensity(WORLD), 
     code is similar to get_country_disaster_intensity,
     and we'll save some comments here)

    Example:
    {
        earthquake: {4.4: 0, 4.5: 10, 4.6: 11, 4.7: 8, 4.8: 3, ...},
        tsunami: {3.0: 5, 3.1: 2, 3.2: 10, 3.3: 2, 3.4: 23}, 
        volcano_eruption: {1.0: 10, 2.0: 15, 3.0: 42, 4.0: 23}
    }

    The country_id parameter is an integer between 0 to about 200.

    Raises exceptions on network connection errors and on data
    format errors.
    '''

    earthquake_query = f'''SELECT disasters.country_id, disasters.id, 
                        earthquake_data.disaster_id, magnitude 
                        FROM disasters, earthquake_data 
                        WHERE earthquake_data.disaster_id = disasters.id 
                        AND disasters.disaster_type_id = 0 '''

    tsunami_query = f'''SELECT disasters.country_id, disasters.id, 
                     tsunami_data.disaster_id, max_water_height_meter
                     FROM disasters, tsunami_data
                     WHERE tsunami_data.disaster_id = disasters.id 
                     AND disasters.disaster_type_id = 1 '''

    volcano_query = f'''SELECT disasters.country_id, disasters.id, 
                     volcano_eruption_data.disaster_id, volcanic_explosivity_index
                     FROM disasters, volcano_eruption_data
                     WHERE volcano_eruption_data.disaster_id = disasters.id 
                     AND disasters.disaster_type_id = 2 '''

    # initialization of output dictionary
    intensity_dict = {"earthquake": {}, "tsunami": {}, "volcano": {}}
    queries = [earthquake_query, tsunami_query, volcano_query]
    try:
        connection = get_connection()
        index = 0
        for disaster_type in intensity_dict.keys():
            cursor = connection.cursor()
            cursor.execute(queries[index])
            index += 1
            for row in cursor:
                key_list = intensity_dict[disaster_type].keys()
                if row[3] == None:
                    continue
                x_axis_value = int(row[3])
                if x_axis_value not in key_list:
                    intensity_dict[disaster_type][x_axis_value] = 1
                else:
                    intensity_dict[disaster_type][x_axis_value] += 1
            cursor.close()
            intensity_dict[disaster_type] = collections.OrderedDict(
                sorted(intensity_dict[disaster_type].items()))
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(intensity_dict)
