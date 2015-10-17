/*global $, document*/

/* 
 * The following code enables AJAX requests with CSRF protection
 * REUSE: from https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        var i, cookie;
        for (i = 0; i < cookies.length; i++) {
            cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function init() {

    // Listen for changes in one of the text areas to update the other
    $('#ltl-input').on('input', function() {
        $.post(
            '/ltl_to_english',
            {
                'formula': $(this).val(),
                'proposition': $('#prop-select').val(),
            },
            function(data) {
                $('#text-input').val(data.sentence);
            }
        );
    });

    function updateExamplesToIndex(i) {
        var formula = $($('option')[i]).data('exampleFormula');
        var sentence = $($('option')[i]).data('exampleSentence');
        $('#ltl-input').attr('placeholder', formula).val("");
        $('#text-input').attr('placeholder', sentence).val("");
    }

    $('select').on('change', function() {
        updateExamplesToIndex($(this).val());
    });
    updateExamplesToIndex(0);

}

$(function() {
    init();
});
