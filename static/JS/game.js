// Make the DIV element draggable:
dragMap(document.getElementById("map"));
dragTab(document.getElementById("science_tab"), "science_header");
dragTab(document.getElementById("buildings_and_units_tab"), "buildings_and_fields_content_h1");

var size_x = 10;
var size_y = 10;

function set_size(x, y) {
  size_x = x;
  size_y = y;
  document.getElementById("map").style.gridTemplateColumns = "repeat(" + x + ", 1fr)";
}

function dragMap(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "map")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "map").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    if (size_y * (document.documentElement.clientWidth / 15) > document.documentElement.clientHeight) {
      if (elmnt.offsetTop - pos2 <= 150) {
        if (elmnt.offsetTop - pos2 >= -((document.documentElement.clientWidth / 15 * size_y) - (document.documentElement.clientHeight) + 150)) {
          elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        } else {
          elmnt.style.top = -((document.documentElement.clientWidth / 15 * size_y) - (document.documentElement.clientHeight) + 150) + "px";
        }
      } else {
        elmnt.style.top = 150 + "px";
      }
    }

    if (size_x > 15) {
      if (elmnt.offsetLeft - pos1 <= 150) {
        if (elmnt.offsetLeft - pos1 >= -((document.documentElement.clientWidth / 15 * size_x) - (document.documentElement.clientWidth) + 150)) {
          elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        } else {
          elmnt.style.left = -((document.documentElement.clientWidth / 15 * size_x) - (document.documentElement.clientWidth) + 150) + "px";
        }
      } else {
        elmnt.style.left = 150 + "px";
      }
    }
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

