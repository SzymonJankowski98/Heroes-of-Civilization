function open_game(game_id) {
    window.location.href = "/game/" + game_id.toString();
}

function add_to_game(game_id) {
    window.location.href = "/user/addToGame/" + game_id.toString();
}