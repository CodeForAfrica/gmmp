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

        /**
         * Toggles using the `Yes` answer i.e. add validation if `Yes` is
         * selected, If `No` is selected or nothing is selected at all, we remove validation.
         */
        var toggle_validation = function toggle_validation(person_set, el) {
            if (el.id === 'id_' + person_set + '-victim_or_survivor_1') {
                var add_validation$ = function(id) {
                    // Set --- since it's an invalid value and thus will receive
                    // validation error if user doesn't select another value
                    $(id).children('option:first').attr('value', '----');
                };
                var remove_validation$ = function(id) {
                    $(id).children('option:first').attr('value', '');
                };
                if ($(el).prop('checked')) {
                    add_validation$('#id_' + person_set + '-victim_of');
                    add_validation$('#id_' + person_set + '-survivor_of');
                } else {
                    remove_validation$('#id_' + person_set + '-victim_of');
                    remove_validation$('#id_' + person_set + '-survivor_of');
                }
            }
        };
        /**
         * Toggles using the `Yes` answer i.e. show if `Yes` is selected.
         */
        var toggle_person_set_victim_or_survivor_questions =
            function toggle_person_set_victim_or_survivor_questions(person_set, el) {
                if (el.id === 'id_' + person_set + '-victim_or_survivor_1') {
                    var $person_set = $('#' + person_set);
                    var $person_set_victim_question = $person_set.find('.field-victim_of');
                    var $person_set_survivor_question = $person_set.find('.field-survivor_of');
                    if (!$(el).prop('checked')) { 
                        $person_set_victim_question.hide();
                        $person_set_survivor_question.hide();
                    } else {
                        $person_set_victim_question.show();
                        $person_set_survivor_question.show();
                    }
                }
            };
        var newspaper_person_set = 'newspaperperson_set';
        var $newspaper_person_victim_or_survivor = $("input[id^='id_" + newspaper_person_set + "-'][id$='-victim_or_survivor_1']");
        $newspaper_person_victim_or_survivor.each(function (index) {
            toggle_validation(newspaper_person_set + '-' + index, this);
            toggle_person_set_victim_or_survivor_questions(newspaper_person_set + '-' + index, this);
        });
        var radio_person_set = 'radioperson_set';
        var $radio_person_victim_or_survivor = $("input[id^='id_" + radio_person_set +  "-'][id$='-victim_or_survivor_1']");
        $radio_person_victim_or_survivor.each(function (index) {
            toggle_validation(radio_person_set + '-' + index, this);
            toggle_person_set_victim_or_survivor_questions(radio_person_set + '-' + index, this);
        });
        var tv_person_set = 'televisionperson_set';
        var $tv_person_victim_or_survivor = $("input[id^='id_" + tv_person_set + "-'][id$='-victim_or_survivor_1']");
        $tv_person_victim_or_survivor.each(function (index) {
            toggle_validation(tv_person_set + '-' + index, this);
            toggle_person_set_victim_or_survivor_questions(tv_person_set + '-' + index, this);
        });
        var internet_person_set = 'internetnewsperson_set';
        var $internet_person_victim_or_survivor = $("input[id^='id_" + internet_person_set + "-'][id$='-victim_or_survivor_1']");
        $internet_person_victim_or_survivor.each(function (index) {
            toggle_validation(internet_person_set + '-' + index, this);
            toggle_person_set_victim_or_survivor_questions(internet_person_set + '-' + index, this);
        });
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
        // For TV, Internet, or Twitter, do not hide age field
        if(!(($('#televisionsheet_form').length > 0) || ($('#internetnewssheet_form').length > 0) || ($('#twittersheet_form').length > 0))) {
            $('.field-age').hide();
        }else{
            $('.field-age').show();
        }
    }

    $(document).ready(function() {
        // Remove "None" option from these fields
        
        $("ul[id^='id_newspaperperson_set-'][id$='-family_role'] li:first-child").remove();
        $("ul[id^='id_newspaperperson_set-'][id$='-victim_or_survivor'] li:first-child").remove();
        $("ul[id^='id_newspaperperson_set-'][id$='-is_quoted'] li:first-child").remove();
        
        $("ul[id^='id_radioperson_set-'][id$='-family_role'] li:first-child").remove();
        $("ul[id^='id_radioperson_set-'][id$='-victim_or_survivor'] li:first-child").remove();
        $("ul[id^='id_radioperson_set-'][id$='-is_quoted'] li:first-child").remove();
        
        $("ul[id^='id_televisionperson_set-'][id$='-family_role'] li:first-child").remove();
        $("ul[id^='id_televisionperson_set-'][id$='-victim_or_survivor'] li:first-child").remove();
        $("ul[id^='id_televisionperson_set-'][id$='-is_quoted'] li:first-child").remove();
        $("ul[id^='id_internetnewsperson_set-'][id$='-family_role'] li:first-child").remove();
        $("ul[id^='id_internetnewsperson_set-'][id$='-victim_or_survivor'] li:first-child").remove();
        $("ul[id^='id_internetnewsperson_set-'][id$='-is_quoted'] li:first-child").remove();
        $("ul[id^='id_twitterperson_set-'][id$='-family_role'] li:first-child").remove();
        $("ul[id^='id_twitterperson_set-'][id$='-victim_or_survivor'] li:first-child").remove();
        $("ul[id^='id_twitterperson_set-'][id$='-is_quoted'] li:first-child").remove();

        // "1": Full monitoring, "2": Short monitoring
        var monitor_mode = $("#id_monitor_mode").find(":selected").val();
        if(monitor_mode === "2"){
            activate_short_monitoring_mode();
        }else{
            activate_long_monitoring_mode();
        }
    });

    $(document).change(function() {
        var monitor_mode = $("#id_monitor_mode").find(":selected").val();
        if(monitor_mode === "2"){
            // Uncheck "Yes" on victim or survivor question
            $('#id_newspaperperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_radioperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_televisionperson_set-0-victim_or_survivor_1').prop('checked', false);
            $('#id_internetnewsperson_set-0-victim_or_survivor_1').prop('checked', false);
            activate_short_monitoring_mode();
        }else{
            activate_long_monitoring_mode();
        }
    });
}(jet.jQuery));
