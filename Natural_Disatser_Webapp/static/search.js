/*
 * search.js
 * Wenlai Han, Katrina Li, Lily Li 10 November 2020
 *
 * Script for a search features. Extract information about all disaster
 * events within a year specified by the user and renders that into a HTML
 * using a table.
 * 
 * We didn't use PHP files to store and process the input values, but this
 * could definitely be a future potential advancement to accomplish.
 *
 */
window.onload = initialize;

function initialize() {
    var element = document.getElementById('search-button');
    if (element) {
        element.onclick = getCountryAndDisasterNames();
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}
/*
* This function is used as an alternative way to 
* get user input from the input box instead of 
* using a PHP file.
* 
*/
function getURL() {
    var searchString = window.location.search;
    var year = searchString.slice(-4);
    year = parseInt(year);
    return year;
}

/*
* This function prepares countryNameDictionary and disasterTypeDictionary
* to convert country_id and disaster_type_id that we retrieved from  
* api to actual string representation of country names and disaster types.
* 
*/
function getCountryAndDisasterNames() {
    var url = getAPIBaseURL() + "/country_id_converter";

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (countries) {
            var countryDictionary = countries[0];

            var disaster_url = getAPIBaseURL() + "/disaster_id_converter";

            fetch(disaster_url, { method: 'get' })
                .then((response) => response.json())
                .then(function (disasters) {
                    var disasterTypeDictionary = disasters[0];
                    var year = getURL();
                    buildTable(countryDictionary, disasterTypeDictionary, year);
                })
                .catch(function (error) {
                    console.log(error);
                });
        })
        .catch(function (error) {
            console.log(error);
        });

}

function buildTable(countryDictionary, disasterTypeDictionary, year) {
    var info_url = getAPIBaseURL() + '/natural_disaster_full_info/year/';
    if (year < 1950 || year > 2020 || isNaN(year)) {
        window.alert("Please choose a year from 1950 to 2020 with the format YYYY!");
    } else {
        info_url += "" + year;
        fetch(info_url, { method: 'get' })
            .then((response) => response.json())
            .then(function (yearDisasters) {

                var tableBody = '<tr><th>Year</th><th>Disaster Type</th><th>Country</th><th>Deaths</th><th>Intensity or Magnitude</th></tr>';
                for (var k = 0; k < yearDisasters.length; k++) {
                    var table = yearDisasters[k];
                    //Changing country_id to countryNames that we got from API
                    var countryName = countryDictionary[table['country_id']];
                    table['country_id'] = countryName;
                    //Changing disaster_type_id to disasterName that we got from API
                    var disasterName = disasterTypeDictionary[table['disaster_type_id']];
                    table['disaster_type_id'] = disasterName;
                    tableBody += '<tr>' + '<td>' + table['year']
                        + '</td>' + '<td>' + table['disaster_type_id']
                        + '</td>' + '<td>' + table['country_id']
                        + '</td>' + '<td>' + table['death']
                        + '</td>' + '<td>' + table['intensity_or_magnitude']
                        + '</td>'
                        + '</tr>\n';
                }

                var naturalDisasterFullInfoYearTable = document.getElementById('disaster-table');
                if (naturalDisasterFullInfoYearTable) {
                    naturalDisasterFullInfoYearTable.innerHTML = tableBody;

                }

            })

            .catch(function (error) {
                console.log(error);
            });
    }
}

