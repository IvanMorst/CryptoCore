function dotString(s) {
    if (s.length > 36)
        return s.trim().substring(0, 33) + "...";
    else
        return s;
}

function addHomeFolder() {
	$('.path-container').prepend('<a href="#" onclick="goHome()"> \
					 <span id="home-item"> \
						<img src="../../skins/default/gui/home.png" alt="Home" /></img> \
					</span> \
				</a>');
}

function addOpenFolder() {
	$('.path-container').append('<a href="#" onclick="openFolder()"> \
					 <span id="open-item"> \
						<img src="../../skins/default/gui/open.png" alt="Open folder" /></img> \
					</span> \
				</a>');
}

function addShowFolder() {
	$('.path-container').append('<a href="#" onclick="showFolder()"> \
					 <span id="show-item"> \
						<img src="../../skins/default/gui/redo.png" alt="Show folder" /></img> \
					</span> \
				</a>');
}

function addUpFolder() {
    var aTag = $('<div class="folder-item"> \
                    <a href="#"> \
						<img border="2" src="../../skins/default/gui/openUp.png" alt=".." /><h4>..</h4></img> \
					</a> \
				</div>');

    aTag.click(function () {
        clickFolder("..");
    });
    
	$('.folder-container').append(aTag);
}

function addFolder(folder) {
    var aTag = $('<div class="folder-item"> \
                    <a href="#"> \
						<img border="2" src="../../skins/default/gui/open.png" alt="' + folder + '" /><h4>' + folder + '</h4></img> \
					</a> \
				</div>');
    
    aTag.click(function () {
        clickFolder(folder);
    });

	$('.folder-container').append(aTag);
}

