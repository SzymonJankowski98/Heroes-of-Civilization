// Make the DIV element draggable:
dragElement(document.getElementById("map"));

var size_x = 10;
var size_y = 10;

function set_size(x, y) {
  size_x = x;
  size_y = y;
}

function dragElement(elmnt) {
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