$(document).ready(function() {
    algodoo.ResetWait();
    var lessons = algodoo.LessonsInDir();

    for (i in lessons) {
        var lesson = lessons[i];
        var image = lesson.replace(".html", "").toLowerCase() + ".png";
        $('body').append('<div class="lesson"><div class="thumb-inner"><a href="' + lesson + '"><img src="' + image + '" /></a></div><a class="lesson-title" href="' + lesson + '">' + Translate('Lesson_' + lesson.replace(".html", "") + '_Title') + '</a></div>');
    }
});