function dragTab(elmnt, tag) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(tag)) {
    // if present, the header is where you move the DIV from:
    document.getElementById(tag).onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;

    var positionInfo = elmnt.getBoundingClientRect();

    if (elmnt.offsetTop - pos2 >= 0) {
      if ((elmnt.offsetTop - pos2 <= document.documentElement.clientHeight - positionInfo.height))
      {
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      }
      else
      {
        elmnt.style.top = document.documentElement.clientHeight - positionInfo.height + "px";
      }
    }
    else {
      elmnt.style.top = 0 + "px";
    }

    if (elmnt.offsetLeft - pos1 >= 0) {
      if ((elmnt.offsetLeft - pos1 <= document.documentElement.clientWidth - positionInfo.width))
      {
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
      }
      else
      {
        elmnt.style.left = document.documentElement.clientWidth - positionInfo.width + "px";
      }
    }
    else {
      elmnt.style.left = 0 + "px";
    }
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

var map = 1;

function change_map() {

  remove_unit_move_markers();

  let j;
  const all_units = document.getElementsByClassName("unit");
  for (j of all_units) {
    if (j.classList) {
      j.classList.remove("active_unit_marker");
    }
  }

  var i = 0;
  const buildings = document.getElementsByClassName("building");
  const units = document.getElementsByClassName("unit");

  if (map === 1)
  {
    map = 2;
    document.getElementById("change_map").src = "/static/images/swords2.png";

    for (i = 0; i < buildings.length; i++) {
      buildings[i].style.display = "none";
    }

    for (i = 0; i < units.length; i++) {
      units[i].style.display = "block";
    }
  } else {
    map = 1;
    document.getElementById("change_map").src = "/static/images/castle_button.png";

    for (i = 0; i < units.length; i++) {
      units[i].style.display = "none";
    }

    for (i = 0; i < buildings.length; i++) {
      buildings[i].style.display = "block";
    }
  }
}

var science = 0;

function toggle_science() {

   var science_tab =  document.getElementById("science_tab");
   if (science === 0) {
     science = 1;
     science_tab.style.display = 'block';

     $.ajax({
      type: 'POST',
      url: "/science",
      dataType: "text",
      success: function(data){
                 document.getElementById("available_science").innerHTML = data;
               }
    });
   }
   else {
     science = 0;
     science_tab.style.display = 'none';
   }
}

function activate_tab(elmnt) {
  const active_field = document.getElementsByClassName("active_field_marker")[0];

  var active_field_coords = active_field.parentElement.id.split(";");

  if ("buildings_tab1".includes(elmnt.id)) {
    elmnt.style.transform = "translateY(-12px)";
    document.getElementById("buildings_and_fields_content_header").style.backgroundColor = "#f5cc16";
    document.getElementById("buildings_and_fields_content_h1").innerText = "Budynki na polu";
    document.getElementById("buildings_tab1_content").style.display = "block";
    document.getElementById("buildings_tab2").style.transform = "translateY(0px)";
    document.getElementById("units_tab1").style.transform = "translateY(0px)";
    document.getElementById("units_tab2").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab2_content").style.display = "none";
    document.getElementById("units_tab1_content").style.display = "none";
    document.getElementById("units_tab2_content").style.display = "none";

    $.ajax({
      type: 'POST',
      url: "/yourbuildings",
      data: {x: active_field_coords[0], y: active_field_coords[1]},
      dataType: "text",
      success: function(data){
                 document.getElementById("buildings_tab1_content").innerHTML = data;
               }
    });
  }
  if ("buildings_tab2".includes(elmnt.id)) {
    elmnt.style.transform = "translateY(-12px)";
    document.getElementById("buildings_and_fields_content_header").style.backgroundColor = "#f5cc16";
    document.getElementById("buildings_and_fields_content_h1").innerText = "Dostępne budynki";
    document.getElementById("buildings_tab2_content").style.display = "block";
    document.getElementById("buildings_tab1").style.transform = "translateY(0px)";
    document.getElementById("units_tab1").style.transform = "translateY(0px)";
    document.getElementById("units_tab2").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab1_content").style.display = "none";
    document.getElementById("units_tab1_content").style.display = "none";
    document.getElementById("units_tab2_content").style.display = "none";

    $.ajax({
      type: 'POST',
      url: "/availablebuildings",
      data: {x: active_field_coords[0], y: active_field_coords[1]},
      dataType: "text",
      success: function(data){
                 document.getElementById("buildings_tab2_content").innerHTML = data;
               }
    });
  }
  if ("units_tab1".includes(elmnt.id)) {
    elmnt.style.transform = "translateY(-12px)";
    document.getElementById("buildings_and_fields_content_header").style.backgroundColor = "lightslategray";
    document.getElementById("buildings_and_fields_content_h1").innerText = "Jednostki na polu";
    document.getElementById("units_tab1_content").style.display = "block";
    document.getElementById("buildings_tab1").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab2").style.transform = "translateY(0px)";
    document.getElementById("units_tab2").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab1_content").style.display = "none";
    document.getElementById("buildings_tab2_content").style.display = "none";
    document.getElementById("units_tab2_content").style.display = "none";

     $.ajax({
      type: 'POST',
      url: "/yourunits",
      data: {x: active_field_coords[0], y: active_field_coords[1]},
      dataType: "text",
      success: function(data){
                 document.getElementById("units_tab1_content").innerHTML = data;
               }
    });
  }
  if ("units_tab2".includes(elmnt.id)) {
    elmnt.style.transform = "translateY(-12px)";
    document.getElementById("buildings_and_fields_content_header").style.backgroundColor = "lightslategray";
    document.getElementById("buildings_and_fields_content_h1").innerText = "Dostępne jednostki";
    document.getElementById("units_tab2_content").style.display = "block";
    document.getElementById("buildings_tab1").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab2").style.transform = "translateY(0px)";
    document.getElementById("units_tab1").style.transform = "translateY(0px)";
    document.getElementById("buildings_tab1_content").style.display = "none";
    document.getElementById("buildings_tab2_content").style.display = "none";
    document.getElementById("units_tab1_content").style.display = "none";

    $.ajax({
      type: 'POST',
      url: "/availableunits",
      data: {x: active_field_coords[0], y: active_field_coords[1]},
      dataType: "text",
      success: function(data){
                 document.getElementById("units_tab2_content").innerHTML = data;
               }
    });
  }
}

function exit_buildings_units_tab() {
  document.getElementById("buildings_and_units_tab").style.display = 'none';
  let i;
  const all_fields = document.getElementsByClassName("active_field_marker");
  for (i of all_fields) {
    if (i.classList) {
      i.classList.remove("active_field_marker");
    }
  }
}

function click_field(elmnt) {
  let i;
  const all_fields = document.getElementsByClassName("active_field_marker");
  for (i of all_fields) {
    if (i.classList) {
      i.classList.remove("active_field_marker");
    }
  }

  let j;
  const all_units = document.getElementsByClassName("active_unit_marker");
  for (j of all_units) {
    if (j.classList) {
      j.classList.remove("active_unit_marker");
    }
  }

  const active_elem = elmnt.getElementsByClassName("player_marker1")[0];
  if (active_elem !== undefined && active_elem.classList.contains("player_marker1")) {
      active_elem.classList.add("active_field_marker");
      document.getElementById("buildings_and_units_tab").style.display = 'block';
  }
  else {
    exit_buildings_units_tab();
  }

  remove_unit_move_markers();
}

function click_unit(elmnt, event) {
  let i;
  const all_units = document.getElementsByClassName("unit");
  for (i of all_units) {
    if (i.classList) {
      i.classList.remove("active_unit_marker");
    }
  }
  elmnt.classList.add("active_unit_marker");

  exit_buildings_units_tab();

  if (!event)
      event = window.event;
    if (event.stopPropagation) {
      event.stopPropagation();
    }
    else {
      event.cancelBubble = true;
    }

   mark_unit_move(elmnt, 2)
}

function mark_unit_move(elmnt, move_dist) {
  remove_unit_move_markers();
  var elmnt_coords = elmnt.parentElement.id.split(";");

  var coords = Array.from({length: move_dist + 1}, (_, i) => i);
  coords = coords.concat(Array.from({length: move_dist + 1}, (_, i) => -i));
  var dest_coords;
  var dest_elmnt;
  for (const i of coords) {
    for (const j of coords) {
       if (i === 0 && j === 0) continue;
       dest_coords = (i + parseInt(elmnt_coords[0])).toString() + ';' + (j + parseInt(elmnt_coords[1])).toString();
       dest_elmnt = document.getElementById(dest_coords);
       if (dest_elmnt) {
         if (dest_elmnt.classList.contains("water")) continue;
         dest_elmnt = dest_elmnt.getElementsByClassName("marker")[0];
         if (dest_elmnt) {
           dest_elmnt.classList.add("active_unit_dest_marker");
         }
       }
    }
  }
}

function remove_unit_move_markers() {
  var i;
  var all_fields = document.getElementsByClassName("active_unit_dest_marker");
  for (i=all_fields.length -1; i >= 0; i--) {
    if (all_fields[i].classList) {
      all_fields[i].classList.remove("active_unit_dest_marker");
    }
  }
}

function doScience(elmnt, name) {
  $.ajax({
      type: 'POST',
      url: "/doscience",
      data: {name: name},
      dataType: "text",
      success: function(data){
                 elmnt.classList.remove("btn_confirm");
                 elmnt.classList.add("btn_disabled");
                 elmnt.disabled = true;
                 document.getElementById("resources").innerHTML = data;
               }
    });
}

function buildBuilding(elmnt, name, x, y) {
  $.ajax({
      type: 'POST',
      url: "/buildbuilding",
      data: {name: name, x:x, y:y},
      dataType: "text",
      success: function(data){

                 elmnt.classList.remove("btn_confirm");
                 elmnt.classList.add("btn_disabled");
                 elmnt.disabled = true;
                 document.getElementById("resources").innerHTML = data;
               },
               error: function () {
                  window.alert('Za mało surowców');
               }
    });
}

function recruitUnit(elmnt, name, x, y) {

    amount = elmnt.parentElement.getElementsByTagName("input")[0];

    if (amount.value === '') {
      window.alert('Podaj liczbę jednostek!');
      return;
    }

    $.ajax({
      type: 'POST',
      url: "/recruitunit",
      data: {name: name, x:x, y:y, amount:amount.value},
      dataType: "text",
      success: function(data){

                 elmnt.classList.remove("btn_recruit");
                 elmnt.classList.add("btn_recruit_disabled");
                 elmnt.disabled = true;
                 amount.disabled = true;
                 document.getElementById("resources").innerHTML = data;
               },
               error: function () {
                  window.alert('Za mało surowców');
               }
    });
}