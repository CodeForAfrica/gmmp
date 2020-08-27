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
        let newspaper_person = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length;
        let radio_person = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length;
        let tv_person = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length;
        let internent_person = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length;

        if((newspaper_person > 0) || (radio_person > 0) || (tv_person > 0) || (internent_person > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide();
        }else{
            $('.field-victim_of').show();
            $('.field-survivor_of').show();
        }
    });
}(jet.jQuery));
