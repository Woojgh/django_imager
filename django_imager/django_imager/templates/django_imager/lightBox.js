$(document).ready(function() {

    /* This is basic - uses default settings */
    
    $("a.thumb-nail").fancybox();
    
    /* Using custom settings */
    
    $("a.thumb-nail").fancybox({
        'hideOnContentClick': true
    });

    /* Apply fancybox to multiple items */
    
    $("a.thumb-nail").fancybox({
        'transitionIn'  :   'elastic',
        'transitionOut' :   'elastic',
        'speedIn'       :   600, 
        'speedOut'      :   200, 
        'overlayShow'   :   false
    });
    
});