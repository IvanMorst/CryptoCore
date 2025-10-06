$(document).ready(function() {
    $('img').bind('dragstart', function(event) { event.preventDefault(); });
});

function Translate(phraseID) {
    return algodoo.Translate(phraseID);
}

function WriteTranslate(phraseID) {
    document.write(Translate(phraseID));
}

