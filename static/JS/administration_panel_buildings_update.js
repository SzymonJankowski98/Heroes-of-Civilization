function delete_building_cost(b_name, r_name) {
    window.location.href = "/administrationpanel/buildings/update/" + b_name.toString() + "/delCost/" + r_name.toString();
}

function delete_building_income(b_name, r_name) {
    window.location.href = "/administrationpanel/buildings/update/" + b_name.toString() + "/delIncome/" + r_name.toString();
}
