// A $( document ).ready() block.
$(document).ready(function() {
  
  // pickup location is a valid string?
  function getDimensions(pickup_location) {
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

  $('#createDonationForm').submit(function() {
    var is_valid_location = false;
    var dimensions = getDimensions($("#pickup_location").val());
    if (dimensions.length > 0) {
      $("#lat").val(dimensions[0]);
      $("#lng").val(dimensions[1]);
      is_valid_location = true;
    }
    else {
      alert("Please enter a valid location and resubmit the form.");
    }
    return is_valid_location;
  });


});
