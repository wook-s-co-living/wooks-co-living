function search_address() {
  new daum.Postcode({
    oncomplete: function(data) {
      const addr = data.address;
      document.getElementById("s_address").value = addr;
      const addt = data.bname;
      document.getElementById("t_address").value = addt;
      const addb = data.buildingName;
      document.getElementById("b_address").value = addb;
    }
  }).open();
}

function previewImage(event) {
  var input = event.target;
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      var preview = document.querySelector('#preview-image');
      preview.setAttribute('src', e.target.result);
      preview.style.display = 'block';
    };

    reader.readAsDataURL(input.files[0]);
  }
}
var imageInput = document.querySelector('#id_image_first');
imageInput.addEventListener('change', previewImage);

document.addEventListener("DOMContentLoaded", function() {
  var limitField = document.getElementById("id_limit");
  limitField.addEventListener("input", function() {
      if (parseInt(limitField.value) < 1) {
          limitField.value = 1;
      }
  });

  var priceField = document.getElementById("id_price");
  priceField.addEventListener("input", function() {
      if (parseInt(priceField.value) < 0) {
          priceField.value = 0;
      }
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var categorySelect = document.querySelector('#id_category');
  var manyMoimDate = document.querySelector('#many-moim-date');
  var onceMoimDate = document.querySelector('#once-moim-date');

  function toggleMoimDate() {
    if (categorySelect.value === 'many') {
      manyMoimDate.style.display = 'block';
      onceMoimDate.style.display = 'none';
    } else if (categorySelect.value === 'once') {
      manyMoimDate.style.display = 'none';
      onceMoimDate.style.display = 'block';
    } else {
      manyMoimDate.style.display = 'block';
      onceMoimDate.style.display = 'none';
    }
  }

  categorySelect.addEventListener('change', toggleMoimDate);
  toggleMoimDate();
});