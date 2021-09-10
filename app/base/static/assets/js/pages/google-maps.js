'use strict';
$(document).ready(function() {
    var basic;
    basic = new GMaps({
        el: '#basic-map',
        lat: 21.217319,
        lng: 72.866472,
        scrollwheel: false
    });
    var map;
    map = new GMaps({
        el: '#markers-map',
        lat: 21.2334329,
        lng: 72.866472,
        scrollwheel: false
    });
    map.addMarker({
        lat: 21.2334329,
        lng: 72.866472,
        title: 'Marker with InfoWindow',
        infoWindow: {
            content: '<p><Phoenicoded></Phoenicoded> <br/> Buy Now at <a href="">Themeforest</a></p>'
        }
    });
    var mapOverlay;
    mapOverlay = new GMaps({
        el: '#mapOverlay',
        lat: 21.2334329,
        lng: 72.866472,
        scrollwheel: false
    });
    mapOverlay.drawOverlay({
        lat: 21.2334329,
        lng: 72.866472,
        content: '<div class="overlay">Address</div>'
    });
    var mapGeo = new GMaps({
        div: '#mapGeo',
        lat: 21.2334329,
        lng: 72.866472
    });
    $('#geocoding_form').submit(function(e) {
        e.preventDefault();
        GMaps.geocode({
            address: $('#address').val().trim(),
            callback: function(results, status) {
                if (status == 'OK') {
                    var latlng = results[0].geometry.location;
                    mapGeo.setCenter(latlng.lat(), latlng.lng());
                    mapGeo.addMarker({
                        lat: latlng.lat(),
                        lng: latlng.lng()
                    });
                }
            }
        });
    });
    var panorama;
    panorama = GMaps.createPanorama({
        el: '#mapStreet',
        lat: 42.3455,
        lng: -71.0983
    });
    var mapT;
    mapT = new GMaps({
        div: '#mapTypes',
        lat: 21.2334329,
        lng: 72.866472,
        mapTypeControlOptions: {
            mapTypeIds: ["hybrid", "roadmap", "satellite", "terrain", "osm"]
        }
    });
    mapT.addMapType("osm", {
        getTileUrl: function(coord, zoom) {
            return "https://a.tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
        },
        tileSize: new google.maps.Size(256, 256),
        name: "OpenStreetMap",
        maxZoom: 18
    });
    mapT.setMapTypeId("osm");
    var georssmap = new google.maps.Map(document.getElementById('georssmap'), {
        zoom: 4,
        center: {
            lat: 21.2334329,
            lng: 72.866472
        }
    });
    var georssLayer = new google.maps.KmlLayer({
        url: 'http://api.flickr.com/services/feeds/geo/?g=322338@N20&lang=en-us&format=feed-georss'
    });
    georssLayer.setMap(georssmap);
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: {
            lat: 21.2334329,
            lng: 72.866472
        }
    });
    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var markers = locations.map(function(location, i) {
        return new google.maps.Marker({
            position: location,
            label: labels[i % labels.length]
        });
    });
    var markerCluster = new MarkerClusterer(map, markers, {
        imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
    });
});
var locations = [{
    lat: 21.1702401,
    lng: 72.8310607
}, {
    lat: 21.128143,
    lng: 79.125618
}, {
    lat: 22.451530,
    lng: 88.399818
}, {
    lat: 20.264774,
    lng: 73.508148
}, {
    lat: 23.080135,
    lng: 72.572174
}, {
    lat: 22.835373,
    lng: 88.360992
}, {
    lat: 29.280394,
    lng: 78.831718
}, {
    lat: 9.907271,
    lng: 78.094429
}, {
    lat: 26.903660,
    lng: 78.514259
}, {
    lat: 19.062054,
    lng: 72.883438
}, {
    lat: 11.235264,
    lng: 78.858414
}, {
    lat: 23.302189,
    lng: 81.356804
}, {
    lat: 12.695032,
    lng: 78.621887
}, {
    lat: 22.511976,
    lng: 88.250992
}, {
    lat: 23.125587,
    lng: 88.546867
}, {
    lat: 21.164993,
    lng: 81.775307
}, {
    lat: 21.779188,
    lng: 87.744629
}, {
    lat: 25.416676,
    lng: 86.129379
}, {
    lat: 15.478569,
    lng: 78.483093
}, {
    lat: 13.340881,
    lng: 74.742142
}, {
    lat: 17.143908,
    lng: 79.623924
}]
