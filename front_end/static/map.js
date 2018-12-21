var title = $('#title').data()["name"];
var address = $('#address').data()["name"];
var description = $('#description').data()["name"];

map = new GMaps({
    div: '#map'
});


GMaps.geocode({
    address: address,
    callback: function(results, status) {
        if (status == 'OK') {
            latlng = results[0].geometry.location;
            map.addMarker({
                lat: latlng.lat(),
                lng: latlng.lng(),
                title: title,
                infoWindow: {
                    content: '<h4>' + title + '</h4><div>' + description + '</div>',
                    maxWidth: 200
                }
            })
            map.setCenter(latlng.lat(), latlng.lng());
        } else if (status == 'ZERO_RESULTS') {
            alert('Sorry, no results found');
        }
    }
});


GMaps.geolocate({
    success: function(position) {
        map.addMarker({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            title: 'My location',
            infoWindow: {
                content: 'my location',
                maxWidth: 200
            }
        })
    },
    error: function(error) {
        alert('Geolocation failed: ' + error.message);
    },
    not_supported: function() {
        alert("Your browser does not support geolocation");
    },
    always: function() {
        // alert("Always");
    }
});