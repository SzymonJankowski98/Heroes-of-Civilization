function delete_resource(r_name) {
    window.location.href = "/administrationpanel/resources/delete/" + r_name.toString();
}

function update_resource(r_name) {
    window.location.href = "/administrationpanel/resources/update/" + r_name.toString();
}