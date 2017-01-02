/*var format = function(d) {
    d = d;
    return d3.format(',.02f')(d);
}*/

var queryAggregatedWFPbyCountry = function(cb) {
	d3.json('http://localhost:5000/data/globalwaterfootprintbycountry', function(error, data) {
	  if (!data){ 
	    console.log("No data returned!"); 
	    return;
	  }
	  
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
	    country["total"] = null;
	    if (country["water_footprint_country_average"]){
	      var total = 0;
	      var colors = ["blue", "green", "grey"];
	      for (var i = 0; i < colors.length; i++) {
	        if (country["water_footprint_country_average"][colors[i]]){
	          total = total + country["water_footprint_country_average"][colors[i]];
	        }
	      }
	      country["total"] = ""+total;
	    }
	  });

	  //data.forEach(function (country) {
	  //  if (country["country"] === "Ecuador"){
	  //    console.log(country);
	  //  }
	  //});

	  cb(data);
	});
}

var updateWFPMap = function(ingredient, cb) {
	data = d3.select('#map').datum();

	d3.json('http://localhost:5000/data/ingredient/waterfootprint/'+ingredient, function(error, newData) {
	  if (!newData){ console.log("No data returned for ingredient: " + ingredient); return; }
	  newData = newData.countries;

	  data.forEach(function(country, index){
	  	//console.log(i); console.log(country); console.log(newData[i]); return;

	    // Calculate the sum of the individual footprints
	    country["total"] = null;
	    if (newData[index]["water_footprint_country_average"]){
	      var total = 0;
	      var colors = ["blue", "green", "grey"];
	      for (var i = 0; i < colors.length; i++) {
	        if (newData[index]["water_footprint_country_average"][colors[i]]){
	          total = total + newData[index]["water_footprint_country_average"][colors[i]];
	        }
	      }
	      country["total"] = ""+total;
	    }

	    //console.log(index); console.log(country); console.log(newData[i]); return;
	  });

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
		var blue = "NA";
		var green = "NA";
		var grey = "NA";
		var format = d3.format(',.02f');

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
        html += format(country.total)  + " m<sup>3</sup>";
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
	var width = 945;
	var height = 492;

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