(function($){
    let tv_check = function () {
        // For TV show the age
        if($('#televisionsheet_form').length > 0){
            $('.field-age').show();
        }
    };
    let internent_check = function () {
        // For Internet show the age
        if($('#internetnewssheet_form').length > 0){
            $('.field-age').show();
        }
    };

    $(document).ready(function() {
        let short_monitor_mode = $('#short_monitor_mode:checked').length;
        let newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        let radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        let tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        let internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
        }
        if(short_monitor_mode > 0){
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
            tv_check();
            internent_check();
        }
    });
    $(document).change(function() {
        const removeValue = function(id) {
            $(`#${id}`).children('option:first').removeAttr('value');
        };
        const addValue = function(id) {
            $(`#${id}`).children('option:first').attr('value', '');
        };
        let newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        let radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        let tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        let internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            addValue('id_newspaperperson_set-0-victim_of');
            addValue('id_newspaperperson_set-0-survivor_of');
            addValue('id_radioperson_set-0-victim_of');
            addValue('id_radioperson_set-0-survivor_of');
            addValue('id_televisionperson_set-0-victim_of');
            addValue('id_televisionperson_set-0-survivor_of');
            addValue('id_internetnewsperson_set-0-victim_of');
            addValue('id_internetnewsperson_set-0-survivor_of');
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
            $('.field-is_photograph').hide();
            $('.field-special_qn_1').hide();
            $('.field-special_qn_2').hide();
            $('.field-special_qn_3').hide();
            $('.field-item_number').hide();
            $('.field-webpage_layer_no').hide();
            tv_check();
            internent_check();

        }else{
            removeValue('id_newspaperperson_set-0-victim_of');
            removeValue('id_newspaperperson_set-0-survivor_of');
            removeValue('id_radioperson_set-0-victim_of');
            removeValue('id_radioperson_set-0-survivor_of');
            removeValue('id_televisionperson_set-0-victim_of');
            removeValue('id_televisionperson_set-0-survivor_of');
            removeValue('id_internetnewsperson_set-0-victim_of');
            removeValue('id_internetnewsperson_set-0-survivor_of');
            $('.field-victim_of').show();
            $('.field-survivor_of').show();
        }
    });
}(jet.jQuery));
