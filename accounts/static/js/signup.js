$(document).ready(function() {
  var typingTimer;
  var doneTypingInterval = 100;

  checkDuplicateFirstName();

  $('#id_first_name').on('input', function() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(checkDuplicateFirstName, doneTypingInterval);
});

  function checkDuplicateFirstName() {
    var firstName = $('#id_first_name').val();

    if (!firstName) {
      $('#first-name-error').hide();
      return;
    }

      $.ajax({
          url: '/accounts/check/',
          type: 'GET',
          data: {'first_name': firstName},
          success: function(response) {
              if (response.duplicate) {
                  $('#first-name-error').text('※ 중복된 닉네임입니다.').show();
              } else {
                  $('#first-name-error').hide();
              }
          }
      });
  }
});

$(document).ready(function() {
  var isAllChecked = $(".checkbox--group .normal").length > 0; 
  $(".checkbox--group .normal").each(function(){
    isAllChecked = isAllChecked && $(this).is(":checked");
  });
  $("#check_all").prop("checked", isAllChecked);
  $("#submit_button").prop("disabled", !isAllChecked);
});

$(".checkbox--group").on("click", "#check_all", function () {
  var isChecked = $(this).is(":checked");
  $(this).parents(".checkbox--group").find('input').prop("checked", isChecked);
  $("#submit_button").prop("disabled", !isChecked);
});

$(".checkbox--group").on("click", ".normal", function() {
  var isAllChecked = true;
  $(".checkbox--group .normal").each(function(){
    isAllChecked = isAllChecked && $(this).is(":checked");
  });
  $("#check_all").prop("checked", isAllChecked);
  $("#submit_button").prop("disabled", !isAllChecked);
});