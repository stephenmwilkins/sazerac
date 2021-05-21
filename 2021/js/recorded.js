

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}



var csvfile = 'data/recorded.csv'


var tags = ['Analogues','Reionization','Dark ages','First stars','AGN','Star formation histories','Metal/dust enrichment','Escape fractions','Theory','Observations','Tools','Outreach and diversity','Other'];



var tag_state = {};

function init() {

  Papa.parse(csvfile, {
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
    tag.innerHTML = '<div class="form-check form-switch"><input class="tag_checkbox form-check-input" type="checkbox" id="'+tag_id+'" name="'+tag_id+'" checked><label class="form-check-label" for="'+tag_id+'">'+tag_id+'</label></div>'
    $("#tag_list").append(tag);
    tag_state[tag_id] = true;

  }

}



window.addEventListener('DOMContentLoaded', make_tag_list)


$(document).ready(function() {

  $(".tag_checkbox").change(function() {
    tag_state[this.id] = this.checked;
    showInfo();
  });

  $("#check_all_tags").click(function() {
    $('.tag_checkbox').prop('checked', true);
    for (i=0;i<tags.length;i++) {
      tag_state[tags[i]] = true;
    }
    showInfo();
  });

  $("#check_no_tags").click(function() {
    $('.tag_checkbox').prop('checked', false);
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

  // console.log(window.data);

  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");



  // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

  for (var j = 0; j < window.data.length; j++) {

      d = window.data[j];

      console.log(d);

      var inc = false;

      var talk_tags = d['Tags'].split(",");

      for (var i=0; i<talk_tags.length; i++) {
        if (tag_state[talk_tags[i].trim()]) {
          inc = true;
        }
      }

      if (inc) {

        tr = table.insertRow(-1);
        tr.id = j;

        var abstract = d['Abstract']
        abstract = abstract.replace(/</g, "&lt;");
        abstract = abstract.replace(/>/g, "&gt;");

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltipc"><b>'+d['First Name']+' '+d['Family Name']+ '</b><span class="tooltiptextc" style="width:300px;">'+ d['Institution']+'<br><a href="mailto:'+d['Email']+'">'+d['Email']+'</a></span></div>';

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltipc">'+d['Talk Title'] + '<span class="tooltiptextc"><b>' + d['Tags']+ '</b><br>' + abstract +'</span></div>';

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = ' <b><a href="'+d['YouTube link']+'">[Recording]</a></b>';

      }


  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);

}
