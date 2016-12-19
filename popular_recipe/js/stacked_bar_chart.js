/**
 * Created by junewang on 15/12/2016.
 */
function stacked_bar(jsondata) {
    console.log(jsondata);
var data=[];
    for (var i = 0; i < jsondata.length; i++) {
        data.push({
            "name": jsondata[i]["name"],
            "blue": jsondata[i]["water_footprint"]["blue"],
            "green": jsondata[i]["water_footprint"]["green"],
            "grey": jsondata[i]["water_footprint"]["grey"],
            "total":jsondata[i]["water_footprint"]["blue"]+jsondata[i]["water_footprint"]["green"]+jsondata[i]["water_footprint"]["grey"]
        });

    }
    console.log(data);

    var svg = d3.select("svg"),
        margin = {top: 117, right: 20, bottom: 5, left: 40},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleBand()
        .rangeRound([0, height])
        .padding(0.1)
        .align(0.1);

    var y = d3.scaleLinear()
        .rangeRound([0, width - 100]);

    var z = d3.scaleOrdinal()
        .range(["#0000FF", "#008000", "#808080"]);

    var stack = d3.stack();
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<strong>blue:</strong> <span style='color:red'>" + d.data.blue.toFixed(2) + "</span>" +
                "<strong>green:</strong> <span style='color:red'>" + d.data.green.toFixed(2) + "</span>" +
                "<strong>grey:</strong> <span style='color:red'>" + d.data.grey.toFixed(2) + "</span>" +
                "<strong>total:</strong> <span style='color:red'>" + d.data.total.toFixed(2) + "</span>";
  })
    svg.call(tip);

//d3.csv("../popular/data.csv", type, function(error, data) {
    // if (error) throw error;

    console.log(data);
    x.domain(data.map(function (d) {
        return d.name;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.total;
    })]).nice();
    z.domain(["blue", "green", "grey"]);

    g.selectAll(".serie")
        .data(stack.keys(["blue", "green", "grey"])(data))
        .enter().append("g")
        .attr("class", "serie")
        .attr("fill", function (d) {
            return z(d.key);
        })
        .selectAll("rect")
        .data(function (d) {
            return d;
        })
        .enter().append("rect")
        .attr("y", function (d) {
            return x(d.data.name);
        })
        .attr("x", function (d) {
            return y(d[0]);
        })
        .attr("width", function (d) {
            return y(d[1]) - y(d[0]);
        })
        .attr("height", x.bandwidth())
        .on('mouseover',tip.show)
        .on('mouseout',tip.hidden)
      ;

    /*g.append("g")
        .attr("class", "axis axis--x")
        .attr("x", 2)
        .attr("y", y(y.ticks(10).pop()))
        .call(d3.axisLeft(x));*/

   /* g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisBottom(y).ticks(10, "s"))
        .append("text")
        .attr("transform", "translate(0," + height + ")")
        .attr("dy", "0.35em")
        .attr("text-anchor", "start")
        .attr("fill", "#000")
        .text("Population");*/

    var legend = g.selectAll(".legend")
        .data(["grey", "green", "blue"])
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(0," + i * 20 + ")";
        })
        .style("font", "10px sans-serif");

    legend.append("rect")
        .attr("x", width - 220)
        .attr("width", 18)
        .attr("height", 18)
        .attr("fill", z);

    legend.append("text")
        .attr("x", width - 230)
        .attr("y", 9)
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .text(function (d) {
            return d;
        });
}