function createScroll() {
    var element = $('body').jScrollPane({
        showArrows: true,
        verticalGutter: -2,
        enableKeyboardNavigation: false,
        animateDuration: 400,
        animateEase: 'easeOutQuad'
        
    });

    api = element.data('jsp');
}

function onTouchChanged() {
    // Remove the scrollbar if touch input
    if (algodoo.IsTouchInput()) {
        if (typeof(api) != "undefined") {
            api.destroy();
            delete api;
        }
    } else {
        createScroll();
    }

    if(typeof reloadDir == 'function') { 
        // If file browser, reload the dir to update the icons
        reloadDir(true);
    }
}