function addFile(filename, container, post) {
    var imgPath = algodoo.GetFileImagePath(algodoo.dir, filename);
	var imgUrl = imgPath + '?imageRev=' + g_imageRev;
	var dropped = "_dropped";
	var itemClass = "scene-item";
    var phzFile = (filename.substr(-3) === "phz");
    var cfgFile = (filename.substr(-3) === "cfg");
	
	var fullname = "";
	
	if (filename.substr(0, dropped.length) === dropped)
	{
		fullname = "";
		itemClass = "dropped-item";
	}
	else
	{
	    fullname = algodoo.ShownFileName(filename);
	}

	if (imgPath==="")
	{
	    // Failed to find an image for the file...
	    container.append('<div class="' + itemClass + '"><a href="#" onclick="clickFile(\'' + filename + '\');"><img border="2" id="' + filename + '" alt="' + filename + '" src=""/></a><h4>' + dotString(fullname) + '</h4></div>');
	
		if (phzFile)
            post.push(filename);
	}
	else
	{
        var hasRenameField = false;
        var img = $("<img/>", {
            border: 2,
            src: imgUrl,
            alt: filename,
            "class": "draggable",
        });

        // Show the renameField and hide the header
        function showRenameField() {
            hasRenameField = true;
            renameField.val(fullname);
            
            var l = header.offset().left;
            var t = header.offset().top;
            
            if (typeof(api) != "undefined")
                t += api.getContentPositionY();

            header.hide('fade', function () {
                renameField.css({ "top" : t, "left" : l});
                renameField.show();
                renameField.select();
            });

            renameButton.hide();
            eraseButton.hide();

            return false;
        }

        var header = $('<h4>' + dotString(fullname) + '</h4>');

        var confirmButton = $("<div/>", {
            "class": "confirm-button",
            text: algodoo.Translate('OK')
        });
        
        var eraseButton = $("<div/>", {
            "class": "erase-button",
            click: function () {
                renameButton.hide(0, function () {
                    header.hide('Drop');
                    confirmButton.show('Drop');
                });
                return false;
            }
        });

        // Rename the file, update the header and the file variable
        function doRenameFile() {
            var oldFilename = fullname;
            fullname = renameField.val();
            var newFilename = fullname;

            if (phzFile)
                newFilename += ".phz";
            else if (cfgFile)
                newFilename += ".cfg";

            if (filename != newFilename && fullname != "") {
                if (renameFile(filename, newFilename)) {
                    header.html(dotString(fullname));
                    filename = newFilename;
                    img.attr('alt', newFilename);
                    
                    if (itemClass === "dropped-item") {
                        div.removeClass(itemClass);
                        itemClass = "scene-item";
                        div.addClass(itemClass);
                    }
                } else {
                    fullname = oldFilename;
                }
            }

            hasRenameField = false;
            renameField.hide('fade', function () {
                header.show();

                if (algodoo.IsTouchInput()) {
                    eraseButton.show();
                    renameButton.show();
                }
            });
        };

        var renameField = $("<input/>", {
            "class": "rename-field",
            type: "text",
            click: function () {
                return false;
            },
            focusout: function () {
                if (hasRenameField)
                    doRenameFile();
            },
            keydown: function (e) {
                // This is what happens when someone clicks 
                // Caveat emptor: non-ascii characters can give e.keyCode == 0
                if (e.keyCode == 13 || e.keyCode == 113) { // Enter or F2
                    doRenameFile();

                    // To be able to use the arrows again
                    href.focus();
                    return false;
                } else if (e.keyCode == 27) { // Escape: Abort
                    hasRenameField = false;
                    renameField.hide('fade', 'fast', function () {
                        header.show();

                        if (algodoo.IsTouchInput()) {
                            renameButton.show();
                        }
                    });

					// To be able to use the arrows again
					href.focus();
                    return false;
                }

                e.stopPropagation();
            }
        });

        var renameButton = $("<div/>", {
            "class": "rename-button",
            click: function () {
                if (!renameField.is(":visible")) {
                    showRenameField();
                    return false;
                } else {
                    doRenameFile();
                    return false;
                }
            }
        });
        
        var div = $("<div/>", {
            "class": itemClass,
            mouseenter: function () {
                if ((!g_plain || fullname == "") && (!hasRenameField)) {
                    eraseButton.show();
                    renameButton.show();
                }
            },
            mouseleave: function () {
                if (!algodoo.IsTouchInput()) {
                    eraseButton.hide();
                    renameButton.hide();
                }

                confirmButton.hide('Drop');

                if (!hasRenameField) {
                    header.show('Drop');

                    if (algodoo.IsTouchInput()) {
                        renameButton.show();
                    }
                }
            },
			click: function () {
                clickFile(filename);
                return false;
            }
        }).appendTo(container);
        
        var href = $("<a/>", {
            href: "#",
        }).appendTo(div);
        
        img.appendTo(href);

        if (algodoo.IsMutable(algodoo.dir + filename)) {
            div.append(eraseButton);
            div.append(confirmButton);
            div.append(renameButton);
            div.append(renameField);

            header.click(function () {
                if (!g_plain) {
                    showRenameField();
                    return false;
                }
            });
        }
        
        if (!algodoo.IsTouchInput() || g_plain) {
            eraseButton.hide();
            renameButton.hide();
        }

        div.append(header);
        
        $("<img/>", {
            src: "../../skins/default/gui/erase.png"
        }).appendTo(eraseButton);
        
        $("<img/>", {
            src: "../../skins/default/gui/rename.png"
        }).appendTo(renameButton);


        confirmButton.click(function () {
                        div.hide('fold', 'slow', function () {
                            eraseFile(filename);
                        });
                        return false;
                     });
	}
}

function rememberDir() {
    // Remembers this dir in a cookie, for the current browser (Scene or Scenelet)
    var dirId = algodoo.dirId;
    
    if (dirId != "")
        // Name, string, expire time
        createCookie(dirId, escape(algodoo.dir), 70000);
}

function goHome() {
    algodoo.GoHome();
    rememberDir();
	reloadDir();
	return false;
}

function openFolder() {
    var dir = algodoo.OpenFolder(algodoo.dir);

    if (dir != "") {
        algodoo.dir = algodoo.NiceDir(dir);
        rememberDir();
        reloadDir();
    }

	return false;
}

function showFolder() {
    algodoo.ShowFolder(algodoo.dir);
	return false;
}

function clickFolder(folder) {
    setSelectedFile(-1);
    algodoo.dir = algodoo.NiceDir(algodoo.dir + folder);
    rememberDir();
	reloadDir();
	return false;
}

function clickFile(scene) {
    algodoo.SelectFile(algodoo.dir + scene);
	return false;
}

function eraseFile(scene) {
    algodoo.EraseFile(algodoo.dir + scene);
    reloadDir(true);
}

function renameFile(scene, name) {
    return algodoo.RenameFile(algodoo.dir + scene, algodoo.dir + name);
}

function clickableDirs(dir) {
	var result = "";
	var folders = dir.split('/');
	var path = "";
	
	for (var i=0; i<folders.length - 1; i++) {
		var depth = folders.length - 2 - i;
		
		result += '<a href="#" onclick="clickFolder(\'';
		for (var j=0; j<depth; j++) {
			result += '../';
		}
		result += '\');">' + folders[i] + '</a>/';
		
	}
	
	return result
}

