var stadium_list = JSON.parse(document.getElementById('stadiums').textContent);
var map = L.map('map').setView([stadium_list[0].latitude,stadium_list[0].longitude ], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
for(const stadium of stadium_list){
    var marker = L.marker([stadium.latitude, stadium.longitude]).addTo(map);
    marker.bindPopup(`<b>${stadium.name}</b>`).openPopup();
    console.log([stadium.latitude, stadium.longitude])
}



