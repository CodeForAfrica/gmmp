(function($){
    $(document).ready(function() {
        var a = $('#newspaperperson_set-group')
        $('.source-fieldset').append(a)
        $("input:radio[name=person_secondary]").click(function() {
            var val = $(this).val();
            if (val == 1) {
                a.show();
            } else {
                a.hide();
            }
})
    });
}(grp.jQuery));

