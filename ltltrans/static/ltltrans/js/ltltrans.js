/*global $, document, Cookies, window*/

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

    var customSubjects = [];
    var propositions = [];
    var updateTimeoutId = -1;
    var UPDATE_WAIT = 2000;  // ms

    // Listen for changes in one of the text areas to update the other
    // However, first wait until the user has finished forming input
    function hide_update_text() {
        $('.update_text').hide();
        $('.success_img').hide();
        $('.error_text').hide();
    }

    $('#ltl-input').on('input', function() {
        hide_update_text();
        $('#text-update-text').show();
        window.clearTimeout(updateTimeoutId);
        updateTimeoutId = window.setTimeout(function() {
            $.post(
                '/ltl_to_english',
                {
                    'formula': $('#ltl-input').val(),
                    'proposition': $('#prop-select').val(),
                    'subjects': JSON.stringify(customSubjects),
                },
                function(data) {
                    hide_update_text();
                    $('#text-input').val(data.sentence);
                    $('#text-success-img').show().delay(2000).fadeOut(2000);
                }
            ).error(function() {
                hide_update_text();
                $('#ltl-error-text').show().delay(2000).fadeOut(2000);
            });
        }, UPDATE_WAIT);
    });

    $('#text-input').on('input', function() {
        hide_update_text();
        $('#ltl-update-text').show();
        window.clearTimeout(updateTimeoutId);
        updateTimeoutId = window.setTimeout(function() {
            $.post(
                '/english_to_ltl',
                {
                    'sentence': $('#text-input').val(),
                    'proposition': $('#prop-select').val(),
                    'subjects': JSON.stringify(customSubjects),
                },
                function(data) {
                    hide_update_text();
                    $('#ltl-input').val(data.ltl);
                    $('#ltl-success-img').show().delay(2000).fadeOut(2000);
                }
            ).error(function() {
                hide_update_text();
                $('#text-error-text').show().delay(3000).fadeOut(2000);
            });
        }, UPDATE_WAIT);
    });

    function updateExamplesToIndex(i) {
        var formula = $($('option')[i]).data('exampleFormula') || '';
        var sentence = $($('option')[i]).data('exampleSentence') || '';
        $('#ltl-input').attr('placeholder', formula).val("");
        $('#text-input').attr('placeholder', sentence).val("");
    }

    $('#prop-select').on('change', function() {
        updateExamplesToIndex($(this).val());
    });
    updateExamplesToIndex(0);

    // Enable users to add new subjects
    $('#add_subj_button').on('click', function(e) {
        $('#add_subj_cont').addClass('show');
        e.preventDefault();
    });

    function propListToString(propositions) {
        var propStrings = [];
        var i, prop, propStr;
        for (i = 0; i < propositions.length; i++) {
            prop = propositions[i];
            propStr = [prop.letter, "=", "'" + prop.subject, prop.verb, prop.object + "'"].join(" ");
            propStrings.push(propStr);
        }
        var propListMessage = propStrings.join(', ');
        return propListMessage;
    }

    function updatePropositionList(propositions) {
        if (propositions.length > 0) {
            $('#prop_list').text(propListToString(propositions))
                .removeClass("uninitialized");
        } else {
            $('#prop_list').text("(add propositions)")
                .addClass("uninitialized");
        }
    }

    $('#add_prop_button').on('click', function(e) {
        function getVal(selector) {
            var allEmpty = true;
            $('input[type="text"]').each(function() {
                if ($(this).val() !== '') {
                    allEmpty = false;
                    return false;
                }
            });
            if (allEmpty === false) {
                return $(selector).val();
            }
            return $(selector).attr('placeholder');
        }
        var prop = {
            'letter': getVal('#symbol_input'),
            'subject': getVal('#subject_input'),
            'verb': getVal('#verb_input'),
            'object': getVal('#object_input'),
        };
        propositions.push(prop);
        updatePropositionList(propositions);
        e.preventDefault();
    });

    function dismiss_add_subj_cont(e) {
        e.preventDefault();
        $('#add_subj_cont').removeClass('show');
        propositions = [];
        updatePropositionList(propositions);
    }

    function add_subject_to_select(propositions, index) {
        var value = "s" + String(index);
        var opt = $('<option></option>')
            .text(propListToString(propositions))
            .val(value);
        $('#prop-select').append(opt);
        return value;
    }

    $('#save_subj_button').on('click', function(e) {
        if (propositions.length > 0) {
            var optValue = add_subject_to_select(propositions, customSubjects.length);
            $('#prop-select').val(optValue);
            customSubjects.push(propositions);
            Cookies.set('subjects', customSubjects);
        }
        dismiss_add_subj_cont(e);
    });

    $('#cancel_subj_button').on('click', function(e) {
        dismiss_add_subj_cont(e);
    });

    // Report errors
    $('#report_button').on('click', function(e) {
        $('#report-details-cont').show();
        e.preventDefault();
    });

    $('#submit_report_button').on('click', function(e) {
        $.post(
            '/report_error',
            {
                'formula': $('#ltl-input').val(),
                'sentence': $('#text-input').val(),
                'proposition': $('#prop-select').val(),
                'error-type': $('#cause-select').val(),
                'suggestion': $('#suggestion-text').val(),
                'subjects': JSON.stringify(customSubjects),
            },
            function() {
                $('#suggestion-text').val("");
                $('#report-details-cont').hide();
                $('#thanks-text').show();
                $('#thanks-text').delay(1000).fadeOut(1000);
            }
        );
        e.preventDefault();
    });

    // Load existing custom subjects from cookies
    customSubjects = Cookies.getJSON('subjects') || [];
    var i;
    for (i = 0; i < customSubjects.length; i++) {
        add_subject_to_select(customSubjects[i], i);
    }

}

$(function() {
    init();
});
