function previewImage(event) {
  var input = event.target;
  if (input.files && input.files.length > 0) {
    var previewContainer = document.querySelector('#preview-container');
    previewContainer.innerHTML = '';

    for (var i = 0; i < input.files.length; i++) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var preview = document.createElement('img');
        preview.setAttribute('src', e.target.result);
        preview.setAttribute('class', 'preview-image');
        previewContainer.appendChild(preview);
      };
      reader.readAsDataURL(input.files[i]);
    }

    previewContainer.style.display = 'flex';
  }
}

var imageInput = document.querySelector('#id_image_first');
imageInput.addEventListener('change', previewImage);


document.addEventListener("DOMContentLoaded", function() {
  var priceField = document.getElementById("id_price");
  priceField.addEventListener("input", function() {
      if (parseInt(priceField.value) < 0) {
          priceField.value = 0;
      }
  });
});