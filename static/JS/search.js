const input = document.querySelector('#search');

input.addEventListener('input', updateValue);

function updateValue(e) {
    var elements = document.getElementsByClassName("resource_name")
    for (var i of elements) {
        console.log(i);
        if (i.innerText.includes(input.value)) {
            i.parentElement.style.display = "table-row";
        }
        else {
            i.parentElement.style.display = "none";
        }
    }
}