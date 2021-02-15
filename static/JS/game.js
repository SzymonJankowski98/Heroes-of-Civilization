// Make the DIV element draggable:
dragMap(document.getElementById("map"));
dragTab(document.getElementById("science_tab"), "science_header");
dragTab(document.getElementById("buildings_and_units_tab"), "buildings_and_fields_content_h1");

var size_x = 10;
var size_y = 10;

function set_size(x, y) {
  size_x = x;
  size_y = y;
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

    if (elmnt.offsetTop - pos2 <= 150) {
       if (elmnt.offsetTop - pos2 >= -((document.documentElement.clientWidth / 15 * size_y) - (document.documentElement.clientHeight) + 150)) {
         elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
       }
       else {
         elmnt.style.top = -((document.documentElement.clientWidth / 15 * size_y) - (document.documentElement.clientHeight) + 150) + "px";
       }
    }
    else {
      elmnt.style.top = 150 + "px";
    }

    if (elmnt.offsetLeft - pos1 <= 150) {
      if (elmnt.offsetLeft - pos1 >= -((document.documentElement.clientWidth / 15 * size_x) - (document.documentElement.clientWidth) + 150)) {
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
      }
      else {
        elmnt.style.left = -((document.documentElement.clientWidth / 15 * size_x) - (document.documentElement.clientWidth) + 150) + "px";
      }
    }
    else {
      elmnt.style.left = 150 + "px";
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
   }
   else {
     science = 0;
     science_tab.style.display = 'none';
   }
}

function activate_tab(elmnt) {
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
  }
}

function exit_buildings_units_tab() {
  document.getElementById("buildings_and_units_tab").style.display = 'none';
}