$(document).ready(function() {
    // Initialize table
    var table = $('#recipe_table').DataTable({
        data : [],
        columns : [ {title : "Recipe"} ]
    });
    $(".recipe-search").keypress(function (e) {
        if (e.which == 13) {
            $.getJSON("/data/recipes/" + $(this).val(), function (recipes) {
                // Destroy table so we can reload data
                table.destroy();
                var data = [];
                $.each(recipes, function(key, row) {
                    data.push([row]);
                });
                table = $('#recipe_table').DataTable({
                    data : data,
                    columns : [ {title : "Recipe"} ]
                });
            });
        }
    });

	// Load ingredients
	$.getJSON('/data/ingredients', function(data_json) {
		console.log(data_json.slice(0,10));		
		var data = [];
		$.each(data_json, function(key, row) {
			data.push([row]);
		});
		console.log(data.slice(0,10));

		var table = $('#ingredient_table').DataTable({
			select: {
	            style: 'single'
	        },
			data : data,
			columns : [ {title : "Ingredient"} ]
		});
		
		table
        .on( 'select', function ( e, dt, type, indexes ) {
            var rowData = table.rows( indexes ).data().toArray();
            //events.prepend( '<div><b>'+type+' selection</b> - '+JSON.stringify( rowData )+'</div>' );
            console.log(rowData);
        } );
		
	});

	
	
	// Load bar chart of water footprint
	var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 420 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

	var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
	var y = d3.scale.linear().range([height, 0]);
	
	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom")
	    //.tickFormat(d3.time.format("%Y-%m"));
	    .ticks(3);
	
	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10);
	
	var svg = d3.select("#barchart_wfp")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", 
	          "translate(" + margin.left + "," + margin.top + ")");
	
	d3.json("/data/wftest", function(error, data) {	
	    data.forEach(function(d) {
	        d.name = d.name;
	        d.value = +d.value;
	    });
		
	  x.domain(data.map(function(d) { return d.name; }));
	  y.domain([0, d3.max(data, function(d) { return d.value; })]);
	
	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)
	    .selectAll("text")
	      .style("text-anchor", "end")
	      .attr("dx", "-.8em")
	      .attr("dy", "-.55em")
	      .attr("transform", "rotate(-90)" );
	
	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("Effect (Units)");
	
	  svg.selectAll("bar")
	      .data(data)
	    .enter().append("rect")
	      .style("fill", "steelblue")
	      .attr("x", function(d) { return x(d.name); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d) { return y(d.value); })
	      .attr("height", function(d) { return height - y(d.value); });
	
	});

	
	
	
	//return false;
});
