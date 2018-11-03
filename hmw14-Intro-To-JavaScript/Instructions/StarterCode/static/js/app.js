// from data.js
var tableData = data;

// YOUR CODE HERE!
var submit = d3.select("#filter-btn");

submit.on("click", function() {
    d3.event.preventDefault();

    var inputElement = d3.select("#datetime");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");

  var filteredData = data.filter(date => date.datetime === inputValue);

  var tbody = d3.select("tbody");
  var rows = document.getElementById("ufo-table").getElementsByTagName("tbody")[0].getElementsByTagName("tr").length;
  console.log(rows);

  if (rows > 0){
    tbody.html("");
    
    filteredData.forEach((date) => {
        var row = tbody.append("tr");
        Object.entries(date).forEach(([key, value]) => {
          var cell = tbody.append("td");
          cell.text(value);
        });
      });
  }

  else{
  filteredData.forEach((date) => {
    var row = tbody.append("tr");
    Object.entries(date).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
  });}
});

