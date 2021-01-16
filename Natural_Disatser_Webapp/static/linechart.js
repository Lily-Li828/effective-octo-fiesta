/*
 * linechart.js
 * Wenlai Han, Katrina Li, Lily Li 10 November 2020
 *
 * 
 * Script for building a linechart from Chartist library.
 * Each line in this linechart consists of numbers of cumulative cases of a type 
 * of disaster of one country. This linechart can take up to three lines.
 * This script takes results from get_cumulative_country_cases endpoint
 * and arrange data to draw lines in chart.
 *
 * Uses the Chartist library: https://gionkunz.github.io/chartist-js/
 * Copyright © 2019 Gion Kunz
 * Free to use under either the WTFPL license or the MIT license.
 */

window.onload = initialize;

function initialize() {
    populateCountrySelector();
    var element = document.getElementById('search-button');

    if (element) {
        element.onclick = buildTable();
    }
}
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}




function populateCountrySelector() {
    // Populate the the drop-down list with the lists of countries from the API.
    var url = getAPIBaseURL() + '/countries';

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (countries) {
            var countrySelector = document.getElementById('country1');
            var countrySelector1 = document.getElementById('country2');
            var countrySelector2 = document.getElementById('country3');
            if (countrySelector) {
                // Populate it with countries from the API
                var countrySelectorBody = '';

                for (let key in countries) {
                    countrySelectorBody += '<option value=' + countries[key] + '>' + key + '</option>';
                }
                countrySelector.innerHTML = '<option value="0"></option>' + countrySelectorBody;
                countrySelector1.innerHTML = '<option value="0"></option>' + countrySelectorBody;
                countrySelector2.innerHTML = '<option value="0"></option>' + countrySelectorBody;

            }

        })
        .catch(function (error) {
            console.log(error);
        });
}

var from_link = sessionStorage.getItem('disaster_type');
var from_page = sessionStorage.getItem('from_page');

if (from_page==1){

    if(from_link==0){

        createCountryChart('http://localhost:5000/api/cumulative_country_cases/1',"1",'Japan','109','',"0",'',"0");
    }

    if(from_link==1){

        createCountryChart('http://localhost:5000/api/cumulative_country_cases/0',"0",'United States','223','',"0",'',"0");

    }

    if(from_link==2){

        createCountryChart('http://localhost:5000/api/cumulative_country_cases/2',"2",'Chile','42','',"0",'',"0");

    }
    
    sessionStorage.setItem('from_page',5);

}



function submitClicked() {
    
    var disasterTypeSelector = document.getElementById('disaster-type');
    var url = getAPIBaseURL();
    if (disasterTypeSelector && disasterTypeSelector.value != "----- Type -----") {
        var disasterTypeId = disasterTypeSelector.value;
        url += "/cumulative_country_cases/" + disasterTypeId;
        console.log(url);
    } else { // did not specify disaster type
        window.alert("Please select a disaster type!");
    }
    var countryName1 = '';
    var countryID1 = '';
    var countryName2 = '';
    var countryID2 = '';
    var countryName3 = '';
    var countryID3 = '';

    var countrySelector1 = document.getElementById('country1');
    if (countrySelector1) {
        countryName1 = countrySelector1.options[countrySelector1.selectedIndex].text;
        countryID1 = countrySelector1.value;
    }
    var countrySelector2 = document.getElementById('country2');
    if (countrySelector2) {
        countryName2 = countrySelector2.options[countrySelector2.selectedIndex].text;
        countryID2 = countrySelector2.value;
    }
    var countrySelector3 = document.getElementById('country3');
    if (countrySelector3) {
        countryName3 = countrySelector3.options[countrySelector3.selectedIndex].text;
        countryID3 = countrySelector3.value;
    }

    createCountryChart(url, disasterTypeId,countryName1, countryID1, countryName2, countryID2, countryName3, countryID3);
}



