


function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}



public_spreadsheet_url = 'https://cors-anywhere.herokuapp.com/https://docs.google.com/spreadsheets/d/e/2PACX-1vTiCh2eEGbqIqyabmOoT9t89ILSYJbcO84npWnnPBdDpv8KR8TigDNZvAgioASBWp6CDQ4FT7Bw6gY0/pub?gid=900996784&single=true&output=csv'


var tag_state = {};

function init() {

  document.getElementById('talk_background').onclick = close_talk;

  Papa.parse(public_spreadsheet_url, {
    download: true,
    header: true,
    complete: saveData
  })
}

window.addEventListener('DOMContentLoaded', init)



function saveData(results) {
    window.data = shuffle(results.data)
    showInfo();
}



function showInfo() {

  console.log(window.data);

  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");

  // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

  for (var j = 0; j < window.data.length; j++) {

      d = window.data[j];


      tr = table.insertRow(-1);
      tr.id = j;

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = '<b>'+d['First Name']+' '+d['Family Name']+'</b>';

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = d['Institution'];

      var abstract = d['Abstract']
      abstract = abstract.replace(/</g, "&lt;");
      abstract = abstract.replace(/>/g, "&gt;");

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = '<div class="tooltip">'+d['Title'] + '<span class="tooltiptext"><br>' + abstract+'</span></div>';

      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = '<a href="'+d['PDF']+'"><b>[Download Poster]</b></a>';


  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);

}





function close_talk() {
  $("#talk_window").html('');
  $("#talk_background").css("display", "none");
  $("#talk_container").css("display", "none");
}




window.addEventListener('DOMContentLoaded', init)
