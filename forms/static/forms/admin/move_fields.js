var move_source = function($, group_id) {
    var a = $(group_id)
    $('.source-fieldset').append(a)
    $("input:radio[name=person_secondary]").click(function() {
        var val = $(this).val();
        if (val == 1) {
            a.show();
        } else {
            a.hide();
        }
    })
}

var move_journalist = function($, group_id) {
    var a = $(group_id)
    $('.story-fieldset').append(a)
}

