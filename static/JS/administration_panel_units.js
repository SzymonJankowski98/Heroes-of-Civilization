function delete_unit(u_name) {
    window.location.href = "/administrationpanel/units/delete/" + u_name.toString();
}

function update_unit(u_name) {
    window.location.href = "/administrationpanel/units/update/" + u_name.toString();
}