function loadScene(scene) {
    algodoo.SelectFile(algodoo.GetHTMLDir() + 'lessons/' + scene);
}

function scrollToStep() {
    if (typeof(api) != "undefined") {
        // Check if we are not on a new section
        if (steps[currentStep + 1].prev('.step').length)
            api.scrollToElement(steps[currentStep], true, true);
        else
            api.scrollToElement(steps[currentStep + 1].prevAll('h2'), true, true);
    } else {
        if (steps[currentStep + 1].prev('.step').length)
            $('html,body').stop().animate({scrollTop: steps[currentStep].offset().top - 20},'normal');
        else
            $('html,body').stop().animate({scrollTop: steps[currentStep + 1].prevAll('h2').offset().top},'normal');
    }
}

function jumpToStep(step) {
    leaveStep();
    currentStep = step;

    if (currentStep != 0) {
       $("#prev-button").removeAttr("disabled");
    } 

    if (currentStep != steps.length - 1) {
        $("#next-button").removeAttr("disabled");
    }

    runStep();
}

function leaveStep() {
    algodoo.ResetWait();
    //steps[currentStep].slideUp(20);
    
    if (currentStep > -1)
        steps[currentStep].removeClass("marked");

    $('#next-button-wrap').removeClass('marked');
}

function prevStep() {
    leaveStep();
    currentStep -= 2;
    scrollToStep();
    currentStep++;
    runStep();

    $("#next-button").removeAttr("disabled");

    if (currentStep == 0) {
       $("#prev-button").attr("disabled", "disabled");
    } 
}

function nextStep() {
    algodoo.ResetWait();
    onTaskComplete();

    $("#prev-button").removeAttr("disabled");
 
    if (currentStep == steps.length - 1) {
       $("#next-button").attr("disabled", "disabled");
    }
}

function onTaskComplete() {
    if (currentStep > -1) {
        //steps[currentStep].slideUp(200);
        steps[currentStep].removeClass("marked");
        steps[currentStep].addClass("done");
    }

    scrollToStep();
    
    currentStep++;
    $('#next-button-wrap').removeClass('marked');

    runStep();
}

function runStep() {
    var step = steps[currentStep];
    
    //step.slideDown(20);
    //step.fadeTo(1.0);
    step.addClass("marked");
    
    if (step.attr('method') == 'select') {
	    algodoo.WaitForToolSelect(step.attr('tool'));
    } else if (step.attr('method') == 'use') {
	    algodoo.WaitForToolUsage(step.attr('tool'));
    } else if (step.attr('method') == 'play') {
	    algodoo.WaitForPlay();
    } else if (step.attr('method') == 'pause') {
	    algodoo.WaitForPause();
    } else if (step.attr('method') == 'undo') {
	    algodoo.WaitForUndo();
    } else if (step.attr('method') == 'redo') {
	    algodoo.WaitForRedo();
    } else if (step.attr('method') == 'liquify') {
	    algodoo.WaitForLiquify();
    } else if (step.attr('method') == 'motor') {
	    algodoo.WaitForHingeMotor();
    } else if (step.attr('method') == 'clone') {
	    algodoo.WaitForClone();
    } else if (step.attr('method') == 'new') {
	    algodoo.WaitNewScene();
    } else if (step.attr('method') == 'save') {
	    algodoo.WaitForSceneSave();
    } else if (step.attr('method') == 'load') {
	    algodoo.WaitForSceneLoad();
    } else if (step.attr('method') == 'zoom') {
	    algodoo.HighlightComponents("CompID_Zoomer");
    } else if (step.attr('method') == 'pan') {
	    algodoo.HighlightComponents("CompID_Panner");
    } else if (step.attr('method') == 'manually' && step.attr('tool')) {
	    algodoo.HighlightTool(step.attr('tool'));
    } else if (step.attr('method') == 'manually' && step.attr('settings') == 'Material') {
	    algodoo.HighlightComponents("CompID_Material");
    } else if (step.attr('method') == 'manually' && step.attr('settings') == 'Color') {
	    algodoo.HighlightComponents("CompID_Apperance");
    } else if (step.attr('method') == 'manually' && step.attr('settings') == 'Visualization') {
	    algodoo.HighlightComponents("CompID_Visualization");
    } else if (step.attr('method') == 'manually' && step.attr('settings') == 'Measure') {
	    algodoo.HighlightComponents("CompID_Measure");
    } else if (step.attr('method') == 'home') {
        algodoo.HighlightComponents("CompID_TutorialBack");
    }
    
    if ((step.attr('method') == 'manually' || step.attr('method') == 'question') && currentStep != steps.length - 1) {
        $('#next-button-wrap').addClass('marked');
        $('#next-button-wrap').stop(true, true).effect("pulsate", { times:1 }, 1000);
    }
}

$(document).ready(function() {
    algodoo.ResetWait();

    $('.section:last').append('<div class="step" method="home">Lesson_Home</div>');

    steps = Array();
    currentStep = 1;

    // Translate every text node
    $('h1, h2, p, .step').each(function () {
        var current = $(this);
        var text = current.html();
        current.html(Translate(text));
    });

    $('.step').each(
        function(index2) {
            var step = $(this);

            // Make the steps clickable
            var cstep = currentStep - 1;
            step.click(function (){
                jumpToStep(cstep);
            });

            //step.hide();

            if (step.attr('method') == 'manually') {
                step.append(Translate('Lesson_Append_Next'));
            } else if (step.attr('method') == 'question') {
                step.append(Translate('Lesson_Append_Next_Question'));
            }

            step.wrapInner('<div class="step-text" />"');
            if (step.attr('tool')) {
                step.prepend('<div class="step-image-wrap"><img class="step-image" src="../../skins/default/gui/tools/' + step.attr('tool').toLowerCase() + '.png" /></div>');
            } else if (step.attr('settings')){
                step.prepend('<div class="step-image-wrap"><img class="step-image" src="../../skins/default/gui/' + step.attr('settings').toLowerCase() + '.png" /></div>');
            } else {
                step.prepend('<div class="step-image-wrap"><img class="step-image" src="../../skins/default/gui/' + step.attr('method').toLowerCase() + '.png" /></div>');
            }

            step.prepend('<div class="number">' + currentStep + '</span>');

            currentStep++;
            steps.push(step);
        }
    );

    currentStep = -1;
	
    $('body').append(' \
<div id="buttons"> \
    <div id="prev-button-wrap"><button id="prev-button" type="button" onclick="prevStep();" disabled="disabled">' + Translate('Lesson_Prev') + '</button></div> \
    <div id="next-button-wrap"><button id="next-button" type="button" onclick="nextStep();">' + Translate('Lesson_Next') + '</button></div> \
</div>');
    
    $('body').append('<div id="button-padding"></div>');


    if (!algodoo.IsTouchInput()) {
        createScroll();
    }
});

$(window).load(function() {
    if (typeof(api) != "undefined") {
        setTimeout(function () {api.reinitialise()}, 100);
    }
});