function selectSort(sort) {
    algodoo.sort = sort;
    reloadDir();
    return false;
}

function FilesPerPage() {
    /* We can't show too many scenes per page, or two things will get slow:
        1) loading (a lot of images to load)
        2) scrolling/mouse over
       So we break it up into several pages.
    */

    /*
    // 2.0.1 - 4 width (4 in plain mode).
    var ret = (algodoo.IsPlain() ? 50 : 48);
    /*/
    // 2.0.2 - 5 width (6 in plain mode).
    var ret = (algodoo.IsPlain() ? 48 : 50);
    /**/
    
    if (g_plain)
        ret *= 20; // If no images, we can have more
    
    //ret *= 10; // TESTING
        
    return ret;
}

function setPlain() {
    g_plain = !g_plain;

    // Name, string, expire time
    createCookie("plain", g_plain, 70000);

    if (g_plain) {
        $('.scene-item').addClass('plain');
        $('#plain').attr('checked', 'checked');

        if (algodoo.IsTouchInput()) {
            $('.erase-button').hide();
            $('.rename-button').hide();
        }
        
    } else {
        $('.scene-item').removeClass('plain');
        $('#plain').removeAttr('checked');

        if (algodoo.IsTouchInput()) {
            $('.erase-button').show();
            $('.rename-button').show();
        }
    }
    
    relistPage(true); // FilesPerPage() changed

    return false;
}

function setSelectedFile(nr, animate) {
    animate = (typeof(animate) != 'undefined' ? animate : false);

    g_selectedFile = nr;
    g_fileDivs.removeClass('selected');
    if (g_selectedFile != -1) {
        g_fileDivs.eq(g_selectedFile).addClass('selected');
        
        if (animate) {
            // Scroll to file div
            if (typeof(api) != "undefined" && scroll) {
                var stickToTop = false; // Scroll as little as possible while.
                var animate = true;
                api.scrollToElement(g_fileDivs.eq(g_selectedFile), stickToTop, animate);
            }
        }
    }
}

// Called from Algodoo
function setFocused(focused) {
    if (focused && g_selectedFile==-1)
        g_selectedFile = 0;
        
    if (!focused || g_selectedFile==-1)
        g_fileDivs.removeClass('selected');
        
    if (focused && g_selectedFile != -1)
        g_fileDivs.eq(g_selectedFile).addClass('selected');
}

// Called from Algodoo
function reloadDir(scrollTo) {
    scrollTo = (typeof(scrollTo) != 'undefined' ? scrollTo : false);
    
    if (typeof(api) != "undefined")
        var oldScroll = api.getContentPositionY();
    else
        var oldScroll = $('body').scrollTop();

	$('.folder-container').html("");
	$('.path-container').html("");
	$('.path-container').append(clickableDirs(algodoo.dir));
    $('.scene-container').remove();

	addOpenFolder();
	addShowFolder();

	var sortHtml = "";
	sortHtml += '<p><form>';
	sortHtml += '<a href="#" onclick="selectSort(\'name\');">';
	sortHtml += '<input type="radio" name="sort_group" value="name"' + (algodoo.sort == 'name' ? ' checked="checked"' : '') + ' />';
	sortHtml += algodoo.Translate('BrowserSortByName') + '</a>';
	sortHtml += '&nbsp&nbsp&nbsp&nbsp';
	sortHtml += '<a href="#" onclick="selectSort(\'time\');">';
	sortHtml += '<input type="radio" name="sort_group" value="time"' + (algodoo.sort == 'time' ? ' checked="checked"' : '') + ' />';
	sortHtml += algodoo.Translate('BrowserLatestFirst') + '</a>';
	sortHtml += '&nbsp&nbsp&nbsp&nbsp';
	sortHtml += '<a href="#" onclick="setPlain();">';
	sortHtml += '<input id="plain" type="checkbox" value="plain"' + (g_plain ? ' checked="checked"' : '') + ' />';
	sortHtml += algodoo.Translate('BrowserNoImages') + '</a>';
	sortHtml += '</form></p>';
	$('.path-container').append(sortHtml);
		
	addHomeFolder();
	addUpFolder();

	var folders = algodoo.FoldersInDir(algodoo.dir);
	for (var i=0; i<folders.length; i++) {
		addFolder(folders[i]);
	}

	g_files = algodoo.FilesInDir();

    if (scrollTo) {
        // Roll back the file list when a file is deleted
        // Keep same page when file is deleted
    } else {
        // First page
        g_pageBegin = 0;
    }
    
    if (g_files.length <= FilesPerPage()) {
        $('#footer a').css({'visibility': 'hidden'});
    } else {
        $('#footer a').css({'visibility': 'visible'});
    }

    relistPage(true, oldScroll);

    if (scrollTo)
        g_imageRev++;
}

