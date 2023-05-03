//Get the data from HTML
var stadium_list = JSON.parse(document.getElementById('stadiums').textContent);

var stadium_array = {}
for(const stadium of stadium_list){
    stadium_array[`Stadium ${stadium.id}`] = stadium;
}


var game_element = document.getElementById('games')
if(game_element){
    var game_list = JSON.parse(game_element.textContent);
} else {
    var game_list = []
}


//Sorting of the games by stadium and by poule
var game_by_poule_stadium = {}
var game_by_stadium = {}

for(const game of game_list){
    var poule_key = `Poule ${game.poule__number}`;
    var stadium_key = `Stadium ${game.stadium}`;
   
    if(!(poule_key in game_by_poule_stadium)){
        game_by_poule_stadium[poule_key] = {};
        game_by_poule_stadium[poule_key][stadium_key] = [game]
    } else {
        if(!(stadium_key in game_by_poule_stadium[poule_key])){
            game_by_poule_stadium[poule_key][stadium_key] = [game]
        } else { 
            game_by_poule_stadium[poule_key][stadium_key].push(game);
        }
    }
/*
    if(!(stadium_key in game_by_stadium)){
        game_by_stadium[stadium_key] = [game];
    } else {
        game_by_stadium[stadium_key].push(game);
    }*/
} 


//Create and center the map
if(stadium_list.length>0){
    var map = L.map('map').setView([stadium_list[0].latitude,stadium_list[0].longitude ], 9);
} else {
    var map = L.map('map').setView([47,1], 4);
}
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


//Function to format the markers' descriptions
function format_string(stadium, game_list) {
    var str = `<h6><b>${stadium.name}</b></h6>`;
    str += "<ul>";
    for(const game of game_list){
        if(game.stadium==stadium.id){
            str += `<li>${game.home_team__name} vs ${game.away_team__name}</li>`;
        }
    }
    str += "</ul>";
    return str
}


//Create the markers for each poule
var markers_by_poule = {};
for(const poule in game_by_poule_stadium){
    for(const stadium_key in game_by_poule_stadium[poule]){
        const stadium = stadium_array[stadium_key];
        var marker = L.marker([stadium.latitude, stadium.longitude]);
        marker.bindPopup(format_string(stadium, game_by_poule_stadium[poule][stadium_key]));

        if(!(poule in markers_by_poule)){
            markers_by_poule[poule] = [marker];
        } else {
            markers_by_poule[poule].push(marker);
        }
    }
}

//Create all the markers
var marker_list = []
for(const stadium of stadium_list){
    var marker = L.marker([stadium.latitude, stadium.longitude])    ;
    marker.bindPopup(format_string(stadium, game_list));
    marker_list.push(marker);
}


//Center the map to display all markers
var all_markers = new L.featureGroup(marker_list).addTo(map);
if(marker_list.length>1){
    map.fitBounds(all_markers.getBounds().pad(0.05));
} else {
    marker.openPopup();
}

//Create layer group for each poule
var overlayMaps = {"Toutes poules":all_markers};
for(const poule in markers_by_poule){
    overlayMaps[poule] = L.layerGroup(markers_by_poule[poule]);
}
var layerControl = L.control.layers(null,overlayMaps).addTo(map);









