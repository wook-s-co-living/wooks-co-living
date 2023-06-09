var myField = document.getElementById("id_category");
var optionCh2 = document.querySelector('#id_category > option:nth-child(2)')
var optionCh3 = document.querySelector('#id_category > option:nth-child(3)')
var optionCh4 = document.querySelector('#id_category > option:nth-child(4)')
var optionCh5 = document.querySelector('#id_category > option:nth-child(5)')
if (myField.value === "") {
  myField.style.color = "rgb(185, 185, 185)";
  optionCh2.style.color = "rgb(128, 128, 128)";
  optionCh3.style.color = "rgb(128, 128, 128)";
  optionCh4.style.color = "rgb(128, 128, 128)";
  optionCh5.style.color = "rgb(128, 128, 128)";
}

myField.addEventListener("change", function(event) {
  if (event.target.value === "") {
    event.target.style.color = "rgb(185, 185, 185)";
    optionCh2.style.color = "rgb(128, 128, 128)";
    optionCh3.style.color = "rgb(128, 128, 128)";
    optionCh4.style.color = "rgb(128, 128, 128)";
    optionCh5.style.color = "rgb(128, 128, 128)";
  } else {
    event.target.style.color = "";
  }
});