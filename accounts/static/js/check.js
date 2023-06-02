$(document).ready(function() {
  var isIdChecked = false;

  $('.id--check--btn').click(function() {
    var usernameInput = $('input[name="username"]');
    var username = usernameInput.val();

    if (username === '') {
      alert('아이디를 입력해주세요.');
      return;
    }

    $.ajax({
      url: idOverlapCheckUrl,
      data: {
        'username': username
      },
      dataType: 'json',
      success: function(data) {
        console.log(data['overlap']);
        if (data['overlap'] === "fail") {
          alert("이미 존재하는 아이디입니다.");
          usernameInput.focus();
          $('#id-check-result').text('');
        } else {
          $('#id-check-result').text('사용 가능한 아이디입니다.').css('color', 'green');
        }
      }
    });
  });

  $('.email--check--btn').click(function() {
    var emailInput = $('input[name="email"]');
    var email = emailInput.val();

    if (email === '') {
      alert('이메일을 입력해주세요.');
      return;
    }

    $.ajax({
      url: emailOverlapCheckUrl,
      data: {
        'email': email
      },
      dataType: 'json',
      success: function(data) {
        console.log(data['overlap']);
        if (data['overlap'] === "fail") {
          alert("이미 존재하는 이메일입니다.");
          emailInput.focus();
          $('#email-check-result').text('');
        } else {
          $('#email-check-result').text('사용 가능한 이메일입니다.').css('color', 'green');
        }
      }
    });
  });

  $('input[name="username"]').on('input', function() {
    $('#id-check-result').text('').css('color', '');
  });

  $('input[name="email"]').on('input', function() {
    $('#email-check-result').text('').css('color', '');
  });

  $('form').submit(function() {
    if ($('#id-check-result').text() !== '사용 가능한 아이디입니다.') {
      alert("아이디 중복 체크를 해주시기 바랍니다.");
      $('input[name="username"]').focus();
      return false;
    }

    if ($('#email-check-result').text() !== '사용 가능한 이메일입니다.') {
      alert("이메일 중복 체크를 해주시기 바랍니다.");
      $('input[name="email"]').focus();
      return false;
    }
    
    var addressInput = $('#s_address');
    var address = addressInput.val();
    if (address === '') {
      alert('주소를 입력해주세요.');
      addressInput.focus();
      return false; }
  });
});
