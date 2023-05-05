//Get the data from HTML
var stadium_list = JSON.parse(document.getElementById('stadiums').textContent);

//Create and center the map
if(stadium_list.length>0){
    var stadium = stadium_list[0]
    var map = L.map('map').setView([stadium.latitude,stadium.longitude ], 9);
} else {
    var map = L.map('map').setView([47,1], 4);
}
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


//Function to format the markers' descriptions
function format_string(stadium) {
    var str = `<h6><b>${stadium.name}</b></h6>`;
    return str
}


var marker = L.marker([stadium.latitude, stadium.longitude]).addTo(map);
marker.bindPopup(format_string(stadium));
marker.openPopup();











