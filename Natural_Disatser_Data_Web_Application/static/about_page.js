
/*
 * about_page.js
 * Wenlai Han, Katrina Li, Lily Li, 12 November 2020
 *
 * Script for making about page
 */
window.onload = initialize;

function initialize() {
    var element = document.getElementById('get_data_button');
    showSlides(slideIndex);

    if (element) {
        element.onclick = table;
    }

}


function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function table() {
    var url = getAPIBaseURL() + '/people_affected_all_countries';

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (people_affected_all_countries) {
            var tableBody = '<tr><th>Country</th><th>Year</th><th>People Affected</th></tr>';
            for (var k = 0; k < people_affected_all_countries.length; k++) {
                var table = people_affected_all_countries[k];
                tableBody += '<tr>' + '<td>' + table['country']
                    + '</td>' + '<td>' + table['year']
                    + '</td>' + '<td>' + table['num_people_affected']
                    + '</td>'
                    + '</tr>\n';
            }

            var people_affected_table = document.getElementById('table');
            if (people_affected_table) {
                people_affected_table.innerHTML = tableBody;
            }
        })

        .catch(function (error) {
            console.log(error);
        });
}


// about page picture js script
var slideIndex = 1;

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}
