(function($){
    var activate_long_monitoring_mode = function () {
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

        var no_newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_2:checked').length > 0;
        var no_radio_person = $('#id_radioperson_set-0-victim_or_survivor_2:checked').length > 0;
        var no_tv_person = $('#id_televisionperson_set-0-victim_or_survivor_2:checked').length > 0;
        var no_internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_2:checked').length > 0;
        if(no_newspaper_person || no_radio_person || no_tv_person || no_internent_person){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
        }else{
            $('.field-victim_of').show();
            $('.field-survivor_of').show();
        }
    }

    var activate_short_monitoring_mode = function() {
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
        // For TV or Internet, do not hide age field
        if(!(($('#televisionsheet_form').length > 0) || ($('#internetnewssheet_form').length > 0))) {
            $('.field-age').hide();
        }
    }

    $(document).ready(function() {
        // Remove "None" option from these fields
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

        // "1": Full monitoring, "2": Short monitoring
        var monitor_mode = $("#id_monitor_mode").find(":selected").val()
        if(monitor_mode === "2"){
            activate_short_monitoring_mode()
        }else{
            activate_long_monitoring_mode()
        }
    });

    $(document).change(function() {
        var monitor_mode = $("#id_monitor_mode").find(":selected").val()
        if(monitor_mode === "2"){
            // Uncheck "Yes" on victim or survivor question
            $('#id_newspaperperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_radioperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_televisionperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_internetnewsperson_set-0-victim_or_survivor_1').prop('checked', false);
            activate_short_monitoring_mode();
        }else{
            var removeValidation$ = function(id) {
                $(id).children('option:first').attr('value', '');
            };
            var addValidation$ = function(id) {
                // Set --- since it's an invalid value and thus will receive validation error if user doesn't select another value
                $(id).children('option:first').attr('value', '----')
            };
            var newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length > 0;
            var radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length > 0;
            var tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length > 0;
            var internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length > 0;
            if(newspaper_person || radio_person  || tv_person || internent_person){
                addValidation$('#id_newspaperperson_set-0-victim_of');
                addValidation$('#id_newspaperperson_set-0-survivor_of');
                addValidation$('#id_radioperson_set-0-victim_of');
                addValidation$('#id_radioperson_set-0-survivor_of');
                addValidation$('#id_televisionperson_set-0-victim_of');
                addValidation$('#id_televisionperson_set-0-survivor_of');
                addValidation$('#id_internetnewsperson_set-0-victim_of');
                addValidation$('#id_internetnewsperson_set-0-survivor_of');
    
            }else{
                removeValidation$('#id_newspaperperson_set-0-victim_of');
                removeValidation$('#id_newspaperperson_set-0-survivor_of');
                removeValidation$('#id_radioperson_set-0-victim_of');
                removeValidation$('#id_radioperson_set-0-survivor_of');
                removeValidation$('#id_televisionperson_set-0-victim_of');
                removeValidation$('#id_televisionperson_set-0-survivor_of');
                removeValidation$('#id_internetnewsperson_set-0-victim_of');
                removeValidation$('#id_internetnewsperson_set-0-survivor_of');
            }
            activate_long_monitoring_mode()
        }
    });
}(jet.jQuery));
