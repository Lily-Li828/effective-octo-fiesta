/*
 * home_page.js
 * Wenlai Han, Katrina Li, Lily Li 10 November 2020
 *
 * A bunch of utility functions that could improve user experience with our web pages.
 */
window.onload = function () {
    var a = document.getElementsByClassName("words_for_pics");
    for (var i = 0; i < a.length; i++) {
        a[i].style.display = "block";
    }
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

