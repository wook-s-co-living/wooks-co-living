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
