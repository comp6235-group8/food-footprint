/*var format = function(d) {
    d = d;
    return d3.format(',.02f')(d);
}*/

var queryWFPbyIngredient = function(ingredient, cb) {
	d3.json('http://localhost:5000/data/ingredient/waterfootprint/' + ingredient, function(error, data) {
	  if (!data){ 
	    console.log("No data returned for ingredient: " + ingredient); 
	    return;
	  }
	  
	  data = data.countries;

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

var updateWFPMap = function(ingredient, data, cb) {
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



var initMap = function (){
	var map = d3.geomap.choropleth()
		.width(945)
		.scale(220)
		.rotate([-10,0,0])
	    .geofile('/static/geojson/countries.json')
	    .colors(colorbrewer.YlOrRd[9])
	    .column('total')
	    .format(d3.format(',.02f'))
	    .legend(true)
	    .unitId('countryCode');

	queryWFPbyIngredient('wheat', function(data){
		d3.select('#canvas-svg')
			.datum(data)
			.call(map.draw, map);

	});

}