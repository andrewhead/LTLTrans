/*global $, document, Cookies*/

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

    // Listen for changes in one of the text areas to update the other
    $('#ltl-input').on('input', function() {
        $.post(
            '/ltl_to_english',
            {
                'formula': $(this).val(),
                'proposition': $('#prop-select').val(),
                'subjects': JSON.stringify(customSubjects),
            },
            function(data) {
                $('#text-input').val(data.sentence);
            }
        );
    });

    function updateExamplesToIndex(i) {
        var formula = $($('option')[i]).data('exampleFormula') || '';
        var sentence = $($('option')[i]).data('exampleSentence') || '';
        $('#ltl-input').attr('placeholder', formula).val("");
        $('#text-input').attr('placeholder', sentence).val("");
    }

    $('select').on('change', function() {
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
        $('select').append(opt).val(value);
    }

    $('#save_subj_button').on('click', function(e) {
        if (propositions.length > 0) {
            add_subject_to_select(propositions, customSubjects.length);
            customSubjects.push(propositions);
            Cookies.set('subjects', customSubjects);
        }
        dismiss_add_subj_cont(e);
    });

    $('#cancel_subj_button').on('click', function(e) {
        dismiss_add_subj_cont(e);
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
