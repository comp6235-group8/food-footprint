 d3.json("http://0.0.0.0:5000/data/recipes/popular_waterfootprint",function(error,data) {
        var str="<tr><th>rank<span class='glyphicon glyphicon-heart'></span></th><th align='center'>recipe name</th><th align='center'>water footprint(m3)</th></tr>";
           for(var i=0;i<data.length;i++)
            {
                var blue=data[i]["water_footprint"]["blue"].toFixed(2);
                var green=data[i]["water_footprint"]["green"].toFixed(2);
                var grey=data[i]["water_footprint"]["grey"].toFixed(2);
                var all=data[i]["water_footprint"]["total"].toFixed(2);
                str+="<tr><td>"+(i+1)+"</td><td>"+data[i]["name"]+"</td><td>"+all+"</td></tr>"
            }
           document.getElementById("top_recipe").innerHTML=str;
            stacked_bar(data);
    })

    d3.json("http://localhost:5000/data/recipes/most_lowest_waterfootprint",function(error,data) {
        //console.log(data);
        var str1='';
        var str2='';
        for(var i=0;i<10;i++)
            {
                str1+="<li>"+data[i]["name"]+"</li>"
                str2+="<li>"+data[i+10]["name"]+"</li>"
            }
           document.getElementById("most_recipe").innerHTML=str1;
           document.getElementById("least_recipe").innerHTML=str2;
    })

function stacked_bar(jsondata) {
    var dataset=[{data:[],name:'blue'},{data:[],name:'green'},{data:[],name:'grey'}];
    for (var i = 0; i < jsondata.length; i++) {
        dataset[0].data.push({
            name: jsondata[i]["name"],
            val0: 0,
            val1: jsondata[i]["water_footprint"]["blue"],
            type:"blue"
        });
         dataset[1].data.push({
            name: jsondata[i]["name"],
             val0: jsondata[i]["water_footprint"]["blue"],
            val1: jsondata[i]["water_footprint"]["green"],
             type:"green"
        });
         dataset[2].data.push({
            name: jsondata[i]["name"],
             val0:jsondata[i]["water_footprint"]["blue"]+jsondata[i]["water_footprint"]["green"],
            val1: jsondata[i]["water_footprint"]["grey"],
             type:"grey"
        });}

     var name = dataset[0].data.map(function (d) {
        return d.name;
    });
    var series = dataset.map(function (d) {
        return d.name;
    });
 var svg = d3.select("#recipe_bar"),
        margin = {top: 200, right: 20, bottom: 45, left: 40},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
     var xMax = 22898;
    var xScale = d3.scale.linear()
        .domain([0, xMax])
        .range([0, width]),
    yScale = d3.scale.ordinal()
        .domain(name)
        .rangeRoundBands([0, height], .1),
    xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        ,
    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient('left'),
    colours = ["white","#6495ed", "#3cb371", "#a9a9a9"];
    var data_all=["",dataset[0],dataset[1],dataset[2]];
    //console.log(data_all);
    var groups = svg.selectAll('g')
        .data(data_all)
        .enter()
        .append('g')
        .style('fill', function (d, i) {
        return colours[i];
    }),
    rects = groups.selectAll('rect')
        .data(function (d) {
        return d.data;
    })
        .enter()
        .append('rect')
        .attr('x', function (d) {
        return xScale(d.val0);
    })
        .attr('id', function (d) {
        return xScale(d.val0);
    })
        .attr('y', function (d, i) {
        return yScale(d.name);
    })
        .attr('height', function (d) {
        return yScale.rangeBand();
    })
        .attr('width', function (d) {
        return xScale(d.val1);
    })
        .on('mouseover', function (d,i) {
       g.selectAll('.watergrey').attr("opacity",1).text((dataset[2].data[i].val1).toFixed(2));
       g.selectAll('.watergreen').attr("opacity",1).text((dataset[1].data[i].val1).toFixed(2));
       g.selectAll('.waterblue').attr("opacity",1).text((dataset[0].data[i].val1).toFixed(2));



        })
        .on('mouseout',function (d) {
    g.selectAll('.watergrey').attr("opacity",0);
       g.selectAll('.watergreen').attr("opacity",0);
       g.selectAll('.waterblue').attr("opacity",0);



        })
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis)
        .attr("opacity",0);

svg.append('g')
    .attr('class', 'axis')
    .attr("x", 2)
    .attr("y", xScale(xScale.ticks(10).pop()))
    .call(yAxis);


 var legend = g.selectAll(".legend")
        .data(["grey", "green", "blue"])
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(200," + (i * 20-200) + ")";
        })
        .style("font", "10px sans-serif");

    legend.append("rect")
        .attr("x", width - 250)
        .attr("width", 18)
        .attr("height", 18)
        .attr("fill", function (d,i) {
            return colours[3-i];

        });

    legend.append("text")
        .attr("x", width - 260)
        .attr("y", 9)
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .text(function (d) {
            return d;
        });
     legend.append("text")
         .attr("class",function (d) {

         return "water"+d;})
            .attr("x", width - 180)
            .attr("y", 9)
            .attr("dy", ".35em")
            .attr("text-anchor", "end")

}