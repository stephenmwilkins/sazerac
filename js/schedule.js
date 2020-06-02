

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTeq8khkfizcAYSLG5QiHDaiiiFBY9zjEmUCPyHkb4jR3iz40hpQUKm3wX0lHoylW4Oi7kwXIWgi4xS/pub?gid=833763484&single=true&output=csv';


var tags = ['Analogues','Reionization','Dark ages','First stars','AGN','Star formation histories','Metal/dust enrichment','Escape fractions','Theory','Observations','Tools','Outreach and diversity','Other'];


var tag_state = {};

function init() {

  Papa.parse(public_spreadsheet_url, {
    download: true,
    header: true,
    complete: saveData
  })
}

window.addEventListener('DOMContentLoaded', init)



function make_tag_list() {

  for (i=0; i<tags.length; i++) {
    tag_id = tags[i];
    var tag = document.createElement("li");
    tag.className = 'tag';
    tag.innerHTML = '<label><input class="checkbox" type="checkbox" id="'+tag_id+'" name="'+tag_id+'" checked=true> &nbsp;'+tag_id+'</label>'
    $("#tag_list").append(tag);
    tag_state[tag_id] = true;
    console.log(tag_id, tag_state[tag_id])
  }
}



window.addEventListener('DOMContentLoaded', make_tag_list)


$(document).ready(function() {

  $(".checkbox").change(function() {
    tag_state[this.id] = this.checked;
    console.log(tag_state);
    showInfo();
  });


  $("#check_all").click(function() {
    $('.checkbox').prop('checked', true);
    console.log('here');
    for (i=0;i<tags.length;i++) {
      tag_state[tags[i]] = true;
    }
    showInfo();
  });

  $("#check_none").click(function() {
    $('.checkbox').prop('checked', false);
    console.log('here');
    for (i=0;i<tags.length;i++) {
      tag_state[tags[i]] = false;
    }
    showInfo();
  });

});


function saveData(results) {
    window.data = results.data
    showInfo();
}



function showInfo() {

  console.log(window.data);

  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");



  // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

  for (var j = 0; j < window.data.length; j++) {

      d = window.data[j];

      var inc = false;

      var talk_tags = d['Tags'].split(",");

      console.log(talk_tags);

      for (var i=0; i<talk_tags.length; i++) {

        console.log(talk_tags[i], tag_state[talk_tags[i].trim()]);
        if (tag_state[talk_tags[i].trim()]) {
          inc = true;
        }
      }


      if (inc) {

        tr = table.insertRow(-1);
        tr.id = j;


        var time_zones = ['PDT','MDT','CDT','EDT','BST','CEST','CST','AWST','JST','AEST'];
        var offsets = [-7,-6,-5,-4,1,2,8,8,9,10];

        time_list = '';

        for (var k=0; k<time_zones.length; k++) {
          time = parseInt(d['Time'])+offsets[k]*100;
          if (time>=2400) {
            time = time - 2400;
            time = pad(time, 4)+'+1';
          } else {
            time = pad(time, 4);
          }
          time_list += '<b>'+time_zones[k]+': </b>'+time+'<br>';
        }


        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltip"><b>'+d['Session']+'/'+d['Talk']+'</b> ('+d['Date']+' '+d['Time']+')<span class="tooltiptext" style="width:100px;">'+time_list+'</span></div>';

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltip"><b>'+d['First Name']+' '+d['Family Name']+ '<span class="tooltiptext" style="width:300px;">'+ d['Institution']+'<br><a href="mailto:'+d['Email']+'">'+d['Email']+'</a></span></div>';

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltip">'+d['Title'] + '<span class="tooltiptext"><b>' + d['Tags']+ '</b><br>' + d['Abstract']+'</span></div>';

      }

  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);

}
