function toggleCarSelection() {
    var exportType = document.querySelector('input[name="export_type"]:checked').value;
    var carSelection = document.getElementById("car_selection");

    if (exportType === "services") {
        carSelection.style.display = "block";
    } else {
        carSelection.style.display = "none";
    }
}

window.onload = function () {
    toggleCarSelection();
};