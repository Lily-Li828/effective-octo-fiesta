/*
 * histogram.js
 * Wenlai Han, Katrina Li, Lily Li, 12 November 2020
 *
 * Script for making histograms from the results of intensity or magnitude of 
 * disaster in the endpoint function
 *
 * Uses the Chartist library: https://gionkunz.github.io/chartist-js/
 * Copyright © 2019 Gion Kunz
 * Free to use under either the WTFPL license or the MIT license.
 *
 */

window.onload = initialize;

function initialize() {
    populateCountrySelector();
}
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}
function populateCountrySelector() {
    // Populate the the drop-down list with the list of states from the API.
    var url = getAPIBaseURL() + '/countries';

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (countries) {
            var countrySelector = document.getElementById('country_name-select');

            if (countrySelector) {
                // Populate it with states from the API
                var countrySelectorBody = '';
                countrySelectorBody += '<option value=\'world\'>World</option>\n'
                for (let key in countries) {

                    countrySelectorBody += '<option value=' + countries[key] + '>' + key + '</option>'
                }
                countrySelector.innerHTML = countrySelectorBody;

                // Set the new-selection handler
                countrySelector.onchange = onCountrySelectorChanged;

                // Start us out looking at World data.
                countrySelector.value = 'world';
                createCountryChart('world', 'world');//need a new version of createCountryChart for the world data
            }

        })
        .catch(function (error) {
            console.log(error);
        });
}

function onCountrySelectorChanged() {
    var countrySelector = document.getElementById('country_name-select');
    if (countrySelector) {
        var countryName = countrySelector.options[countrySelector.selectedIndex].text
        var countryID = countrySelector.value;
        createCountryChart(countryName, countryID);
    }
}

function createCountryChart(countryName, countryID) {
    // Set the title
    var countryTitle = document.getElementById('country-intensity-title');
    if (countryTitle) {
        countryTitle.innerHTML = 'Earthquake Manitude in ' + countryName;
    }

    var countryTitle2 = document.getElementById('country-intensity-title2');
    if (countryTitle2) {
        countryTitle2.innerHTML = 'Maximum Water Height in Tsunami Events in ' + countryName;
    }
    var countryTitle3 = document.getElementById('country-intensity-title3');
    if (countryTitle3) {
        countryTitle3.innerHTML = 'Volcanic Explositivity Index in ' + countryName;
    }
    // Create the chart
    var url = '';
    if (countryID == 'world') {
        url = getAPIBaseURL() + '/country_disaster_intensity/all'; 
        countryTitle.innerHTML = 'Earthquake Manitude across the ' + countryName;
        countryTitle2.innerHTML = 'Maximum Water Height in Tsunami Events across the ' + countryName;
        countryTitle3.innerHTML = 'Volcanic Explositivity Index across the ' + countryName;
    } else {
        url = getAPIBaseURL() + '/country_disaster_intensity/' + countryID;
    }

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (intensities) {
            
            var labels1 = [];
            var labels2 = [];
            var labels3 = [];
            var newIntensityData1 = [];
            var newIntensityData2 = [];
            var newIntensityData3 = [];


            for (let key in intensities) {
                var temp_dictionary = intensities[key];
                for (let key_inner in temp_dictionary) {
                    if (key == 'earthquake') {
                        labels1.push(key_inner);
                        newIntensityData1.push({ meta: key_inner, value: temp_dictionary[key_inner] })
                    } else if (key == "tsunami") {
                        if (key_inner <= 10) {
                            labels2.push(key_inner);
                            newIntensityData2.push({ meta: key_inner, value: temp_dictionary[key_inner] })
                        }
                        continue;
                    } else {
                        labels3.push(key_inner);
                        newIntensityData3.push({ meta: key_inner, value: temp_dictionary[key_inner] })
                    }
                }
            }
            var options = {
                seriesBarDistance: 1,
                onlyInteger: true,
                scaleMinSpace: 20
            };
        
            var data1 = { labels: labels1, series: [newIntensityData1] };
            var data2 = { labels: labels2, series: [newIntensityData2] };
            var data3 = { labels: labels3, series: [newIntensityData3] };
            var result_print1 = document.getElementById('country-intensity-chart');
            var result_print2 = document.getElementById('country-intensity-chart2');
            var result_print3 = document.getElementById('country-intensity-chart3');
            
            // Finally, we create the bar chart, and attach it to the desired <div> in our HTML.
            if (newIntensityData1.length > 0) {
                var chart = new Chartist.Bar('#country-intensity-chart', data1, options);
                result_print1.innerHTML = ''
            } else {
                if (result_print1) {
                    result_print1.innerHTML = "<h4>Data Not Avaliable</h4>"
                }
            }
            if (newIntensityData2.length > 0) {
                var chart = new Chartist.Bar('#country-intensity-chart2', data2, options);
                result_print2.innerHTML = ''
            } else {
                if (result_print2) {
                    result_print2.innerHTML = "<h4>Data Not Avaliable</h4>"
                }
            }
            if (newIntensityData3.length > 0) {
                var chart = new Chartist.Bar('#country-intensity-chart3', data3, options);
                result_print3.innerHTML = ''
            } else {
                if (result_print3) {
                    result_print3.innerHTML = "<h4>Data Not Avaliable</h4>"
                }
            }


           
            
        })

        // Log the error if anything went wrong during the fetch.
        .catch(function (error) {
            console.log(error);
        });
}