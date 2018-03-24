/**
 * Created by Antonina on 24.03.2018.
 */
$('#send-review-s').click(function() {
    var data = {
        "review": $('#review').val()
    };
    $.ajax({
        url: '/', //the page containing python script
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        type: 'POST',
        success: function(response) {
            if (response.redirect=='true'){
                var msg = response.message;
                alert(msg);
                window.location.href = response.redirect_url;
            }
            if (response.redirect=='false'){
                var msg = response.message;
                alert(msg);
            }
        },
        error: function() {
            console.log('error');
        }
    });
});

$('#send-review-c').click(function() {
    var data = {
        "review": $('#review-c').val()
    };
    $.ajax({
        url: '/', //the page containing python script
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        type: 'POST',
        success: function(response) {
            if (response.redirect=='true'){
                var msg = response.message;
                alert(msg);
                window.location.href = response.redirect_url;
            }
            if (response.redirect=='false'){
                var msg = response.message;
                alert(msg);
            }
        },
        error: function() {
            console.log('error');
        }
    });
});

$('#send-review-course').click(function() {
    var data = {
        "review": $('#review-course').val()
    };
    $.ajax({
        url: '/', //the page containing python script
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        type: 'POST',
        success: function(response) {
            if (response.redirect=='true'){
                var msg = response.message;
                alert(msg);
                window.location.href = response.redirect_url;
            }
            if (response.redirect=='false'){
                var msg = response.message;
                alert(msg);
            }
        },
        error: function() {
            console.log('error');
        }
    });
});