function clamp(x, min, max) {
    if (x < min) return min;
    if (x > max) return max;
    return x;
}

function changePage(next) {
    var oldPageBegin = g_pageBegin;
    
    if (g_files.length <= FilesPerPage()) {
        g_pageBegin = 0;
    } else {
        if (next) {
            if (g_pageBegin+FilesPerPage() < g_files.length) // If not all was already shown
                g_pageBegin += FilesPerPage();
        } else {
            g_pageBegin -= FilesPerPage();
        }
    
        g_pageBegin = clamp(g_pageBegin, 0, g_files.length-1);
    }
    
    if (oldPageBegin == g_pageBegin)
        return; // No change.
    
    relistPage(next);
    
    if (g_selectedFile != -1 && oldPageBegin != g_pageBegin) {
        var animate = false; // irritating
        setTimeout(function () {
            setSelectedFile(next ? 0 : FilesPerPage()-1, animate);
        }, 50); // Delay b/c relistPage:s api.scrollToY is delayed...
    }
}

function relistPage(next, scrollTo) {
    scrollTo = typeof(scrollTo) != 'undefined' ? scrollTo : 0;
    
    if (g_files.length <= FilesPerPage())
        g_pageBegin = 0;
        
    g_pageBegin = clamp(g_pageBegin,                  0, g_files.length-1);
    var pageEnd = clamp(g_pageBegin + FilesPerPage(), 0, g_files.length  );

    if (g_files.length == 0) {
        $('#file-info').text("0 / 0");
        g_pageBegin = 0;
        pageEnd = 0;
    }
    else {
        $('#file-info').text((g_pageBegin + 1) + "-" + pageEnd  + " / " + g_files.length);
    }
    
    var container = $('<div class="scene-container" />');
    var post = [];

    for (var i=g_pageBegin; i<pageEnd; ++i) {	    
        addFile(g_files[i], container, post);
    }

    var lastContainer = $('.scene-container');
    if (next) {
        $('#scene-containers').append(container);
        lastContainer.animate({"height": "0px"}, 0, function () {
            lastContainer.remove();
        });
    } else {
        container.css({'height':'0px'});
        $('#scene-containers').prepend(container);
        container.css({"height": "auto"});

        lastContainer.animate({"height": "0px"}, 0, function () {
            lastContainer.remove();
        });
    }
    
    // Add images for scenes without thumbnails.
    for (var i=0; i < post.length; i++) {
        algodoo.GetImage(algodoo.dir + post[i]).assignToHTMLImageElement(document.getElementById(post[i]));
    }

    if (g_plain)
        $('.scene-item').addClass('plain');

    if (algodoo.IsPlain())
        $('.scene-container').css({'margin-left':'0px'});

    g_fileDivs = $('.scene-container > div');
    
    if (typeof(api) != "undefined") {
        setTimeout(function () {
            api.reinitialise();

            // Scroll to top of page, or last position
            if (scrollTo == 0)
                api.scrollToY(scrollTo, true);
            else
                api.scrollToY(scrollTo, false);
        }, 50);
    } else {
        // Scroll to top of page, or last position
        if (scrollTo == 0)
            $('html,body').stop().animate({scrollTop: scrollTo}, 'normal');
        else
            $('html,body').stop().animate({scrollTop: scrollTo}, 0);
    }  
}
            
function delayedScrollToTop() {
    setTimeout(function () {
        api.reinitialise();
        api.scrollToY(0, true);
    }, 50);
}

