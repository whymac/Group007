var usageByNeigh = {};
var seasonData = {};
var tripnum = {};
var tip = {};
var tippercent = {};


// var incomeByNeigh = {}
var color1 = d3.scale.threshold()
    .domain([10000.37440000000004, 40000.70399999999995, 70000.9383999999973, 600942.08239999997, 15003518.00])
    .range(["#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8", "#756bb1", "#54278f"]);

console.log(color1(2.76254));
var width = 1200,
    height = 650,
    centered;
    gridSize = Math.floor(width / 25),
    legendWidth = (gridSize/2 + 4)


var tip1 = d3.tip()
  .attr('class', 'd3-tip1')
  .offset([-10, 0])
  .html(function(d) {
  return "<strong>Neighbourhood:</strong> <span style='color:red'>" + d.properties.NAME +"<br>"+ "</span>"+
           "<strong>Borough:</strong> <span style='color:red'>" + d.properties.CITY + "<br>"+"</span>"+
           "<strong>Taxi Usage:</strong> <span style='color:red'>" + seasonData[d.properties.NAME]+"<br>"+"</span>"+
          "<strong>Total trips:</strong> <span style='color:red'>" + tripnum[d.properties.NAME]+"<br>"+"</span>"+
          "<strong>Tip amount:</strong> <span style='color:red'>" + tip[d.properties.NAME]+"<br>"+"</span>"+
          "<strong>Tip percent:</strong> <span style='color:red'>" + tippercent[d.properties.NAME]+"<br>"+"</span>"



  });
// var tip2= d3.tip()
//   .attr('class', 'd3-tip2')
//   .offset([-10, 0])
//   .html(function(d) {
//     return "<strong>Neighbourhood:</strong> <span style='color:red'>" + d.properties.NAME +"<br>"+ "</span>"+
//            "<strong>Borough:</strong> <span style='color:red'>" + d.properties.CITY + "<br>"+"</span>"+
//            "<strong>Taxi Usage:</strong> <span style='color:red'>" + usageByNeigh[d.properties.NAME]+"<br>"+"</span>"+
//            "<strong>Median Household Income:</strong> <span style='color:red'>" +"$"+ incomeByNeigh[d.properties.NAME]/100000+ "<br>"+"</span>"
//   });


var projection = d3.geo.transverseMercator()
    .rotate([45,-150])
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
    .call(tip1);
    // .call(tip2);
var g = svg.append("g").call(zoom);


var legend = svg.selectAll(".g").data([1]).enter().append("legend")
  .attr("class","rect")
    .attr("width", 100)
    .attr("height", 100)
    .attr("x",500)
    .attr("y",300)
    .style("fill","black");



queue()
    .defer(d3.json, "./topo/T2.json")
    .defer(d3.csv,"./data/season.csv")
    .await(ready);

    function ready(error,ny,usg,ind) {
    //read data from taxiusage file,income file,add file name
      
      usg.forEach(function(d){
        usageByNeigh[d.Neighborhood] = +d.revenue
      });
      // console.log(usg);
      // console.log(usageByNeigh);
      // usg.forEach(function(d){console.log(d.Neighborhood);});
      var tracts = topojson.feature(ny, ny.objects.neighborhood);
       var b = path.bounds(tracts),
          s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
          t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];
    
    projection
      .scale(s)
      .translate(t);

      g.append("g")
      .attr("class", "county")
      .selectAll("paths")
      .data(topojson.feature(ny, ny.objects.neighborhood).features)
      .enter().append("path")
      .attr("class", "neighbourhood")
      .attr("data-neighbourhood", function(d) {return d.properties.NAME; })
      .attr("data-borough", function(d) {return d.properties.CITY; })
      .attr("d", path)
      .style("fill",function(d) { return color1(1);})
      .on("click", clicked)
      .on('mouseover', tip1.show)
      .on('mouseout', tip1.hide);


  d3.select("#Spring").on("click", function(d) { update(1); } );
  d3.select("#Summer").on("click", function(d) { update(2); } );
  d3.select("#Fall").on("click", function(d) { update(3); } );
  d3.select("#Winter").on("click", function(d) { update(4); } );
  

function update(season){
  seasonData = {}
  tripnum = {};
  tip = {};
  tippercent = {};
  if (season=="1")
  {   
      for(var i = 0;i < usg.length; i++) {
        if (usg[i].season=="1"){
          // console.log(usg[i].Neighborhood);
        seasonData[usg[i].Neighborhood] = +usg[i].revenue;
        tripnum[usg[i].Neighborhood] = +usg[i].tripsnumber;
        tip[usg[i].Neighborhood] = +usg[i].tipamount;
        tippercent[usg[i].Neighborhood] = +usg[i].tippercentage;

      }
    }
  }

  if (season=="2")
  {   
      for(var j = 0;j < usg.length; j++) {
        if (usg[j].season=="2"){
          // console.log(usg[j].Neighborhood);
      seasonData[usg[j].Neighborhood] = +usg[j].revenue;
        tripnum[usg[j].Neighborhood] = +usg[j].tripsnumber;
        tip[usg[j].Neighborhood] = +usg[j].tipamount;
        tippercent[usg[j].Neighborhood] = +usg[j].tippercentage;
      }
    }
  }
  if (season=="3")
  {   
      for(var k = 0;k< usg.length; k++) {
        if (usg[k].season=="3"){
          // console.log(usg[k].Neighborhood);
      seasonData[usg[k].Neighborhood] = +usg[k].revenue;
        tripnum[usg[k].Neighborhood] = +usg[k].tripsnumber;
        tip[usg[k].Neighborhood] = +usg[k].tipamount;
        tippercent[usg[k].Neighborhood] = +usg[k].tippercentage;
      }
    }
  }
  if (season=="4")
  {   
      for(var l = 0;l < usg.length; l++) {
        if (usg[l].season=="4"){
          // console.log(usg[l].Neighborhood);
      seasonData[usg[l].Neighborhood] = +usg[l].revenue;
        tripnum[usg[l].Neighborhood] = +usg[l].tripsnumber;
        tip[usg[l].Neighborhood] = +usg[l].tipamount;
        tippercent[usg[l].Neighborhood] = +usg[l].tippercentage;
      }
    }
    console.log(seasonData);
  }

      d3.selectAll("path.neighbourhood").remove();
       g.append("g")
      .attr("class", "county")
      .selectAll("paths")
      .data(topojson.feature(ny, ny.objects.neighborhood).features)
      .enter().append("path")
      .attr("class", "neighbourhood")
      .attr("data-neighbourhood", function(d) {return d.properties.NAME; })
      .attr("data-borough", function(d) {return d.properties.CITY; })
      .attr("d", path)
      .style("fill",function(d) { return color1(seasonData[d.properties.NAME]);})
      .on("click", clicked)
      .on('mouseover', tip1.show)
      .on('mouseout', tip1.hide);
  }



}





 //      g.append("g")
 //      .attr("class","centre")
 //      .selectAll("circle")
 //      .data(topojson.feature(ny, ny.objects.neighborhood).features)
 //      .enter().append("circle")
 //      .attr("class","centroid")
 //      .style("fill","orange")
 //      .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
 //      .attr("r", function(d) { return incomeByNeigh[d.properties.NAME]/100000; })
 //      .on("click", clicked)
 //      .on('mouseover', tip2.show)
 //      .on('mouseout', tip2.hide);
    
 // }









function zoomed() {
  g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  g.select(".state-border").style("stroke-width", 1.5 / d3.event.scale + "px");
  g.select(".county-border").style("stroke-width", 0.5/d3.event.scale + "px");
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
