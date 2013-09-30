function myweekchart(imp_week_data,eng_week_data,week_label){
w = 720,
h = 320,
margin = 40,
y0 = d3.scale.linear().domain([0, d3.max(imp_week_data)]).range([0 + margin, h - margin]),
y1 = d3.scale.linear().domain([0, d3.max(eng_week_data)]).range([0 + margin, h - margin]),
x = d3.scale.linear().domain([0, week_label.length]).range([0 + margin, w - margin - 60]);

var vis = d3.select("#weekchart")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var g = vis.append("svg:g")
    .attr("transform", "translate(0, 320)");

var line0 = d3.svg.line()
    .x(function(d,i) { return x(i); })
    .y(function(d) { return -1 * y0(d); })
    .interpolate("basis");

var line1 = d3.svg.line()
    .x(function(d,i) { return x(i); })
    .y(function(d) { return -1 * y1(d); })
    .interpolate("basis");

g.selectAll(".nodecircle0")
    .data(imp_week_data)
    .enter().append("svg:circle")
    .attr("class", "nodecircle0")
    .attr("cx", function(d,i) { return x(i); })
    .attr("cy", function(d) { return -1 * y0(d); })
    .style("fill", "steelblue")
    .attr("r", 3);

g.selectAll(".nodecircle1")
    .data(eng_week_data)
    .enter().append("svg:circle")
    .attr("class", "nodecircle1")
    .attr("cx", function(d,i) { return x(i); })
    .attr("cy", function(d) { return -1 * y1(d); })
    .style("fill", "green")
    .attr("r", 3);

g.append("svg:path").attr("d", line0(imp_week_data));

g.append("svg:path")
    .attr("d", line1(eng_week_data))
    .style("stroke", "green");

g.append("svg:line")
    .attr("x1", x(0))
    .attr("y1", -1 * y0(0))
    .attr("x2", x(week_label.length))
    .attr("y2", -1 * y0(0));
 
g.append("svg:line")
    .attr("x1", x(0))
    .attr("y1", -1 * y0(0))
    .attr("x2", x(0))
    .attr("y2", -1 * y0(d3.max(imp_week_data)));

g.append("svg:line")
    .attr("x1", x(week_label.length))
    .attr("y1", -1 * y1(0))
    .attr("x2", x(week_label.length))
    .attr("y2", -1 * y1(d3.max(eng_week_data)));

g.selectAll(".xLabel")
    .data(x.ticks(10))
    .enter().append("svg:text")
    .attr("class", "xLabel")
    .text(function(i) { return week_label[i]})
    .attr("x", function(d) { return x(d) })
    .attr("y", -20)
    .attr("text-anchor", "middle");
 
g.selectAll(".y0Label")
    .data(y0.ticks(6))
    .enter().append("svg:text")
    .attr("class", "y0Label")
    .text(function(d) {return String(d/1000)+"K"})
    .attr("x", 10)
    .attr("y", function(d) { return -1 * y0(d) })
    .attr("text-anchor", "right")
    .attr("dy", 4);

g.selectAll(".y1Label")
    .data(y1.ticks(6))
    .enter().append("svg:text")
    .attr("class", "y1Label")
    .text(String)
    .attr("x", x(week_label.length))
    .attr("y", function(d) { return -1 * y1(d) })
    .attr("text-anchor", "left")
    .attr("dy", 4);

g.selectAll(".xTicks")
    .data(x.ticks(10))
    .enter().append("svg:line")
    .attr("class", "xTicks")
    .attr("x1", function(d) { return x(d); })
    .attr("y1", -1 * y0(0))
    .attr("x2", function(d) { return x(d); })
    .attr("y2", -1 * y0(-300));
 
g.selectAll(".y0Ticks")
    .data(y0.ticks(6))
    .enter().append("svg:line")
    .attr("class", "yTicks")
    .attr("y1", function(d) { return -1 * y0(d); })
    .attr("x1", x(imp_week_data.length))
    .attr("y2", function(d) { return -1 * y0(d); })
    .attr("x2", x(0));

g.selectAll(".title")
    .data([1])
    .enter().append("svg:text")
    .attr("class", "title")
    .text("Impressions and Engagements in one week")
    .attr("x", 360)
    .attr("y", -5)
    .attr("text-anchor", "middle");

var legend = vis.append("svg:g")
	  .attr("class", "legend")
	  .attr("height", 100)
	  .attr("width", 100)
    .attr('transform', 'translate(-20,50)');
      
    
    legend.selectAll('rect')
      .data(["steelblue","green"])
      .enter()
      .append("rect")
	  .attr("x", w-40)
      .attr("y", function(d, i){ return i *  20;})
	  .attr("width", 10)
	  .attr("height", 10)
	  .style("fill", function(d){ return d; });
      
    legend.selectAll('text')
      .data(["IMP","ENG"])
      .enter()
      .append("text")
	  .attr("x", w -25)
      .attr("y", function(d, i){ return i *  20 +9;})
	  .text(function(d) { return d; });

}