$(document).ready(function() {
    if (!algodoo.IsTouchInput()) {
        createScroll();
    }

    //////////////////////////////////////////////////////////////////////////
    // GLOBALS
    
    // g_plain means "no images". algodoo.IsPlain() means "just show files, no folders etc".
    g_plain = readCookie("plain");
    g_plain = (g_plain == "true" && !algodoo.IsPlain());

    g_pageBegin = 0;     // The first file in g_file shown on the current page
    g_fileDivs = $();    // The file-elements on the current page
    g_imageRev = 0;      // Used to force re-load of images
    g_selectedFile = -1; // The selected file (if any).
    //////////////////////////////////////////////////////////////////////////
    
    var currentDir = readCookie(algodoo.dirId);
    if (currentDir != null) {
        algodoo.dir = algodoo.NiceDir(unescape(currentDir));
    }

    reloadDir();
  	$('img ').not('.draggable').bind('dragstart', function(event) { event.preventDefault(); });

    if (algodoo.IsPlain()) {
        $('#header').hide();
        $('.folder-container').hide();

        var palette = algodoo.GetPaletteName();

        g_fileDivs.find('h4').each(function (i) {
            if ($(this).text() == algodoo.ShownFileName(palette + '.cfg')) {
                g_selectedFile = i;
                return false;
            }
        });

        if (g_selectedFile == -1) {
            g_selectedFile = 0; // Select first file if no palette match
        }

        setSelectedFile(g_selectedFile);
        
        // Scroll to file div
        $('html,body').stop().animate({scrollTop: g_fileDivs.eq(g_selectedFile).offset().top - 80},'normal');
    }

    $('body').keydown(function (e) {
        if (e.keyCode == 13) { // Enter: open scene
            if (g_selectedFile != -1) {
                g_fileDivs.eq(g_selectedFile).find('> a').click();
            }
        } else if (e.keyCode == 113) { // F2: rename
            if (g_selectedFile != -1) {
                g_fileDivs.eq(g_selectedFile).find('.rename-button').click();
            }
        } else {
            var width = 1;

            if (g_fileDivs.length > 1) {
                var ground = g_fileDivs.eq(0).offset().top;
                var comp   = g_fileDivs.eq(1).offset().top;

                while (ground >= comp) {
                    width++;

                    if (width < g_fileDivs.length)
                        comp = g_fileDivs.eq(width).offset().top;
                    else
                        // Special case when only one row
                        comp = ground + 1;
                }
            }

            var scroll = false;
            var isArrowKey = (37 <= e.keyCode && e.keyCode <= 40);
            var oldSelectedFile = g_selectedFile;
            
            if (e.keyCode == 33) { // page up
                changePage(false);
                delayedScrollToTop();
            }
            else if (e.keyCode == 34) { // page down
                changePage(true);
            }
            else if (e.keyCode == 35) { // end
                scroll = true;
                g_selectedFile = g_fileDivs.length - 1;
            }
            else if (e.keyCode == 36) { // home
                setSelectedFile(0, true);
                delayedScrollToTop();
            }
            else if (isArrowKey && g_selectedFile<0) {
                g_selectedFile = 0; // Select first file.
                e.preventDefault();
            }
            else if (e.keyCode == 37) { // Left arrow
                if (g_selectedFile > 0) {
                    if (g_selectedFile % width == 0)
                        scroll = true;

                    g_selectedFile--;
                } else {
                    changePage(false);
                }
                e.preventDefault();
            } else if (e.keyCode == 38) { // Up arrow
                if (g_selectedFile > width - 1) {
                    scroll = true;
                    g_selectedFile -= width;
                } else {
                    g_selectedFile = 0; // First
                    changePage(false);
                }
                e.preventDefault();
            } else if (e.keyCode == 39 || e.keyCode == 9) { // Right arrow OR tab
                if (g_selectedFile < g_fileDivs.length - 1) {
                    g_selectedFile++;

                    if (g_selectedFile % width == 0)
                        scroll = true;
                } else {
                    changePage(true);
                }
                e.preventDefault();
            } else if (e.keyCode == 40) { // Down arrow
                if (g_selectedFile < g_fileDivs.length - width) {
                    g_selectedFile += width;
                    scroll = true;
                } else {
                    g_selectedFile = g_fileDivs.length-1; // Last
                    changePage(true);
                }
                e.preventDefault();
            } else if (e.keyCode == 46) { // delete
                if (g_selectedFile != -1) {
                    // Delete it.
                    var ix = g_pageBegin + g_selectedFile;
                    if (ix < g_files.length) {
                        eraseFile(g_files[ix]);
                        setSelectedFile(g_selectedFile, true);
                    }
                }
            }

            if (oldSelectedFile != g_selectedFile) {
                setSelectedFile(g_selectedFile, scroll);
            }
        }
    });

    $('#prevPage').click(function () {
        changePage(false);
    });

    $('#nextPage').click(function () {
        changePage(true);
    });

    if (typeof(api) != "undefined") {
        //setTimeout(function () {
		//    api.reinitialise();
		//}, 300);

        $(window).bind('resize', function() {
            api.reinitialise();
        });    
    }
});
