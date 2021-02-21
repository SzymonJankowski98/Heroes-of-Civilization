function delete_science_cost(s_name, r_name) {
    window.location.href = "/administrationpanel/science/update/" + s_name.toString() + "/delCost/" + r_name.toString();
}

function add_science_cost(s_name, r_name, r_amount) {
    window.location.href = "/administrationpanel/science/update/" + s_name.toString() + "/addCost/" + r_name.toString() + "/" + r_amount.toString();
}

