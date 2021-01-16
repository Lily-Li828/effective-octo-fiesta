/*
 * home_page.js
 * Wenlai Han, Katrina Li, Lily Li 10 November 2020
 *
 * A bunch of utility functions that could improve user experience with our web pages.
 */

window.onload = initialize;


function initialize() {
    var a = document.getElementsByClassName("words_for_pics");
    for (var i = 0; i < a.length; i++) {
        a[i].style.display = "block";
    }
    if (element) {
        element.onclick = onCatsButton;
    }

}


function toLinechart(num){
   
    sessionStorage.setItem('disaster_type',num);
    sessionStorage.setItem('from_page',1);
    window.location.href="linechart.html";
}


var scrollHeight = document.body.scrollHeight;
var height = window.innerHeight;
var scroll = document.getElementsByClassName("scroll")[0];

window.onscroll = function () {
    var t = document.documentElement.scrollTop || document.body.scrollTop;
    if (scrollHeight - 4 < height + t) {
        scroll.style.display = "none"
    }
    else {
        scroll.style.display = "block"
    }
}

window.onresize = function () {
    height = window.innerHeight;
}


function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onCatsButton() {
    var url = getAPIBaseURL() + '/people_affected_all_countries';

    fetch(url, { method: 'get' })

        .then((response) => response.json())

        .then(function (people_affected_all_countries) {
            var listBody = '';
            for (var k = 0; k < cats.length; k++) {
                var cat = cats[k];
                listBody += '<li>' + cat['name']
                    + ', ' + cat['birth_year']
                    + '-' + cat['death_year']
                    + ', ' + cat['description'];
                + '</li>\n';
            }

            var animalListElement = document.getElementById('animal_list');
            if (animalListElement) {
                animalListElement.innerHTML = listBody;
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
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

