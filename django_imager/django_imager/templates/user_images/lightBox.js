$(document).ready(function() {

    /* This is basic - uses default settings */
    
    $("a.thumbNail").fancybox();
    
    /* Using custom settings */
    
    $("a.thumbNail").fancybox({
        'hideOnContentClick': true
    });

    /* Apply fancybox to multiple items */
    
    $("a.thumbNail").fancybox({
        'transitionIn'  :   'elastic',
        'transitionOut' :   'elastic',
        'speedIn'       :   600, 
        'speedOut'      :   200, 
        'overlayShow'   :   false
    });
    
});