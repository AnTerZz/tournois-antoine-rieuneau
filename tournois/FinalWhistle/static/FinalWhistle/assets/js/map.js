var stadium_list = JSON.parse(document.getElementById('stadiums').textContent);

var game_element = document.getElementById('games')
if(game_element){
    var game_list = JSON.parse(game_element.textContent);
} else {
    var game_list = []
}


if(stadium_list.length>0){
    var map = L.map('map').setView([stadium_list[0].latitude,stadium_list[0].longitude ], 9);
} else {
    var map = L.map('map').setView([47,1], 4);
}

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function format_string(stadium) {
    var str = `<h6><b>${stadium.name}</b></h6>`
    str += "<ul>"
    for(const game of game_list){
        if(game.stadium==stadium.id){
            str += `<li>${game.home_team__name} vs ${game.away_team__name}</li>`
        }
    }
    str += "</ul>"
    return str
}

var marker_list = []
for(const stadium of stadium_list){
    var marker = L.marker([stadium.latitude, stadium.longitude]).addTo(map);
    marker.bindPopup(format_string(stadium));
    marker_list.push(marker)
    console.log([stadium.latitude, stadium.longitude])
}

if(marker_list.length>1){
    var group = new L.featureGroup(marker_list);
    map.fitBounds(group.getBounds().pad(0.05));
} else {
    marker.openPopup();
}






