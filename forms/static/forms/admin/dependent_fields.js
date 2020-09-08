(function($){
    const special_fields = function () {
        // For TV show the age
        if($('#televisionsheet_form').length > 0){
            $('.field-age').show();
        }
        // For Internet show the age
        if($('#internetnewssheet_form').length > 0){
            $('.field-age').show();
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

        special_fields();
        const newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        const radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        const tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        const internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

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
        special_fields();
    }

    $(document).ready(function() {
        const monitor_mode = localStorage.getItem("monitor_mode");
        if(monitor_mode === "short"){
            $('#short_monitor_mode').prop("checked", true)
            short_monitoring_mode()
        }else{
            $('#long_monitor_mode').prop("checked", true);
            long_monitoring_mode()
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
