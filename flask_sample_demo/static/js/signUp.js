$(function() {
    $('#btnSignUp').click(function() {
        $('#result').empty();
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                var result = response;
                $("#result").html(result);
            },
            error: function(error) {
                console.log(error);
                var result = error;
                $("#result").html(result);
            }
        });
    });
});
