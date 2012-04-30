var vip = {
	locations : [],
	location : undefined,
	BASE_API_URL : "http://api.votinginfoproject.org/vip/3.0/",
	locationSelected : function(idx) {
		vip.location = vip.locations[idx];

		var locationId = vip.location.id;
		console.log("locationId" + locationId);

		/*
		 * var url = "http://10.166.23.96:8080/location";
		 * 
		 * var data = { apikey : 1, locationId : locationId, limit : 300 };
		 * 
		 * $.post(url, data, function(result) { console.log(result); }, "json");
		 */
		
		$(".location-name").text(vip.location.address.location_name);

		window.location = "#location";

//		alert('loading: ' + JSON.stringify(vip.location));
	},
	addListClickListeners : function() {
		$("ul#locations a").click(function(e) {
			e.preventDefault();
			var idx = $(this).attr("idx");
			console.log("index: " + idx);
			vip.locationSelected(idx);
			return false;
		});
	},
	vipCallback : function(result) {
		vip.locations = result.locations;
		$("#locations").empty();

		for ( var i = 0; i < vip.locations.length; i++) {
			var location = vip.locations[i];
			var address = location.address;

			var html = "<li><a href='#location' idx='" + i + "'>";
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
		$("ul#locations").listview('refresh');
		vip.addListClickListeners();
	},
	searchFormatted : function(formattedAddress) {
		var url = "http://mobile.votinginfoproject.org/electioncenter?jsonp=vip.vipCallback&address="
				+ formattedAddress;

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
	$("#search_form").submit(function() {
		var str = $(this).find("#input_text").val();
		vip.reverseGeocode(str, function(formatted) {
			vip.searchFormatted(formatted);
		});
		return false;
	});
});