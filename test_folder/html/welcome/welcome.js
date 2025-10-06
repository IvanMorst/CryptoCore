function openTutorials() {
   algodoo.HighlightComponents("CompID_HelpButton");
   setTimeout(function () {algodoo.OpenWidgetByID('Help')}, 750);
   setTimeout(function () {algodoo.HighlightComponents("")}, 2000);
   return false; 
}

function openLessons() {
   algodoo.HighlightComponents("CompID_LessonsButton");
   setTimeout(function () {algodoo.OpenWidgetByID('LessonsBrowser')}, 750);
   setTimeout(function () {algodoo.HighlightComponents("")}, 2000);
   return false; 
}

function openContent() {
   algodoo.HighlightComponents("CompID_Algobox");
   setTimeout(function () {algodoo.OpenWidgetByID('AlgoboxBrowser')}, 750);
   setTimeout(function () {algodoo.HighlightComponents("")}, 2000);
   return false; 
}

function prevStep() {
    if (currentStep != 0) {
        //steps.eq(currentStep).hide('blind', { direction: "horizontal"}, 1000);
        currentStep--;
        createCookie('currentStep', currentStep, 70000);
        steps.eq(currentStep).animate({"margin-left": "+=485px"}, 750, "easeInOutQuad");
        //steps.eq(currentStep).show('blind', { direction: "horizontal", easing: "easeInOutExpo" }, 1000);
    }

    if (currentStep == 0)
        $('#buttons').hide('fade', 500);

    algodoo.HighlightComponents("");
}

function jumpSteps(steps) {
    if (steps.length == 1) {
        steps.eq(0).animate({"margin-left": "-=485px"}, 750, "easeOutQuad");
    } else {
        steps.eq(0).animate({"margin-left": "-=485px"}, 300, "linear", function () {
            jumpSteps(steps.slice(1));
        });
    }
}

function nextStep(jump) {
    jump = typeof(jump) != 'undefined' ? jump : 0;

    if (currentStep == 0)
        $('#buttons').show('fade', 1500);

    if (jump > 0) {
        var middle = steps.slice(currentStep, currentStep + jump + 1);
        jumpSteps(middle);

        currentStep += jump + 1;
        createCookie('currentStep', currentStep, 70000);

    } else {
        if (currentStep != steps.length - 1) {
            steps.eq(currentStep).animate({"margin-left": "-=485px"}, 750, "easeInOutQuad");

            // Check the step as done
            var check = steps.eq(currentStep).attr('introCheck');
            if (typeof(check) != "undefined") {
                createCookie(check, "true", 70000);
                $('#' + check + ' .checked').show();
            }

            currentStep++;
            createCookie('currentStep', currentStep, 70000);
            
            if (currentStep == steps.length - 1)
                algodoo.HighlightComponents("CompID_OptionsButton");
            else
                algodoo.HighlightComponents("");

        } else {
            // Hide every step except first and last
            steps.slice(1, steps.length - 1).hide();

            // Animate the last step
            steps.eq(currentStep).css({"position":"relative", "left":"-485px"});
            steps.eq(currentStep).animate({"left": "-=485px"}, 750, "easeInOutQuad");
            
            // Animate the first step
            steps.eq(0).animate({"margin-left": "+=485px"}, 0, "easeInOutQuad");
            steps.eq(0).css({"position":"relative", "left":485});
            steps.eq(0).animate({"left": "-=485px"}, 750, "easeInOutQuad", function () {
                // Reset every step
                steps.eq(steps.length - 1).css({"position":"static", "left":"0px"});
                steps.slice(1, steps.length - 1).show().animate({"margin-left": "+=485px"}, 0, "easeInOutQuad");
            });
            
            currentStep = 0;
            createCookie('currentStep', currentStep, 70000);

            $('#buttons').hide('fade', 500);
            
            algodoo.HighlightComponents("");
        }
    }
}

$(document).ready(function () {
    // Insert translations
    $('.translate').each(function () {
        var current = $(this);
        var text = current.html();
        current.html(Translate(text));
    });

    // Remove the activate step, if unlocked Algodoo or MAS
    if (!algodoo.IsLockedAlgodoo() || algodoo.IsAlgodooForMAS()) {
        $('#activate').remove();
    }

    if (algodoo.IsAlgodooForMAS()) {
        $('#introActivate').remove();
    }

    if (algodoo.IsLockedAlgodoo() && algodoo.IsDemoPeriodOver()) {
        $('#tutorials').hide(1, function () {
            $('#buy').show();
        });
    }

    // Replace the content button with a lessons button, if For Education
    if (algodoo.HasLessons()) {
        $('#content').hide(1, function () {
            $('#lessons').show();
        });
    }

    steps = $('body > div').not('.footer');
    
    currentStep = readCookie('currentStep');
    if (currentStep == null || currentStep > steps.length) {
        currentStep = 0;
        createCookie('currentStep', currentStep, 70000);
    }else {
        currentStep = parseInt(currentStep);
        for (var i=0; i<currentStep; i++) {
            steps.eq(i).animate({"margin-left": "-=485px"}, 1, "easeOutBounce");
        }
    }

    $('body').append(' \
<div id="buttons"> \
    <div id="prev-button-wrap"><button id="prev-button" type="button" onclick="prevStep();">' + Translate('Lesson_Prev') + '</button></div> \
    <div id="next-button-wrap"><button id="next-button" type="button" onclick="nextStep();">' + Translate('Lesson_Next') + '</button></div> \
</div>');

    if (currentStep != 0)
        $('#buttons').delay(100).show('fade', 500);

    // Add all the languages
    var languages = algodoo.GetLanguages();
    for (var i=0; i<languages.length; i++) {
        var language = languages[i];
        $('#languages').append('<li id="' + language + '" onclick="algodoo.LoadLanguage(\'' + language + '\');"><label>' + language + '</label><div class="checked"></div></li>');

        var flagPath = algodoo.GetLanguageFlagPath(language);
        if (flagPath != "") {
            var flag = $("<img />");
            flag.attr("src", flagPath);
            $('#' + language).append(flag);
        }
    }

	$('.checked').hide();

    // Set the current language
    $('#' + algodoo.GetLanguage() + ' .checked').show();

    // Set the current skin
    var skin = algodoo.GetSkinName();
    if (skin == "default")
        $('#default .checked').show();
    else if (skin == "white")
        $('#white .checked').show();

    // Set platform
    var touch = algodoo.IsTouchInput();
    if (touch)
        $('#touch .checked').show();
    else
        $('#keyboard .checked').show();

    // Make intro links
    $('#introLanguage').click(function () {
        nextStep();
    });

    $('#introSkin').click(function () {
        nextStep(1);
    });

    $('#introPlatform').click(function () {
        nextStep(2);
    });


    steps.each(function () {
        // Check if the step has been done before
        var check = $(this).attr('introCheck');
        if (typeof(check) != "undefined") {
            var intro = readCookie(check);
            if (intro != null && intro == "true") {
                $('#' + check + ' .checked').show();
            }
        }
    });

    if (!algodoo.IsLockedAlgodoo()) {
        $('#introActivate .checked').show();
    } else {
        $('#introActivate').click(function () {
            nextStep(3);
        });
    }

    // Disable text selection
    $('body').disableSelection();

    // Add the scrollpane
    setTimeout(function () {
        var element = $('#languages').jScrollPane({
            showArrows: true,
			verticalGutter: -2
        });

        var api = element.data('jsp');
        var scrollTo = $('#' + algodoo.GetLanguage()).position().top - $('#languages').position().top;
        api.scrollToY(scrollTo);
    }, 10);
});