function countCases(cases) {
    // A helper function that changes form like this:
    // [{1970: 10},{1971:25},{1972:45}]
    // to this:
    // [10,25,45,...]
    caseCounts = [];
    for (var k = 0; k < cases.length; k++) {
        var temp_dictionary = cases[k];
        var label = Object.keys(temp_dictionary)[0];
        caseCounts.push(temp_dictionary[label]);
    }
    return caseCounts;
}

function createCountryChart(baseURL, disasterType_Id, countryName1, countryID1, countryName2, countryID2, countryName3, countryID3) {
    // This is where we actually draw the chart


    // Set the title
    var disaster_type = "Natural Disasters";
    if(disasterType_Id="0"){

        disaster_type = "Earthquake";

    }

    if(disasterType_Id="1"){

        disaster_type = "Tsunami";

    }

    if(disasterType_Id="2"){

        disaster_type = "Volcanic Eruptions";

    }

    var countryTitle = document.getElementById('disaster-comparsion-title');
    if (countryTitle) {
        countryTitle.innerHTML = 'Cumulative '+disaster_type+' Case Counts in:<br> ' + countryName1 + "&nbsp &nbsp " + countryName2 + " &nbsp &nbsp  " + countryName3;
    }
    var labels = [];
    var caseCounts1 = [];
    var caseCounts2 = [];
    var caseCounts3 = [];
    // Create the chart


    //options is the third parameter of Chartist.Line()
    var options = {
        seriesBarDistance: 1,
        axisX: {
            labelInterpolationFnc: function (value, index) {
                return index % 5 === 0 ? value : null;
            }
        },
        chartPadding: {
            right: 40
        },

        // We FAILED to implement this, 
        // (but we DID find an alternative way),
        // keep it here for future development: 
        // plugins: [ 
        //     Chartist.plugins.legend({
        //         position: 'bottom'
        //     })
        // ]
    };


    if (countryID1 == "0") { //Did not select country 1
        window.alert("Please select a starting country!");
        // still needs an empty chart to cover the last result from 'submit'
        var chart = new Chartist.Line('#disaster-comparsion-chart', {}, options);
    }
    else { //Did select country 1
        var url1 = baseURL + '/' + countryID1;
        fetch(url1, { method: 'get' })
            .then((response) => response.json())
            .then(function (cases) {
                caseCounts1 = countCases(cases);

                if (countryID2 != "0") { // user wants at least country 1 and 2
                    var url2 = baseURL + '/' + countryID2;
                    fetch(url2, { method: 'get' })
                        .then((response) => response.json())
                        .then(function (cases2) {
                            caseCounts2 = countCases(cases2);


                            if (countryID3 != "0") { //user clearly wants three countries
                                var url3 = baseURL + '/' + countryID3;
                                fetch(url3, { method: 'get' })
                                    .then((response) => response.json())
                                    .then(function (cases3) {
                                        caseCounts3 = countCases(cases3);

                                        var data = {
                                            labels: labels,
                                            series: [
                                                { data: caseCounts1 },
                                                { data: caseCounts2 },
                                                { data: caseCounts3 }
                                            ]
                                        }
                                        // Finally, we create the bar chart, and attach it to the desired <div> in our HTML.
                                        var chart = new Chartist.Line('#disaster-comparsion-chart', data, options);
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                    });
                            }
                            else { // if only country1 and country2 selected
                                var data = {
                                    labels: labels,
                                    series: [
                                        { data: caseCounts1 },
                                        { data: caseCounts2 }
                                    ]
                                }
                                var chart = new Chartist.Line('#disaster-comparsion-chart', data, options);
                            }
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                }
                else {// if no country 2
                    if (countryID3 != "0") {// if user has country 1, skips 2 and has 3
                        countryTitle.innerHTML = 'Cumulative Natural Disasters Case Count in ' + countryName1;
                        alert("Please fill Country Two first! The following result would only show for Country One.");
                    }
                    var data = {
                        labels: labels,
                        series: [
                            { data: caseCounts1 }
                        ]
                    }
                    var chart = new Chartist.Line('#disaster-comparsion-chart', data, options);
                }


            })
            // Log the error if anything went wrong during the fetch.
            .catch(function (error) {
                console.log(error);
            });
    }


}

