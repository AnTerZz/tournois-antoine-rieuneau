var stadium_list = JSON.parse(document.getElementById('stadiums').textContent);
if(stadium_list.length>0){
    var map = L.map('map').setView([stadium_list[0].latitude,stadium_list[0].longitude ], 9);
} else {
    var map = L.map('map').setView([47,1], 4);
}

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
for(const stadium of stadium_list){
    var marker = L.marker([stadium.latitude, stadium.longitude]).addTo(map);
    marker.bindPopup(`<b>${stadium.name}</b>`).openPopup();
    console.log([stadium.latitude, stadium.longitude])
}



