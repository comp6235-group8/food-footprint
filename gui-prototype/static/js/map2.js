/*var format = function(d) {
    d = d;
    return d3.format(',.02f')(d);
}*/

var preprocessCountryData = function(data){
  // Pre-processing WFP data per country
  data.forEach(function(country){
    // Create Code-Id (Alpha3)
    if (countryCodeMapping[country.country]){
      country.countryCode = countryCodeMapping[country.country];
    }else{
      //console.log("No country code for:" + country.country);
      country.countryCode = "";
    }

    // Calculate the sum of the individual footprints
    // TOTAL is the column used to apply the color by country
    // TOTAL should be a String. This is how d3-geomaps works.
    country["total"] = "";
    var wfp = country["water_footprint_country_average"];
    if (wfp && (wfp.blue || wfp.green || wfp.grey)){
      var total = 0;
      ["blue", "green", "grey"].forEach( function(color){
        if (wfp[color]){
          total = total + wfp[color];
        }
      });
      country["total"] = ""+total;
    }
  });
}

var queryAggregatedWFPbyCountry = function(cb) {
	d3.json('http://localhost:5000/data/globalwaterfootprintbycountry', function(error, data) {
	  if (!data){ 
	    console.log("No data returned!"); 
	    return;
	  }
	  
	  preprocessCountryData(data);

	  cb(data);
	});
}

var findUpdatedCountry = function(data, countryCode){
	for (var i = 0; i < data.length; i++) {
		var country = data[i];
		if (country.countryCode === countryCode){
			return country;
		}
	}

	return null;
}

var updateWFPMap = function(ingredient, recipe, cb) {
	data = d3.select('#map').datum();

	var request = '/data/ingredient/waterfootprint/'+ingredient;
	if(recipe){
		request = '/data/recipe/waterfootprintpercountry/'+recipe;
	}  

	d3.json(request, function(error, newData) {
	  //console.log( newData.slice(0,10));
	  if ( !((newData && newData.countries) ||  (typeof newData !== 'undefined' && newData.length > 0))) {
		// NO DATA
	  	console.log("No data returned for ingredient: " + ingredient);

	  	// Remove previous data
	  	data.forEach(function(country, index){
		    // Calculate the sum of the individual footprints
		    country["total"] = "";
		    country["water_footprint_country_average"] = null;
		}); 
	  }else{
		  // DATA
		  if (newData.countries){
		  	newData = newData.countries;
		  }
		  preprocessCountryData(newData);

		  data.forEach(function(country, index){
		  	updated = findUpdatedCountry(newData, country["countryCode"]);
		    country["total"] = updated["total"];
		    country["water_footprint_country_average"] = updated["water_footprint_country_average"];
		  });
	  }

	  cb(data);
	});
}


var findCountryById = function(id){
	var data = d3.select('#map').datum();
	
	for (var i = 0; i < data.length; i++) {
		if(data[i].countryCode === id){
			//console.log("Found: " + data[i].country);
			return data[i];
		}
	}

	return null;
}

var noMethod = function(d){
	console.log(d);
}

var mouseMoveMethod = function(d, coordinates){
	var country = findCountryById(d.id);
	
	if (country){
		var total = "NA";	
		var blue = "NA";
		var green = "NA";
		var grey = "NA";
		var format = d3.format(',.02f');

		if(country.total){
			total = format(+country.total);
		}

		if(country["water_footprint_country_average"]){
			if (country["water_footprint_country_average"]["blue"]){
				blue = format(+country["water_footprint_country_average"]["blue"]);

			}
			if (country["water_footprint_country_average"]["green"]){
				green = format(+country["water_footprint_country_average"]["green"]);
			}
			if (country["water_footprint_country_average"]["grey"]){
				grey = format(+country["water_footprint_country_average"]["grey"]);
			}
		}

        var html = "";
        html += "<div class=\"tooltip_kv\">";
        html += "<span class=\"tooltip_key\">";
        html += country.country;
        html += "</span>";
        html += "<span class=\"tooltip_value\">";
        html += "<b>";
        html += total + " m<sup>3</sup>";
        html += "</b>";
        html += "";
        html += "</span>";
        html += "<div>";
        html += "Green footprint: ";
        html += "<span class=\"tooltip_value\">";
        html += green  + " m<sup>3</sup>";
        html += "";
        html += "</span>";
        html += "</div>";
        html += "<div>";
        html += "Blue footprint: ";
        html += "<span class=\"tooltip_value\">";
        html += blue + " m<sup>3</sup>";
        html += "";
        html += "</span>";
        html += "</div>";
        html += "<div>";
        html += "Grey footprint: ";
        html += "<span class=\"tooltip_value\">";
        html += grey + " m<sup>3</sup>";
        html += "";
        html += "</span>";
        html += "</div>";
        html += "</div>";

        $("#tooltip-container").html(html);
        //$(this).attr("fill-opacity", "0.8");
        $("#tooltip-container").show();

        //var coordinates = d3.mouse(this);
        //console.log(coordinates);

        //var map_width = $('.choropleth')[0].getBoundingClientRect().width;945
        var map_width = $('.background')[0].width;
        //var map_width = 945;

        if (d3.event.pageX < map_width / 2) {
            d3.select("#tooltip-container")
                .style("top", (d3.event.layerY + 15) + "px")
                .style("left", (d3.event.layerX + 15) + "px");
        } else {
            var tooltip_width = $("#tooltip-container").width();
            d3.select("#tooltip-container")
                .style("top", (d3.event.layerY + 15) + "px")
                .style("left", (d3.event.layerX - tooltip_width - 30) + "px");
        }
	}

}

var mouseOutMethod = function(d){
	//$(this).attr("fill-opacity", "1.0");
	$("#tooltip-container").hide();
}


var initMap = function (){
	var width = 950;
	var height = 500;

	var map = d3.geomap.choropleth()
		.width(width)
		.scale(200)
		.rotate([-10,0,0])
		.translate([(width/2), (height/2)+40])
	    .geofile('/static/geojson/countries.json')
	    .colors(colorbrewer.YlOrRd[9])
	    .column('total')
	    .format(d3.format(',.02f'))
	    .legend(true)
	    .unitId('countryCode')
	    .mouseMoveMethod(mouseMoveMethod)
	    .mouseOutMethod(mouseOutMethod)
	    ;

	queryAggregatedWFPbyCountry(function(data){
		d3.select('#map')
			.datum(data)
			.call(map.draw, map);

	});

	return map;
}