function mydaychart(imp_day_data,eng_day_data,day_label){
w = 720,
h = 320,
margin = 40,
y0 = d3.scale.linear().domain([0, d3.max(imp_day_data)]).range([0 + margin, h - margin]),
y1 = d3.scale.linear().domain([0, d3.max(eng_day_data)]).range([0 + margin, h - margin]),
x = d3.scale.linear().domain([0, day_label.length]).range([0 + margin, w - margin - 60]);

var vis = d3.select("#daychart")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var g = vis.append("svg:g")
    .attr("transform", "translate(0, 320)");

var line0 = d3.svg.line()
    .x(function(d,i) { return x(i); })
    .y(function(d) { return -1 * y0(d); })
    .interpolate("basis");

var line1 = d3.svg.line()
    .x(function(d,i) { return x(i); })
    .y(function(d) { return -1 * y1(d); })
    .interpolate("basis");

g.selectAll(".nodecircle0")
    .data(imp_day_data)
    .enter().append("svg:circle")
    .attr("class", "nodecircle0")
    .attr("cx", function(d,i) { return x(i); })
    .attr("cy", function(d) { return -1 * y0(d); })
    .style("fill", "steelblue")
    .attr("r", 3);

g.selectAll(".nodecircle1")
    .data(eng_day_data)
    .enter().append("svg:circle")
    .attr("class", "nodecircle1")
    .attr("cx", function(d,i) { return x(i); })
    .attr("cy", function(d) { return -1 * y1(d); })
    .style("fill", "green")
    .attr("r", 3);

g.append("svg:path").attr("d", line0(imp_day_data));

g.append("svg:path")
    .attr("d", line1(eng_day_data))
    .style("stroke", "green");

g.append("svg:line")
    .attr("x1", x(0))
    .attr("y1", -1 * y0(0))
    .attr("x2", x(day_label.length))
    .attr("y2", -1 * y0(0));
 
g.append("svg:line")
    .attr("x1", x(0))
    .attr("y1", -1 * y0(0))
    .attr("x2", x(0))
    .attr("y2", -1 * y0(d3.max(imp_day_data)));

g.append("svg:line")
    .attr("x1", x(day_label.length))
    .attr("y1", -1 * y1(0))
    .attr("x2", x(day_label.length))
    .attr("y2", -1 * y1(d3.max(eng_day_data)));

g.selectAll(".xLabel")
    .data(x.ticks(10))
    .enter().append("svg:text")
    .attr("class", "xLabel")
    .text(function(i) { return day_label[i]})
    .attr("x", function(d) { return x(d) })
    .attr("y", -20)
    .attr("text-anchor", "middle");
 
g.selectAll(".y0Label")
    .data(y0.ticks(6))
    .enter().append("svg:text")
    .attr("class", "y0Label")
    .text(function(d) {return String(d/1000)+"K"})
    .attr("x", 10)
    .attr("y", function(d) { return -1 * y0(d) })
    .attr("text-anchor", "right")
    .attr("dy", 4);

g.selectAll(".y1Label")
    .data(y1.ticks(6))
    .enter().append("svg:text")
    .attr("class", "y1Label")
    .text(String)
    .attr("x", x(day_label.length))
    .attr("y", function(d) { return -1 * y1(d) })
    .attr("text-anchor", "left")
    .attr("dy", 4);

g.selectAll(".xTicks")
    .data(x.ticks(10))
    .enter().append("svg:line")
    .attr("class", "xTicks")
    .attr("x1", function(d) { return x(d); })
    .attr("y1", -1 * y0(0))
    .attr("x2", function(d) { return x(d); })
    .attr("y2", -1 * y0(-300));
 
g.selectAll(".y0Ticks")
    .data(y0.ticks(6))
    .enter().append("svg:line")
    .attr("class", "yTicks")
    .attr("y1", function(d) { return -1 * y0(d); })
    .attr("x1", x(imp_day_data.length))
    .attr("y2", function(d) { return -1 * y0(d); })
    .attr("x2", x(0));

g.selectAll(".title")
    .data([1])
    .enter().append("svg:text")
    .attr("class", "title")
    .text("Impressions and Engagements in one day")
    .attr("x", 360)
    .attr("y", -5)
    .attr("text-anchor", "middle");

var legend = vis.append("svg:g")
	  .attr("class", "legend")
	  .attr("height", 100)
	  .attr("width", 100)
    .attr('transform', 'translate(-20,50)');
      
    
    legend.selectAll('rect')
      .data(["steelblue","green"])
      .enter()
      .append("rect")
	  .attr("x", w-40)
      .attr("y", function(d, i){ return i *  20;})
	  .attr("width", 10)
	  .attr("height", 10)
	  .style("fill", function(d){ return d; });
      
    legend.selectAll('text')
      .data(["IMP","ENG"])
      .enter()
      .append("text")
	  .attr("x", w -25)
      .attr("y", function(d, i){ return i *  20 +9;})
	  .text(function(d) { return d; });

}

