



// var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQSVI1z0krjanS3xjQY1LoIDPU9gE0OZDy9kGFie9sESOl4ibVdW_tOFgx4SEWf6IAbh5zpG1WQ-pD0/pub?gid=526173983&single=true&output=csv';

var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv';

// var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRB4E_6RnpLP1wWMjqcwsUvotNATB8Np3OntlXb7066ULcAHI9oqqRhucltFifPTYNd7DRNRE56oTdt/pub?output=csv';

function init() {
  Papa.parse(public_spreadsheet_url, {
    download: true,
    header: true,
    complete: showInfo
  })
}

window.addEventListener('DOMContentLoaded', init)

function showInfo(results) {

  window.data = results.data


  $('#header').append('<b>'+window.data.length+'</b> people have registered so far.');

    window.data.sort(function(a, b) {
      return a['Family Name'] > b['Family Name'];
  });

  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");

  // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

  var tr = table.insertRow(-1);                   // TABLE ROW.

  var cols = ['Institution', 'Current Position', 'Talk Title'];

  // ADD JSON DATA TO THE TABLE AS ROWS.
  for (var i = 0; i < window.data.length; i++) {
      tr = table.insertRow(-1);
      tr.id = i;
      d = window.data[i];

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = '<b>'+d['First Name']+' '+d['Family Name']+'</b>';

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = d['Institution'];

  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";

  divContainer.appendChild(table);

}

window.addEventListener('DOMContentLoaded', init)
