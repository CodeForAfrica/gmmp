(function($){
    $(document).ready(function() {
        let newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        let radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        let tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        let internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
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
