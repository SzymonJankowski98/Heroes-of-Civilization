const input = document.querySelector('#search');

input.addEventListener('input', updateValue);

function updateValue(e) {
    var elements = document.getElementsByClassName("search_key")
    for (var i of elements) {
        if (i.innerText.toLowerCase().includes(input.value.toLowerCase())) {
            i.parentElement.style.display = "table-row";
        }
        else {
            i.parentElement.style.display = "none";
        }
    }
}