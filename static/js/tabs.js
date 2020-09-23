(function($){
    var set_button_navigation = function() {
        var last_tab = $('.changeform-tabs li:last-child').hasClass('selected');
        if(last_tab) {
            $('input[name=_addanother]').show();
            $('input[name=_save]').show();
            $('input[name=_continue]').hide();
        }else{
            $('input[name=_addanother]').hide();
            $('input[name=_save]').hide();
            $('input[name=_continue]').show();
        }
    };

    $(document).ready(function() {
        var newspapersheet_form = $('#newspapersheet_form').length > 0;
        var radiosheet_form = $('#radiosheet_form').length > 0;
        var televisionsheet_form = $('#televisionsheet_form').length > 0;
        var internetnewssheet_form = $('#internetnewssheet_form').length > 0;
        var twittersheet_form = $('#twittersheet_form').length > 0;
        
        if(newspapersheet_form || twittersheet_form || radiosheet_form || televisionsheet_form || internetnewssheet_form){
            // Rename the save and continue button to Next
            var continueButton$ = $('input[name=_continue]');
            continueButton$.val('Next Tab');
            continueButton$.click((function(e) {
                e.preventDefault();
                // Move to next tab unless we are on the last tab
                var selectedTab$ = $('.changeform-tabs li.selected');
                    
                if ($('.changeform-tabs li.selected:last-child').length === 0){
                    selectedTab$.removeClass('selected').next().addClass('selected');
                    var module = selectedTab$.index();
                    $('.module_'+module).removeClass('selected');
                    $('.module_'+(module+1)).addClass('selected');
                    set_button_navigation();
                }
            }));
            $('.changeform-tabs li').click(function (e) {
                $('.changeform-tabs li').removeClass('selected');
                $(e.currentTarget).addClass('selected');

                set_button_navigation();
            });
            if($('.success').length){
                var selectedTab$ = $('.changeform-tabs li.selected');
                var module = selectedTab$.index();
                selectedTab$.removeClass('selected');
                $('.changeform-tabs li:first-child').addClass('selected');
                $('.module_'+module).removeClass('selected');
                $('.module_0').addClass('selected');
            }
            set_button_navigation();
        }
    });
}(jet.jQuery));
