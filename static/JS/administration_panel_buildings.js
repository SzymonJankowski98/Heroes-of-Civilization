function delete_building(b_name) {
    window.location.href = "/administrationpanel/buildings/delete/" + b_name.toString();
}

function update_building(r_name) {
    window.location.href = "/administrationpanel/buildings/update/" + r_name.toString();
}