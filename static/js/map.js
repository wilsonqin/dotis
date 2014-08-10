
// A $( document ).ready() block.
$(document).ready(function() {

  // pickup location is a valid string?
  function getDimensions(pickup_location) {
    console.log(pickup_location);
    var address_array = []
    pickup_location.split(",").forEach(function (index) {
          address_array.push(index.split(" ").join("+"));
        });
    var address_str = address_array.join(",");

    var results = []
    $.ajax({
      type: "GET",
      async:false,
      url: "https://maps.googleapis.com/maps/api/geocode/json",
      data: { address: address_str }
      })
      .done(function( data ) {
        if(data["results"].length > 0){   
          //this array is not empty 
          results.push(data["results"][0].geometry.location.lat);
          results.push(data["results"][0].geometry.location.lng);
        }
      });
    return results;  
  }

  $('#map-btn').click(function() {
    var is_valid_location = false;
    var dimensions = getDimensions($('#map_search').val());
    console.log(dimensions);

    if (dimensions.length > 0) {
      lat = dimensions[0];
      lng = dimensions[1];
      radius = $("#map_radius").val();

      $.ajax({
      type: "GET",
      async:false,
      url: "/getDonations",
      data: { radius: radius, lat: lat, lng: lng }
      })
      .done(function( data ) {
        console.log(data);
      });
    }
  });


  // renderMap();

  
  
  // function renderMap() {
    var map;
    var donationSites = [];
    var donationCoords = [];
    var siteListeners = [];
    var siteClicked = [];
    var siteStyles = [];
    var testNum = 10;
    for (var i = 0; i < testNum; i++) {
      donationCoords.push({id: i, location: new google.maps.LatLng(42.358 + 0.1*Math.random() - 0.05, -71.059 + 0.1*Math.random() - 0.05)})
    };

    for (var i = donationCoords.length - 1; i >= 0; i--) {
      siteClicked.push({id: i, state: false})
    };

    for (var i = donationCoords.length - 1; i >= 0; i--) {
      siteStyles.push(
        new StyledIcon(StyledIconTypes.MARKER,{color:"ff0000"})
        )
    };

    google.maps.event.addDomListener(window, 'load', initialize);
  // }

  function initialize() {
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(42.358, -71.059 )
      }
      map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

      for (var i = donationCoords.length - 1; i >= 0; i--) {
        donationSites.push(
          new StyledMarker({
            styleIcon: siteStyles[i],
            position: donationCoords[i].location,
            map: map
          })
        )
      };

      function createfunc(i) {
        return function() { 
                  siteClicked[i].state = ! siteClicked[i].state;
                  if (siteStyles[i].color == "ff0000") {
                    siteStyles[i].set("color", "0000ff");
                  } else if (siteStyles[i].color == "0000ff") {
                    siteStyles[i].set("color", "ff0000");
                  };
                  // alert(" Is site " + donationCoords[i].id + " selected? " + siteClicked[i].state
                  // ); 
                };
      }

      for (var i = donationSites.length - 1; i >= 0; i--) {
        siteListeners.push(createfunc(i));
      }  

      for (var i = donationSites.length - 1; i >= 0; i--) {
        google.maps.event.addListener(donationSites[i], 'click', siteListeners[i]);
      }  

    }  


  
 

});


