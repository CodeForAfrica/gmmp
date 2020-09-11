var check_tab_errors = function($, tab_id, tab_number) {
    if ($(`${tab_id} *`).hasClass("errorlist")) {
        $(`.changeform-tabs li:nth-child(${tab_number})`).addClass('errors');
    }
}
