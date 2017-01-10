$(document).ready(function () {
    bad_crop();
})
function bad_crop() {

    var svg = d3.select("#bad_crop");
    var margin = {top: 30, right: 20, bottom: 150, left: 40},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height")- margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .3);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#6495ed", "#3cb371", "#a9a9a9"]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(20)
        .tickFormat(d3.format(".2s"));

    var constant = 50;

    d3.json("../static/bad_crop.json", function (error, data) {
        if (error) throw error;

        var types = d3.keys(data[0]).filter(function (key) {
            return (key !== "product") && (key !== "amount");
        });

        data.forEach(function (d) {
            d.waterfootprint = types.map(function (name) {
                return {name: name, value: +d[name]};
            });
        });
        //console.log(data);
        x0.domain(data.map(function (d) {
            return d.product;
        }));
        x1.domain(types).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data, function (d) {
            return d3.max(d.waterfootprint, function (d) {
                return d.value;
            });
        })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate("+constant+"," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .attr("transform", "rotate(-80)")
            .attr("dx", "-1em")
            .attr("dy", ".20em")
            .style("text-anchor", "end")
            .style("font-size", "11px")
            .style("font-weight", "bold");

        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate("+constant+",0)")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Waterfootprint(m3)");

        var state = svg.selectAll(".state")
            .data(data)
            .enter().append("g")
            .attr("class", "state")
            .attr("transform", function (d) {
                var length = +x0(d.product) + constant;
                return "translate("+length+",0)";
            });

        state.selectAll("rect")
            .data(function (d) {
                return d.waterfootprint;
            })
            .enter().append("rect")
            .attr("width", x1.rangeBand())
            .attr("x", function (d) {
                return x1(d.name);
            })
            .attr("y", function (d) {
                return y(d.value);
            })
            .attr("height", function (d) {
                return height - y(d.value);
            })
            .style("fill", function (d) {
                return color(d.name);
            });

        // var _p3 = d3.format(".1f"); // save one number after point
        // var texts = state.selectAll(".MyText")
        //     .data(function (d) {
        //         return d.waterfootprint;
        //     })
        //     .enter()
        //     .append("text")
        //     .attr("x", function (d) {
        //         return x1(d.name) - 12;
        //     })
        //     .attr("y", function (d) {
        //         return y(d.value) - 25;
        //     })
        //     .attr("dx", 10)
        //     .attr("dy", 20)
        //     .text(function (d) {
        //         return _p3(d.value);
        //     });

        var legend = svg.selectAll(".legend")
            .data(types.slice().reverse())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function (d, i) {
                return "translate(0," + i * 20 + ")";
            });

        legend.append("rect")
            .attr("x", width+18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);

        legend.append("text")
            .attr("x", width+8)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function (d) {
                return d;
            });


    });
}