var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Neighbourhood:</strong> <span style='color:red'>" + d.properties.neighborhood +"<br>"+ "</span>"+
           "<strong>borough:</strong> <span style='color:red'>" + d.properties.borough + "<br>"+"</span>"+
           "<strong>Taxi Usage:</strong> <span style='color:red'>" +"$"+ Math.random()*30 +"<br>";
  })

var color = d3.scale.quantize()
  .range(["rgb(237,248,233)","rgb(186,228,179)","rgb(116,196,118)","rgb(49,163,84)","rgb(0,109,44)"])
  .domain([1,6]);

var width = 1000,
    height = 600,
    centered;


var projection = d3.geo.transverseMercator()
    .rotate([50,-150])
    .scale(1)
    .translate([0, 0]);

var path = d3.geo.path().projection(projection)


var zoom = d3.behavior.zoom()
    .translate([0, 0])
    .scale(1)
    .scaleExtent([1, 20])
    .on("zoom", zoomed);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var dis = svg.append("g")
    .attr("width", width)
    .attr("height", height)
    .on("click", clicked)
    .call(tip);

var g = svg.append("g").call(zoom);

 queue()
    .defer(d3.json, "./topo/T1.json")
    .await(ready);

    function ready(error, ny) {
      var tracts = topojson.feature(ny, ny.objects.nyc);

      var b = path.bounds(tracts),
          s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
          t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

      projection
      .scale(s)
      .translate(t);

      g.append("g")
      .attr("data-legend",function(d) { return d.properties.borough})
      .attr("class", "counties")
      .selectAll("paths")
      .data(topojson.feature(ny, ny.objects.nyc).features)
      .enter().append("path")
      .attr("class", "zip")
      .attr("data-neighbourhood", function(d) {return d.properties.neighborhood; })
      .attr("data-borough", function(d) {return d.properties.borough; })
      .attr("d", path)
      .style("fill",function(d){
        return color(Math.floor(Math.random() * 6) + 1);})
      .on("click", clicked)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
    }


function zoomed() {
  g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  g.select(".state-border").style("stroke-width", 1.5 / d3.event.scale + "px");
  g.select(".county-border").style("stroke-width", .5 / d3.event.scale + "px");
}


function clicked(d) {
  var x, y, k;

  if (d && centered !== d) {
    var centroid = path.centroid(d);
    x = centroid[0];
    y = centroid[1];
    k = 20;
    centered = d;
  } else {
    x = width / 2;
    y = height / 2;
    k = 1;
    centered = null;
  }

  g.selectAll("path")
      .classed("active", centered && function(d) { return d === centered; });

  g.transition()
      .duration(750)
      .attr("transform",function() {console.log ("translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")");return "transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")"})
      .style("stroke-width", 1.5 / k + "px");
}