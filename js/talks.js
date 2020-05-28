



var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzuvYTA1U4H94gWcxZSQzWGXuKTeoeEJx2sm8AJOI_wa-rctxhN6FRxt6d9SDDKAXmH6Tj9rHoQvsH/pub?gid=1202228213&single=true&output=csv';


var tag_groups = ['processes', 'galaxy_types', 'components', 'observations', 'wavelengths', 'theory', 'misc'];
var processes = ['Reionisation', 'Star formation', 'Dark ages', 'Enrichment', 'Escape fractions'];
var galaxy_types = ['Dusty galaxies', 'LBGs', 'LAEs', 'Analogues', 'AGN'];
var components = ['Pop III stars', 'Stellar pops', 'BHs', 'HII regions', 'ISM', 'CGM', 'IGM'];
var observations = ['Wide Fields', 'Deep Fields', 'Ground', 'Space', 'Lensed', 'Imaging', 'Spectroscopy', 'IFU', 'Tools'];
var wavelengths = ['X-ray', 'UV', 'Optical', 'IR', 'Radio'];
var theory = ['Analytical', 'SAMs', 'Hydro', 'RT'];
var misc = ['Outreach', 'Diversity', 'Other'];

var tags = processes.concat(galaxy_types, components, observations, wavelengths, theory, misc);
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

for (j=0; j<tag_groups.length; j++) {
    tag_group = window[tag_groups[j]]
    for (i=0; i<tag_group.length; i++) {
      tag_id = tag_group[i];
      var tag = document.createElement("li");
      tag.className = 'tag';
      tag.innerHTML = '<label><input class="checkbox" type="checkbox" id="'+tag_id+'" name="'+tag_id+'" checked=true> &nbsp;'+tag_id+'</label>'
      $("#"+tag_groups[j]+"_tag_list").append(tag);
      tag_state[tag_id] = true;
      console.log(tag_id, tag_state[tag_id])
    }
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
    for (i=0;i<tags.length;i++) {
      tag_state[tags[i]] = true;
    }
    showInfo();
  });

  $("#check_none").click(function() {
    $('.checkbox').prop('checked', false);
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
        tr.onclick = showTalk;

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<b>'+d['First Name']+' '+d['Family Name']+'</b>';

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = d['Institution'];

        var tabCell = tr.insertCell(-1);
        tabCell.innerHTML = '<div class="tooltip">'+d['Title'] + '<span class="tooltiptext"><b>' + d['Tags']+ '</b><br>' + d['Abstract']+'</span></div>';

      }

  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);

}


function showTalk() {

  i = parseInt(this.id);

  var d = window.data[i];

  console.log(d);

  YT = d['YouTube link'].split('/');

  $("#talk_window").html('<div id="videoWrapper"><iframe src="https://www.youtube.com/embed/'+YT[YT.length - 1]+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>');

  $("#talk_window").append('<div id="talk_close" onclick="close_talk();"><img width="30px" src="images/close.png"></div>');
  // document.getElementById("talk_window").innerHTML += '<div id="talk_close" onclick="close_talk();"><img width="30px" src="images/close.png"></div>';

  $("#talk_speaker").html(d['First Name']+' '+d['Family Name']);
  $("#talk_title").html(d['Title']);
  $("#talk_abstract").html(d['Abstract']);

  if (d['Copy of slide'].length > 5) {
    $("#talk_slides").html('<a href="'+d['Copy of slide']+'">Download Slides</a>');
  } else {
    $("#talk_slides").html('');
  }


  $("#talk_background").css("display", "block");
  $("#talk_container").css("display", "block");
  $(window).scrollTop(0);


}


function close_talk() {
  $("#talk_background").css("display", "none");
  $("#talk_container").css("display", "none");
}




window.addEventListener('DOMContentLoaded', init)
