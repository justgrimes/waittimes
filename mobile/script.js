var vip = {
	BASE_API_URL : "http://api.votinginfoproject.org/vip/3.0/",
	vipCallback : function(result) {
		var locations = result.locations;
		$("#locations").empty();

		for ( var i = 0; i < locations.length; i++) {
			var location = locations[i];
			var address = location.address;

			var html = "<li><a href='#location'>";
			html += address.location_name;
			if (address.line1 != '') {
				html += "<br>" + address.line1;
			}
			
			if (address.line2 != '') {
				html += ", " + address.line2;
			}


			if (address.city != '') {
				html += ", " + address.city;
			}
			if (address.state != '') {
				html += ", " + address.state;
			}

			if (address.zip != '') {
				html += " " + address.zip;
			}


			html += "</a></li>";
			$("#locations").append(html);
		}

		// Force Listview Redraw
		$("ul").listview("refresh");
		// $.mobile.hidePageLoadingMsg();
	},
	searchFormatted : function(formattedAddress) {
		// var address =
		// "5008%2012th%20St%20S,%20Arlington,%20VA%2022204,%20USA";
		var url = "http://mobile.votinginfoproject.org/electioncenter?jsonp=vip.vipCallback&address="
				+ formattedAddress;

		// $.mobile.showPageLoadingMsg("a", 'Finding Polling Locations');

		var headID = document.getElementsByTagName("head")[0];
		var newScript = document.createElement('script');
		newScript.type = 'text/javascript';
		newScript.src = url;
		headID.appendChild(newScript);
	},
	reverseGeocode : function(input, callback) {
		var geocoder = new google.maps.Geocoder();
		geocoder
				.geocode(
						{
							'address' : input
						},
						function(results, status) {
							if (status == google.maps.GeocoderStatus.OK) {
								var result = results[0];
								if (result) {

									if (result.types[0] != 'street_address') {
										alert("Could Not find a Polling Place.  Please Provide a More specific address.");
									} else {
										var formattedAddress = result.formatted_address;
										console.log(formattedAddress);
										callback(formattedAddress);
									}
								} else {
									alert("No results found");
								}
							} else {
								alert("Could not find the address.");
							}
						});
	}
};

$(function() {
	/*
	 * var house = 4205; var street = '6TH ST S'; var city = 'ARLINGTON'; var
	 * state = 'VA'; var zip = 22204; var url = vip.BASE_API_URL +
	 * "GetPollingLocations2?%24format=json"; url +=
	 * "&key=DF798AA4-C20B-4473-B1B3-9A393CC1BCF3"; url += "&house=" + house +
	 * "&street='" + street + "'&city='" + city + "'&state='" + state +
	 * "'&zip='" + zip +
	 * "'&$expand=Election/State/ElectionAdministration,Locations/PollingLocation/Address,Locations/SourceStreetSegment/NonHouseAddress&onlyUpcoming=false";
	 * console.log(url); $.get(url, function(result) { var locations =
	 * result.d.results.Locations; $("#locations").empty(); for ( var i in
	 * locations) { var location = location[i]; $("#locations").append( "<a
	 * href='#'>" + location.PollingLocation.Name + "</a>"); } });
	 */

	$("#search_form").submit(function() {
		var str = $(this).find("#input_text").val();
		vip.reverseGeocode(str, function(formatted) {
			vip.searchFormatted(formatted);
		});
		return false;
	});

});