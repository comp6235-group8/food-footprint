//Simple d3.js barchart example to illustrate d3 selections
//other good related tutorials
//http://www.recursion.org/d3-for-mere-mortals/
//http://mbostock.github.com/d3/tutorial/bar-1.html
//Object with the basic properties of the barchart

//Useful links:
//https://bl.ocks.org/d3noob/7030f35b72de721622b8
//https://bost.ocks.org/mike/bar/3/
//http://bl.ocks.org/enjalot/1429426

// Function that defines the basic properties (size, margin) of the bar chart
function gwfBasics() {
  var margin = {
    top: 10,
    right: 10,
    bottom: 30,
    left: 50
  },
  width = 270 - margin.left - margin.right,
  height = 311 - margin.top - margin.bottom,
  colorBar = d3.scale.category20(),
  barPadding = 1;
  return {
    margin: margin,
    width: width,
    height: height,
    colorBar: colorBar,
    barPadding: barPadding
  };
}

// Creates / updates the barchart based on the new data
function updateBarChartGWF(data){
    // console.log(data);

    // Load basic properties
    var basics = gwfBasics();

    var margin = basics.margin,
    width = basics.width,
    height = basics.height,
    colorBar = basics.colorBar,
    barPadding = basics.barPadding;

    //nice breakdown of d3 scales
    //http://www.jeromecukier.net/blog/2011/08/11/d3-scales-and-color/
    var x = d3.scale.ordinal()
        .domain(data.map(function(d) { return d.name; }))
        .rangeRoundBands([0, width], .1);
    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.value; })])
        .range([height, 0]);
    var colors = d3.scale.ordinal()
        .domain(['blue', 'green', 'grey'])
        .range(['steelblue', 'mediumseagreen', 'lightslategrey'])

    // Axis
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var chart = d3.select("#barchart")

    var bars = chart.selectAll("rect.bar")
        .data(data);

    //update
    //bars
    //    .attr("fill", "#0a0")
    //    .attr("stroke", "#050")

    //enter
    bars.enter()
        .append("rect")
        .attr("class", "bar")
        .attr("fill", function(d, i) { return colors(d.name) })
        //.attr("stroke", "#800");

    //exit 
    bars.exit()
        .transition()
        .duration(300)
        .ease("exp")
        .attr("height", 0)
        .remove()

    bars
        //.attr("stroke-width", 4)
        .transition()
        .duration(300)
        .ease("quad")
        .attr("x", function(d) { return x(d.name); })
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .attr("width", x.rangeBand())
        ;

    // Update Axis
    var svg = d3.select("#wfp_barchart_svg").transition();
    svg.select(".x.axis") // change the x axis
        .duration(750)
        .call(xAxis);
    svg.select(".y.axis") // change the y axis
        .duration(750)
        .call(yAxis);

}

// Creates the basic structure of the barchart
function initBarChartGWF(){
    // Load basic properties
    var basics = gwfBasics();

    var margin = basics.margin,
    width = basics.width,
    height = basics.height,
    colorBar = basics.colorBar,
    barPadding = basics.barPadding;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);
    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    //setup the svg
    var chart = d3.select("#wfp_barchart_svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("id", "barchart")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    chart.append("g")
        .attr("id", "barchart-xaxis")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    chart.append("g")
        .attr("id", "barchart-yaxis")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Water footprint (m3)");
}


function queryGwfAndUpdateBarChart(ingredient){
    if (!ingredient){
        console.log("No Ingredient!");
        
        var data = [ 
            {'name': 'blue',  'value':0}, 
            {'name': 'green', 'value':0},
            {'name': 'grey',  'value':0} 
        ];
        updateBarChartGWF(data);
        return;
    }

    d3.json('/data/ingredient/globalwaterfootprint/'+ingredient, function(error, jsonData) {

        var data = $.map(jsonData, function(value, index) {
            return [{'name':index, 'value':value}];
        });

        if (data.length > 0 ){
            updateBarChartGWF(data);
        }else{
            console.log('No data for the ingredient: ' + ingredient);
            var data = [ 
                {'name': 'blue',  'value':0}, 
                {'name': 'green', 'value':0},
                {'name': 'grey',  'value':0} 
            ];
            updateBarChartGWF(data);
        }
        
    });    
}

$(document).ready(function() {
    initBarChartGWF();
    
    d3.json('/data/ingredient/globalwaterfootprint', function(error, jsonData) {
        var data = $.map(jsonData, function(value, index) {
            return [{'name':index, 'value':value}];
        });

        updateBarChartGWF(data);
    });    

});