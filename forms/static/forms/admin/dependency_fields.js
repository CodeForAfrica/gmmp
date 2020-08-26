(function($){
    $(document).ready(function() {
        let newspaperperson = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length
        let radioperson = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length
        let tvperson = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length
        let internentperson = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length

        if((newspaperperson > 0) | (radioperson > 0) | (tvperson > 0) | (internentperson > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide()
        }
    });
    $(document).change(function() {
        let newspaperperson = $('#id_newspaperperson_set-0-victim_or_survivor_1:checked').length
        let radioperson = $('#id_radioperson_set-0-victim_or_survivor_1:checked').length
        let tvperson = $('#id_televisionperson_set-0-victim_or_survivor_1:checked').length
        let internentperson = $('#id_internetnewsperson_set-0-victim_or_survivor_1:checked').length

        if((newspaperperson > 0) | (radioperson > 0) | (tvperson > 0) | (internentperson > 0)){
            $('.field-victim_of').hide();
            $('.field-survivor_of').hide()
        }else{
            $('.field-victim_of').show();
            $('.field-survivor_of').show()
        }
    });
}(jet.jQuery));
