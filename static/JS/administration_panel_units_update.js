function delete_unit_cost(u_name, r_name) {
    window.location.href = "/administrationpanel/units/update/" + u_name.toString() + "/delCost/" + r_name.toString();
}