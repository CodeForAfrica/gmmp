(function($){
    const special_tabs = function (field_age) {
        // For TV show the age
        if($('#televisionsheet_form').length > 0){
            field_age.show();
        }
        // For Internet show the age
        if($('#internetnewssheet_form').length > 0){
            field_age.show();
        }
    };

    const long_monitoring_mode = function () {
        $('.field-page_number').show();
        $('.field-space').show();
        $('.field-age').show();
        $('.field-is_photograph').show();
        $('.field-special_qn_1').show();
        $('.field-special_qn_2').show();
        $('.field-special_qn_3').show();
        $('.field-item_number').show();
        $('.field-webpage_layer_no').show();
        $('.field-victim_or_survivor').show();

        const newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_2:checked').length;
        const radio_person = $('#id_radioperson_set-0-victim_or_survivor_2:checked').length;
        const tv_person = $('#id_televisionperson_set-0-victim_or_survivor_2:checked').length;
        const internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_2:checked').length;

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
        }else{
            $('.field-victim_of').show();
            $('.field-survivor_of').show();
        }
    }

    const short_monitoring_mode = function() {
        // Show the short monitor mode form.
        $('.field-page_number').hide();
        $('.field-space').hide();
        $('.field-victim_or_survivor').hide();
        $('.field-victim_of').hide();
        $('.field-survivor_of').hide();
        $('.field-is_photograph').hide();
        $('.field-special_qn_1').hide();
        $('.field-special_qn_2').hide();
        $('.field-special_qn_3').hide();
        $('.field-item_number').hide();
        $('.field-webpage_layer_no').hide();
        $('.field-age').hide();

        special_tabs($('.field-age'));
    }

    $(document).ready(function() {
        const monitor_mode = $("#id_monitor_mode").find(":selected").val()
        $("#id_newspaperperson_set-0-family_role li:first-child").remove()
        $("#id_radioperson_set-0-family_role li:first-child").remove()
        $("#id_internetperson_set-0-family_role li:first-child").remove()
        $("#id_twitterperson_set-0-family_role li:first-child").remove()

        $("#id_newspaperperson_set-0-victim_or_survivor li:first-child").remove()
        $("#id_radioperson_set-0-victim_or_survivor li:first-child").remove()
        $("#id_internetperson_set-0-victim_or_survivor li:first-child").remove()
        $("#id_twitterperson_set-0-victim_or_survivor li:first-child").remove()

        $("#id_newspaperperson_set-0-is_quoted li:first-child").remove()
        $("#id_radioperson_set-0-is_quoted li:first-child").remove()
        $("#id_internetperson_set-0-is_quoted li:first-child").remove()
        $("#id_twitterperson_set-0-is_quoted li:first-child").remove()

        if(monitor_mode === "2"){
            short_monitoring_mode();
        }else{
            long_monitoring_mode();
        }
    });
    $(document).change(function() {
        const removeValidation = function(id) {
            $(`#${id}`).children('option:first').attr('value', '');
        };
        const addValidation = function(id) {
            // Set --- since it's an invalid value and thus will receive validation error if user doesn't select another value
            $(`#${id}`).children('option:first').attr('value', '----')
        };
        let newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        let radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        let tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        let internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

        const monitor_mode = $("#id_monitor_mode").find(":selected").val()
        if(monitor_mode === "2"){
            short_monitoring_mode()
        }else{
            long_monitoring_mode()
        }

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            addValidation('id_newspaperperson_set-0-victim_of');
            addValidation('id_newspaperperson_set-0-survivor_of');
            addValidation('id_radioperson_set-0-victim_of');
            addValidation('id_radioperson_set-0-survivor_of');
            addValidation('id_televisionperson_set-0-victim_of');
            addValidation('id_televisionperson_set-0-survivor_of');
            addValidation('id_internetnewsperson_set-0-victim_of');
            addValidation('id_internetnewsperson_set-0-survivor_of');
        }else{
            removeValidation('id_newspaperperson_set-0-victim_of');
            removeValidation('id_newspaperperson_set-0-survivor_of');
            removeValidation('id_radioperson_set-0-victim_of');
            removeValidation('id_radioperson_set-0-survivor_of');
            removeValidation('id_televisionperson_set-0-victim_of');
            removeValidation('id_televisionperson_set-0-survivor_of');
            removeValidation('id_internetnewsperson_set-0-victim_of');
            removeValidation('id_internetnewsperson_set-0-survivor_of');
    }});
}(jet.jQuery));
