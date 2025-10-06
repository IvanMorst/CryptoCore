Algodoo, a 2D physics sandbox by Emil Ernerfeldt.
Copyright 2008-2012, Algoryx Simulation (www.algoryx.se).
Homepage: www.algodoo.com
Support:  support@algodoo.com
Contact:  contact@algodoo.com


For how to use the program, click the help button inside Algodoo or visit http://www.algodoo.com/wiki/Tutorials
If you lack a translation to your language, go to http://www.algodoo.com/wiki/Translations

Trouble shooting:
	* Check http://algodoo.com/wiki/FAQ
	
	* If Algodoo has started acting strange lately, try resetting it.
		The easiest way is to, in Algodoo, go to Options->Reset and click "Reset configuration...". You should get a message saying "Algodoo has been successfully reset to factory settings.".
		If you fail to find this button, try this: First close Algodoo, then:
			On Windows: Click "Reset Algodoo" under Start menu->Algodoo.
			On Linux/Mac: execute "algodoo -reset".
		If all this fails, go to your Algodoo home directory ("My Documents/Algodoo/" in Windows, "~/Library/Application Support/Algodoo/" on MacOS or "~/Algodoo/" in Linux) and delete "config.cfg", "config.autosave.cfg", "scenes/_ONEXITSAVE.phz" and "scenes/_AUTOSAVE.phn".

	* If you have trouble with fullscreen in Windows, try pressing Win-m (minimize all) and then bring Algodoo to front.
	
	* If you have problems running the program, or having problem with a stutter and low framerate, follow these steps one at the time:
		- Download and install the latest graphics drivers for your computer (IMPORTANT!)
		- Set your monitor bit depth to 32-bits (or set Algodoo to 16 bit by adding "System.depth = 16;" to config.cfg, see below)
		- Disable any secondary monitors

		Try Algodoo again, if no success, try these things:
		- Navigate to your Algodoo installation folder (where this README.txt can be found).
		- Open "config.cfg". At the end of config.cfg, add these lines:
			Resources.shaders = false;
			System.fullscreen = false;       // or try true
			System.resolution = [1024, 768]; // or your default screen resolution
			System.zDepth = 16;              // or try 24, or 32.
			System.depth = 24;               // or try 16 (32 default). The higher, the better.
			System.vSync = false;
		- Save config.cfg (either to the installation folder or to "My Documents/Algodoo/" in Windows, "~/Library/Application Support/Algodoo/" on MacOS or "~/Algodoo/" in Linux).
		- Try Algodoo again. If still no luck, play around with the config.cfg settings some more.


Changelog:

=== Algodoo 2.1.0, 2013-0?-?? ===
* NEW: Custom-textured springs
* NEW: More scripting:
** onClick  - called when user clicks an entity
** onKey    - called on each key press
** onSpawn  - called when an entity is created
** onDie    - called when an entity is killed
** postStep - called after each simulation step
** update   - called each frame
* IMP: Quicker rendering
* IMP: Faster solver
* FIX: A lot of fixes and tweaks

=== Algodoo 2.0.2, 2012-03-27 ===
* NEW: Plot now calculates (and visualizes) the integral on mouse-over.
* NEW: Added support for plotting acceleration and force for an object.
* NEW: Drag tool options are now serialized to scene.
* NEW: Entity info window now show position.
* NEW: Added ability to bind analog joysticks to thrusters and hinge motors.
* NEW: Replaced "Big buttons" checkbox with a slider to let the user choose any scale between 0.5 and 2.0.
* NEW: Scene thumbnail preview in save window.
* NEW: Paste images right into Algodoo.
* NEW: Wind (available in air menu).
* NEW: Direction picker for gravity, wind and object velocity.
* NEW: pos/angle/vel/angvel scriptable attributes. e.g: "vel = {- pos}"
* NEW: Thyme keyword 'entity' - get the owning entity of a scripted attribute (replaces 'owner' keyword).
* NEW: Sim.scriptUpdatesEveryStep - if true, scripted attributes gets executed on every simulation step (rather than just once per frame). True by default.
* NEW: Thyme functions: System.WriteToFile, System.ReadWholeFile, string.Split
* IMP: Better file browser file selection (use arrow keys).
* IMP: One can now delete the selected file in the file browser by pressing 'delete' button on keyboard.
* IMP: One can go to the next page of scenes with PageUp/PageDown.
* IMP: Larger scene browser and Algobox windows.
* IMP: Large values in script menu will now collapse/expand on click.
* IMP: Removed extra zeros from floating point values in console and script menu (e.g. 0.0000000 becomes 0.0).
* IMP: Slight optimization of floating point parsing (and thus loading of scenes with lots of polygons).
* IMP: Plot 'head' now drawn at current value.
* IMP: Nicer drawing of Plot text (mouse over and legends).
* IMP: Some issues with white skin now resolved.
* IMP: Options->Skin->Color now does more to change the skin color.
* IMP: The unlock menu will now automatically go and fetch unlock information from clipboard buffer (if available).
* IMP: Less window-wobble.
* IMP: Widget connector now fades with widget.
* IMP: Made Algodoo slightly less eager to automatically generate geometry from dropped texture.
* IMP: Air friction will now be applied to a more accurate position for polygons.
* IMP: In the file browser F2 can now be used to rename the selected file.
* IMP: Script menu readables now update their values.
* IMP: Plot window now keeps clear button icon even when side bar is contracted.
* IMP: Holding down SHIFT or ALT when clicking plot clear button or sidebar contract button will now apply it to all open plot windows.
* IMP: Older plot lines now fade slightly to distinguish from newest measurement.
* IMP: Dragging a slider will no longer show its tooltip.
* IMP: On touch screens, it is now easier to hit nice round values when dragging a slider.
* IMP: Widget visibility button now opens sub-menu instead of hiding windows right away.
* IMP: Gravity/air/grid options now only opens on right-click, double-click and click-hold.
* IMP: Reorganized axle menu.
* IMP: Improved collision detection between polygons with circular outer shell vs polygons and circles. A circle and a circular polygon should now behave equally in all situations.
* IMP: Added options to visualize force/velocity/momentum to velocity menu. Also added button for quick-access to right side bar options for these things.
* IMP: Better scene thumbnail scaling.
* IMP: Removed startup splashscreen for unlocked (bought) Algodoo.
* IMP: Air friction force arrows are now shown even while scaling or rotating an object.
* IMP: Scene scale indicator now has a subtle shadow for increased visibility.
* IMP: You can now use a comma as decimal separator when entering numbers to sliders.
* IMP: You can now use mathematical functions (sin, cos, pi etc) when entering numbers to sliders. (e.g. "atan(0.5)*180/pi")
* IMP: Chain tool will preview when the created chain will bite its own tail.
* FIX: Cloning of scripted attributes referencing geometries.
* FIX: Scaling will no longer affect scripted attributes.
* FIX: Checkboxes are now as wide as the containing menu (in most places).
* FIX: Improper undo/serialization of spring impulse, sometimes leading to 'explosions' on undo.
* FIX: Broken undo of hinge/laser/thruster/destroy/mirror button bindings.
* FIX: Thumbnails not under the home folder are again shown.
* FIX: Bug causing kinetic and potential energy calculations to be out of sync, making it appear in the plot as if the total energy was not constant.
* FIX: Translation of "ReloadScene" button. 
* FIX: Error with scripted drawBorder attribute.
* FIX: Potential and total energy calculations now take air buoyancy into account.
* FIX: Issue with Ctrl-A selecting text instead of entities.
* FIX: Controller widget options hiding.
* FIX: Hinge tool will now try to connect selected objects first.
* FIX: Fixed context menu will now also be hidden in Play Mode.
* FIX: Blinking axle motor/brake indicator.
* FIX: Sim.airFrictionVersion not being reset to default after closing old scene.
* FIX: Better handling of the case when user switches on velocity/momentum arrows before anything moves.
* FIX: Non-ASCII characters now work again when renaming files (scenes, components etc).
* FIX: Load screen flicker on WinXP.
* FIX: Bug causing the changing of default material to sometimes change the color of all objects in the scene.
* FIX: Unnecessarily wide force view menu.
* FIX: Changing skin in Welcome menu will now adjust (reset) window positions.
* FIX: Hinge motor torque visualization.
* FIX: Finite velocity lasers not going all the way to their fade distance.
* FIX: Contact arrow force direction (I think).
* FIX: Multi-touch support (Windows only).
* FIX: Fixed some problems with finger-shifting on SMART boards.
* FIX: Saving scenes with names containing new-line characters.
* FIX: You can no longer save scenes without a title.
* FIX: Dropping textures onto a plane will now wrap the texture.
* FIX: Grid options not showing right number of axes.
* FIX: Re-uploading a scene on Algobox will no longer reset the scene group or allow-comments/responses/ratings.
* FIX: Better visualization of large force arrows (clamped to screen size).
* FIX: Bug causing rounding errors in body velocities on scene load and undo.


=== Algodoo 2.0.1, 2011-12-21 ===
* NEW: Object can now have custom script variables that are properly serialized and cloned (they must start with an underscore, e.g. "_size := 15").
* NEW: Both "color" and "colorHSVA" now serialized, making both scriptable.
* NEW: Move selected objects half a pixel at the time using the arrow keys (only when simulation is paused).
* NEW: Move selected objects to front/back with SHIFT + down/up arrow keys.
* NEW: Improved script menu with readables and cmd result.
* NEW: Thyme command Scene.entityByID, (e.g. (Scene.entityByID(21)).color)
* NEW: Thyme command Scene.entityByGeomID
* NEW: Thyme functions Math.log10 and Math.log (natural base).
* NEW: Geometry generation from opaque images (background removal). Works best with clip-art like images.
* NEW: Added check/uncheck all buttons to options->layers as well as to the force visualization menu.
* NEW: Added helpful Thyme command "Scene.MakeModern" to update a scene:s settings to the modern Algodoo version. Will change simulation settings and legacyMode:s.
* NEW: Algodoo now uses CrashRpt (Windows only) to catch most crashes and ask the user to send in a crash report to Algoryx.
* NEW: Ctrl-D now deselects everything in the scene.
* NEW: TAB now toggles hide/show windows.
* NEW: Play mode, accessible with button in menu-bar, or SHIFT-space.
* NEW: When loading a scene, a popup will show the scene description, if any.
* IMP: A polygon with a circular outer shell will now roll much smoother on planes and boxes.
* IMP: Positioning of long undo/redo lists.
* IMP: Loading screen no longer stays on top of all other windows.
* IMP: Spring end-points can now be behind the geometry it is connected to (by popular request).
* IMP: Improved support for drag-and-drop of images from web browser into Algodoo. It now works with Chrome, Firefox and Safari (but NOT Internet Explorer) on both Windows and Mac.
* IMP: Added popup message when failing to rename a file in the file browser.
* IMP: Algodoo now always starts full screen after first install.
* IMP: User textures will now be copied to Algodoo/textures/ directory.
* IMP: Improved culling of small force/velocity/momentum arrows.
* IMP: Sim.positionsLast now true by default, fixing issue where the force arrows of moving objects would be wrong when simulation was paused.
* IMP: Re-enabled undo-merging of certain actions (drag, move, slider, texture, palette) when done within 10 seconds of last action of same type. Control with App.enableUndoMerge.
* IMP: Nicer splash screen/about window with links to algodoo.com/algoryx.se
* IMP: Rotating an object around a hinge will no longer re-attach the hinge (or fixate).
* FIX: Loading screen translucency now disabled on Windows XP.
* FIX: Turning a circle into a polygon (for instance by scaling or doing CSG) will now conserve its area (used to be off by about 0.1%).
* FIX: Bug causing rotate not to be undoable.
* FIX: Bug where moving a spring would sometimes change it's strength and/or damping.
* FIX: Popups will now steal focus (from e.g. text boxes).
* FIX: Can't drag windows with right mouse button.
* FIX: Some instances where the file browser could crash Algodoo.
* FIX: Loading files with non-ascii letters.
* FIX: Thyme command "readable" now works properly when loading and cloning objects.
* FIX: Sim.targetPenetration for old Phun scenes.
* FIX: Chain tool now previews length when holding down SHIFT.
* FIX: Chain tool now build chain as soon as SHIFT is up.
* FIX: Rare corner-case issue where a laser would pass right through the diagonal of a box or box-like polygon.
* FIX: Better handling of lasers at shallow angle of incidence.
* FIX: Correct preview of laser beam when cloning a laser pen.
* FIX: Random laser pen color will now always be visible against the sky.
* FIX: Bug when calculating rotational kinetic energy for bodies that made it appear as if energy was increasing when in fact it was not.
* FIX: Scene save overwrite dialog's "Save as foo_0000.phz" not working.
* FIX: Chain tool drawing in white even on white background.
* FIX: Some start up issues.
* FIX: Rare source of crash that could occur when unlocking Algodoo on Windows.
* FIX: Entering a bad serial key temporarily re-locking an already unlocked Algodoo.
* FIX: Total force arrow color (once again it is red).
* FIX: Issue with drag-and-drop of components from the component browser.
* FIX: Issue with Algodoo claiming no Internet connection when browsing own scenes/components (caused by failure of finding "My Documents" for whatever reason).
* FIX: When a tutorial highlights a button in the GUI, the window containing the button will be moved on top of other windows.
* FIX: Saving a scene as alternative file name (e.g. "foo_0000.phz") will now change the scene title.
* FIX: Premature culling of hinge force arrows.
* FIX: Issue with invalid characters in scene file name.
* FIX: Issue with expanding force description fields.
* FIX: Rare issue with large text fields not drawing top part.
* FIX: A bug that would sometimes cause Algodoo to crash on startup.
* FIX: Issue where some bad polygons would make Algodoo hang.
* FIX: Startup crash involving http://www.algodoo.com/algobox/details.php?id=59214
* FIX: Issue with fullscreen toggle moving the window outside the monitor.
* FIX: Only one of: Splash, Welcome and About windows will be shown at startup.
* FIX: Issue with clicking a folder in the scene browser when the view has been scrolled down a bit.
* FIX: Opening a sidebar widget will now give keyboard focus to the component (allowing, for instance, selecting the new scene template with arrow keys/enter).
* FIX: Issue with incorrect undo of attraction falloff (and possibly other attributes).
* FIX: Bug where using scale tool would change selection after scaling was completed.

=== Algodoo 2.0.0 (RC6 / GOLD), 2011-10-18 ===
* FIX: All side bar windows can now be detached.
* FIX: Issue with welcome guide on small screen resolutions.
* FIX: Thyme: "vel" and "angvel" now always accessible with 'readable'.
* FIX: Thruster resize box size.
* FIX: Undo no longer combines actions.
* FIX: Load screen no longer fades on Windows XP and earlier (produced flicker for some).
* FIX: Issue with detached side bar widgets lingering after being closed.
* FIX: Windows: Algodoo reset not showing popup message on top.
* FIX: Empty tool window for pan/zoom tools.
* FIX: Thyme: code in {}-based attributes being run even after object is no longer in scene.
* FIX: Automatic language detection on Mac.

=== Algodoo 2.0.0 RC5, 2011-10-14 ===
* NEW: Thyme command App.AddUndoPoint - good for save points in games.
* NEW: Thyme command 'readable' to read volatile entity attributes (e.g. "(readable e.other).pos(0)")
* NEW: Thyme command 'owner' to get owner scope from {}-scripted attribute (e.g. "color = {p := (readable owner).pos; [p(0), p(1), 1, 1]}")
* IMP: You can now select a spring without the endpoints by holding down ALT.
* IMP: Better looking spring selection outline.
* IMP: Nice connector between side menu and open widget.
* IMP: Nice preview when trying to detach side bar widget.
* IMP: Sub-menus to the Edit menu must now be tugged quite a bit before detaching.
* IMP: Better handling of end-point depths.
* FIX: Issue with spring tool connecting springs to existing line end points even when those where covered by a geometry.
* FIX: Moving a spring now suspends the bodies it is attached to.
* FIX: Issues with changing line end point sizes.
* FIX: Scaling sometimes expanding hinges, springs, etc.

=== Algodoo 2.0.0 RC4, 2011-10-11 ===
* IMP: Some more language choices.
* IMP: Removed bug reporter (still available with F8 key press).
* FIX: Crash at startup for some.

=== Algodoo 2.0.0 RC3, 2011-10-07 ===
* IMP: Made find-texture window resizable.
* IMP: Starting Algodoo for the first time can be slow, so now a special loading message is shown for this case.
* IMP: Loading messages now always show for a couple of second to give you time to read the tips in them. Close by clicking anywhere.

* FIX: Spring selection ghost point positioning.
* FIX: Expanding script menu.
* FIX: gif/jpeg loading on Windows.
* FIX: Issue with "New Scene" window suddenly getting a scroll bar when one was not needed.
* FIX: Issue with thyme scripts sometimes not finding built-in functions.
* FIX: Pressing new scene, then undo will no longer reset textures to white.
* FIX: Loading scenes overriding default textures (e.g. "wood") even after the user opens a new scene.
* FIX: Issue with pressure sensitivity with tablets.
* FIX: Issue with palm erase on SMART boards.

=== Algodoo 2.0.0 RC2, 2011-10-05 ===
* NEW: Added button in plot window to hide the left side bar, giving more screen space to the actual graph.
* NEW: The right hand side appearance and material menus can now be detached.
* NEW: Licence system. 
** All older licenses will unlock Algodoo for Education.
** Support for subscription licenses.

* IMP: Color samples always have borders (looks nicer!)
* IMP: Better mac touch-pad support:
** A zoom threshold makes it easier to pan without accidently zooming.
** Pressing down the trackpad will disable two-finger pan/zoom.
* IMP: Algodoo will now lower GUI.scale if the window gets too small, allowing all windows to fit nicely even on the small screens of netbooks.
* IMP: Algodoo will now use less video memory for textures, allowing it to run on older hardware.
* IMP: Algodoo will now start even faster.
* IMP: If shaders aren't supported (or turned off), Algodoo will now use gluBuild2DMipmaps over GL_GENERATE_MIPMAP/glGenerateMipmapEXT to increase compatibility with older hardware.
* IMP: Window resizing.
* IMP: The scene browser now has pages if there are too many scene in a folder (over 48 at the moment).
* IMP: Selecting 'No images' is now remembered in the scene browser.
* IMP: To scroll on touch screens you now simply drag the component with your finger.
* IMP: Added small threshold making moving windows by mistake less likely.

* FIX: F11 fullscreen.
* FIX: Hinge motor selection size.
* FIX: Null polygons (e.g. "scene.addpolygon{surfaces := [[[0,0],[0,0],[0,0]]]}") hanging Algodoo.
* FIX: A thyme-related memory leak.
* FIX: Hinge/laser keys activating even if simulation was paused.
* FIX: Fixed problem that would cause slowdown when moving the mouse a lot.
* FIX: Problem with force/velocity arrow scales from scenes made before 1.7.9
* FIX: Problem where font size in open scene/phunlet/texture menu would be unrelated to global font size.
* FIX: Planes now snap to the grid correctly again.
* FIX: Lingering mouse-over effects when mouse was not over Algodoo window.
* FIX: Selecting tracers would sometimes make whole scene black.

=== Algodoo 2.0.0 RC1, 2011-09-23 ===
* NEW: Clicking the pan/zoom buttons in the sim control now also acts like tool buttons. Clicking them twice returns you to previously selected tool.
* NEW: Added thyme command Scene.RemoveEntity, e.g. "onCollide = (e)=>{Scene.RemoveEntity(e.other)}".
* NEW: Added "New scene" button to scene bar where one now get to choose the palette of the new scene.
* NEW: Thyme: Added support for C# style string literals that starts with @" and ends with ".

* IMP: Tool cursor now reflect which tool is in use, not which is selected.
* IMP: Added Sim.stepsPerFrame to improve screen capture smoothness.
* IMP: Plot now draws on top of axis for greater clarity.
* IMP: Velocity component sliders now go from negative to positive 25 m/s.
* IMP: Sizing of axles/fixates/lasers/tracers/thrusters.
* IMP: If Algodoo runs out of memory, it will now try to free up some and then show a helpful error message. You can also manually free up memory with App.FreeUpMemory.
* IMP: Rope color now follows palette.
* IMP: Improved air friction widget with new explanation and correct units.
* IMP: When applying a palette to a scene, each chain will be given just one random color.
* IMP: The current palette is now saved with the scene.
* IMP: Optimizations.
* IMP: Added error message for when user don't have Internet connection.
* IMP: Collision callbacks (onCollide) are now called every simulation step rather than every frame if Sim.collideCallbacksEveryStep is true (false for old scenes).

* FIX: Context menu buttons not filling the full width of the menu.
* FIX: Issue with objects moving while scaling them if simulation was running.
* FIX: Dragging the clone button now places the clone under the mouse cursor (again).
* FIX: Changing palette would not change palette preview or slider colors.
* FIX: Key bindings eating input, denying it elsewhere (especially clicking).
* FIX: Fullscreen toggle with F11 sometimes not working.
* FIX: Bug making it impossible to look at the energy of geometries with infinite inertia.
* FIX: Some issues with resitution=1 leading to energy increase.
* FIX: Spring can again snap to the middle of a circle when the grid is on.
* FIX: Optimized scenes with many and/or long tracers.
* FIX: Floats again always serialized with a dot so that there is no confusing them with integers on deserialization.
* FIX: Closing the color menu when auto-apply palette is set will no longer re-apply the palette to the scene.
* FIX: Objects with 0 and inf friction now has infinite traction (again) to fix http://www.algodoo.com/algobox/details.php?id=27343.
* FIX: Springs from old scenes will now have the endpoints at proper depth.
* FIX: Positioning of side menus to always be inside screen.
* FIX: Restored laser fade distance slider.
* FIX: Issue with serialization of stretched chains.
* FIX: Jerking of stretched ropes when freezing their velocities.
* FIX: Laser events now sent at most once per simulation step.

=== Algodoo 1.9.9.9 beta, 2011-09-07 ===
* NEW: Scenes can now be browsed without images.
* NEW: Added support for anisotropic filtering to improve quality of stretched textures (mainly springs). Control in Options->Rendering.
* NEW: Added optional smoothing to plots.

* IMP: Moving a spring endpoint will now only insta-move it if it is attached to background or other static body.
* IMP: Language is now changed in options rather than the file menu.
* IMP: Made the material icons slightly smaller.
* IMP: Entering negative speeds in velocity menu will now flip direction of movement.
* IMP: Changed drag tool's "center of mass" feature and added a "Disable rotation" checkbox.
* IMP: Cloning glued geometries will no longer glue the objects to the originals.
* IMP: Drawing of stretched axles.
* IMP: Larger tool text.
* IMP: Rope tool now draws total length so far.
* IMP: Rope tool now temporarily suspends the movement of bodies it is working on.
* IMP: Setting default material will now also reset texture and color, if a previous material had been set.
* IMP: Undo now only merges drag/move etc if less than 10 seconds between them.
* IMP: Better sizing of axles, fixates, thrusters, lacers and tracers when clicking small objects, or choosing "Add center X".
* IMP: ctrl-s will now save the scene right away if it has been saved previously. ctrl-shift-s brings up the save dialog.
* IMP: Optimized drawing of selections.
* IMP: Scenelets officially renamed 'components'.
* IMP: Translated welcome scene ("Quick tour").
* IMP: Windows installer no longer hassles you about existing Algodoo directory after you uninstall old version.
* IMP: Direct solver disabled for springs by default, for greater speed.
* IMP: One can now enable and disable the direct solver for individual hinges/springs in the script menu.
* IMP: Optimizations!

* FIX: Spring line end point colors.
* FIX: Overkill 17 decimals of precision in script menu, console and when serializing.
* FIX: Parsing of floats ending with the "." (e.g "10.").
* FIX: Force visualization was accidently on for all thrusters/springs when enabling it for just one geometry.
* FIX: The tutorial window can now be minimized without losing the current lesson.
* FIX: The prev. button in the lesson tutorials could sometimes be disabled when it shouldn't.
* FIX: The prev. button in the lesson tutorials now also scrolls the view.
* FIX: The highlighter is now removed when the help widget is closed when running a lesson.
* FIX: Box "textConstrained" attribute being ignored.
* FIX: Issue with drag-dropping scenelets with tracked group.
* FIX: Issue with line end points moving to front when-ever they where moved with mvoe tool.
* FIX: Annoyance where resizing a window would sometimes move it.
* FIX: Scene.my.* declarations are done at top of the scene file now so they can be referenced later on.
* FIX: Direction of spring force arrow.
* FIX: Made it easier to click text fields (like slider values).
* FIX: Bug causing growing context menu.
* FIX: Optimized circle shader.
* FIX: Resizing the inner hinge of a gear will no longer detach it.
* FIX: Removed "infinity" as the maximum hinge motor strength. You can still enter "+inf" manually.
* FIX: Issue with Thyme parsing which would sometimes cause string literals to be wrongfully regarded as languange identifiers, causing unparsable thyme files.
* FIX: "Vibrating" controller menu when resizing the controlled geometry.
* FIX: issues with button input (for motors, lasers etc). They will no longer be activated if ctrl is down (e.g. ctrl+z will not activate a laser bound to z, but pressing only z will activate it).
* FIX: Issue with "Stop following object" button.
* FIX: Renaming a scene was very slow when a lot of scenes was in the same folder.
* FIX: Bug causing wrong velocities for composite bodies when undoing or loading a scene.
* FIX: Problem causing different air friction depending on whether two object where hinges or fixated/glued together.
* FIX: Issue drag-dropping in old phunlets.
* FIX: Bug causing motored hinges to behave differently after an undo.
* FIX: Issue where rope tool would sometimes create ropes with "gaps" in it.
* FIX: Issue with fixates rotating when using drag-tool.
* FIX: Issue with blinking tooltip.
* FIX: Problem with per-geometry force/vel/momentum visualization on glued geometries.
* FIX: Sizes of springs and their endpoints when loading old scenes.
* FIX: Fixed issue with popup-menus closing even though a slider in them where being dragged.
* FIX: Fixed issue with move tool changing selecting but not including that change of selection in its undo.
* FIX: The Mac version can again open scenes from the install directory (e.g. Official, Games & Phun).
* FIX: Issues with auto fitting force, velocity and momentum arrows.
* FIX: Problem with opening the text menu for several boxes containing markup.
* FIX: Issue where dragging the ends of a HTML window would sometimes not resize it.

=== Algodoo 1.9.9 beta, 2011-08-17 ===
* NEW: You can now select a material in the right-side menu, and all new objects will get that material.
* NEW: Added icon for resetting to default material.
* NEW: Added sliders for controlling strength of chains.
* NEW: Added button for reloading a scene in the save scene widget.
* NEW: Added button to clear file filter field.
* NEW: Added checkbox in force visualization menu controlling if Algodoo may use a slightly different solver when visualizing forces so as to improve force arrow stability.
* NEW: Scenes and scenelets can now be renamed in the scene browser.
* NEW: Added "New scene" button to scene widget.
* NEW: Added "Check all"/"Uncheck all" buttons to collision menu.
* NEW: New color picker!
* NEW: You can now set water color in the appearance menu (when some water is selected).
* NEW: Options to draw arrow components and/or angles.
* NEW: Checkbox for turning kinetic panning on/off.
* NEW: Added slider for controlling plot time span.
* NEW: Drag tool has sliders for strength and max force.
* NEW: Drag tool checkbox for dragging center of mass.
* NEW: Added buttons for hiding the on-screen menus.

* IMP: Shortened titles for the submenus of the edit menu.
* IMP: Window names of the right hand side menus now explain what you are changing settings for (selected or new).
* IMP: Material menu now shows currently selected material(s).
* IMP: Made glass more translucent.
* IMP: Changed default laser color to be a random fully saturated color.
* IMP: Fixed filtering and sorting for folders in scene/scenelet browser.
* IMP: Removed title bar from file menu, and made immovable.
* IMP: A step can now be clicked in a lesson to jump directly to the step.
* IMP: Lowered default chain strength to 1e5 (making them softer, but more stable).
* IMP: Slider values now use a nicer form of scientific notation for large numbers. "12000000" will now display as "1.2 * 10^7" (instead of "1.200000000e+007").
* IMP: Algodoo will now guess Algobox ID for scenes downloaded from Algobox based on file name.
* IMP: More collision layers.
* IMP: When moving a spring end point, the spring will not re-attach to anything until the move is complete.
* IMP: Springs can attach a geometry to itself now.
* IMP: Rope breakage much better now: a rope will break at only one point per time step.
* IMP: Move to front/back undoable.
* IMP: Nicer plot window.
* IMP: Tool cursor hide when mouse is over a window.
* IMP: When selected, all objects will now show in some way, even if very small or very thin.
* IMP: Adjusted strength of refracted light, as light is broken up into the colors of the rainbow. This makes rainbows dimmer and more beautiful. Set with App.rainbowSplitMult.

* FIX: Fixed some issues with the SimControl popup menus.
* FIX: Clicking a phunlet will open it in middle of scene instead of under mouse.
* FIX: Bug where the borders around non-geometries would sometimes be larger than the objects.
* FIX: material velocity.
* FIX: When returning to the help menu from a lesson, the lesson is now stopped.
* FIX: Right hand side visualization menu bugs.
* FIX: Some issues with scenelet drag-dropping into and out of folder other than the default.
* FIX: File browser path is kept relative to Algodoo folder for as long as possible.
* FIX: Geometry airFrictionMult should no longer affect air buoyancy.
* FIX: Kibibyte unit symbol (KiB instead of kiB).
* FIX: Bug causing the button "toggle" state to... toggle.
* FIX: Backspace once again deletes objects rather than undoing.
* FIX: The undo/redo menus now opens with the most recent items closest even when the Sim control menu is at the top (default is bottom).
* FIX: Rare Thyme problem with integers larger than 2147483647 not being parsable. They are now treated as floats.
* FIX: System.maxFPS not working.
* FIX: Folders with apostrophes and quotation marks can now be opened.
* FIX: Hiding and showing all windows will no longer re-maximize all opened windows.
* FIX: Scenes with non-ascii characters can again be opened and deleted on the Mac.
* FIX: Algodoo now remembers and restores last screen position (and size).
* FIX: When reading old scene with springs, the spring end points will now get the attributes of the old spring (fixing issues with mirror button not working for spring in old scenes).
* FIX: Issue with spamming of messages "Switching to fallback ..." and "Polygon transparency not fully supported by your computer...".
* FIX: Spring end points now always have the color of what they are attached to, but keeps own alpha.
* FIX: Left sidepanel menus can no longer be moved or minimized.
* FIX: Bug causing "send into orbit" to be oblivious to collision groups.
* FIX: When holding down shift and using the brush or eraser, nothing will be drawn/erased until shift is let go.
* FIX: Issues with settings lingering from old versions.
* FIX: Springs will again snap to the center of circles.
* FIX: Added hard limits to positions and velocites in Sim.limit*. Useful when there are no killer planes.
* FIX: An issues with the visualization of the scale center when using the scale tool.
* FIX: Very thin polygons being invisible.
* FIX: Fixed issue with Algodoo crashing when pressing Shift+5 and other such combos in a button selector.

=== Algodoo 1.9.8 beta, 2011-07-21 ===
* NEW: Removed "cute clouds" feature.
* NEW: The text for the lessons have been moved to the translation files and can therefor be translated.
* NEW: The zoom factor can now be set in the options (especially useful for users with a Magic Mouse).
* NEW: The fade out of the clouds can now be turned off (App.Background.fadeCloudsOnSimStop).
* NEW: Added a button to file browser to show the current folder in the OS file browser.
* NEW: Kinetic panning (scrolling) - throw the camera to quickly pan.
* NEW: Added support for Mac touch-pads
** Use two-fingers for panning and zooming.
** Swipe with three fingers to undo, redo, play/pause and minimize/maximize windows, or go back/forwards in a browser.
* NEW: Home dir button in scene save dialog.
* NEW: The Windows installer will now ask to uninstall the previous version of Algodoo first.
* NEW: When deleting files from within Algodoo, they will now be moved to the recycle bin.
** When you overwrite a scene on save, the old version will be moved to the recycle bin, unless you set App.moveToTrashOnOverwrite to false.
* NEW: The Algobox browser now shows the URL for easy sharing of scene url:s.
* NEW: You can now use back/forward button on your mouse or keyboard to undo/redo in algodoo, as well as navigate the browsers.
* NEW: Added selected tool icon to cursor  -  congratulations, tatt ;)

* IMP: Algodoo once again uses single precision float math (it was double during the earlier betas). This will speed up most things.
* IMP: More responsive panning.
* IMP: Reduced the size of the tool options widget.
* IMP: Moved the lessons into the help widget and they are dynamically added.
* IMP: Nicer slider rendering using customizable borders.
* IMP: Algodoo now loads (much) quicker.
* IMP: Smoother load screen with version number.
* IMP: Moved "Use as chain" up to the first part of the context menu.
* IMP: Made rope texture power-of-two for greater speed, quality and compatibility.
* IMP: Chain tool will now extend existing chain starting at the point where user drags rather than the edge of that geometry.
* IMP: Pressing the "Show scene on Algobox" will now open the scene in the Algobox browser
* IMP: Back/forward buttons will now gray out when not applicable.
* IMP: Better image scaling in scene, scenelet and texture browser, improving both image quality and load times.
* IMP: The thumbnail folder created by the file browser is now hidden in Windows Explorer.
* IMP: For clarity, stretched hinges are now blurred along the axis of elongation. Thanks for the idea, Kilinich!
* IMP: Much nicer selections for all non-geometries.
* IMP: Plot now has a helpful grid as well as guide-lines to the axes on mouse-over.
* IMP: Drag tool is now stronger when you zoom out. Control with Tools.DragTool.strength.
* IMP: Slightly better GUI responsiveness.
* IMP: Fixate and hinge tools now adjusts the size of the fixate/hinge based on the size of the involved object(s).
* IMP: Turned off font anti-aliasing, making text more readable on macs.
* IMP: Lowered default chain/rope strength from 1e7 to 1e6 N/m, which should solve most of the "exploding ropes" bugs.

* FIX: Air friction multiplier sometimes getting ignored for rotational air friction.
* FIX: Bug which would cause over-streched hinges to mess up the conservation of angular momentum, causing things like unrotatable objects.
* FIX: Black text on the background now has a white shadow.
* FIX: The Mac version draws the graphics more smoothly again.
* FIX: The global scenes (located in the install directory) should now be reachable through the file browser.
* FIX: The direction of the chain (and rope) is now always created the same way (so it doesn't look weird).
* FIX: Some fixes to how the endpoints are drawn.
* FIX: Misaligned planes snaps to the grid again.
* FIX: Small, low-density objects would sometimes get a rotation out of nowhere.
* FIX: Unintentional auto-brake on all hinges. Hinges will no longer auto-brake unless they are created by the chain tool.
* FIX: The resolution is now saved correctly.
* FIX: Fixed first welcome scene showing up in weird maximized-but-not-really mode on Windows.
* FIX: Opening the contect menu for a spring will now open the spring sub-menu again.
* FIX: Removed "clone" and "mirror" buttons for the end points of springs.
* FIX: Infinite inertia multiplier will no longer erase objects.
* FIX: The "show file" button (when saving plots) is working as it should again.
* FIX: Material velocity re-enabled for geom-geom contacts.
* FIX: Erasing of non-.phz files from file browser.
* FIX: Better snapping when moving thrusters, lasers, hinges, fixates and springs.
* FIX: Minor issue with closing polygons.
* FIX: Undo list order (bottom-up now).
* FIX: Fixed bug where the simulation would pause when moving something on top of a window.
* FIX: Legacy border width.
* FIX: Issues with rope (extra hinges and groups).
* FIX: Issues with selecting just the end-points of a chain: you can now always select just the end lumps of a chain to tug it or attach it somewhere else.
* FIX: Issue with tooltip positioning.
* FIX: Backing up Algodoo with Time Machine on the Mac should be working now.


=== Algodoo 1.9.7 beta, 2011-06-23 ===
* FIX: The undo list was sometimes placed wrong.
* FIX: The materials menu does not cause the screen to go black when a plane is selected any more.
* FIX: The white rectangles problem should finally be gone for every graphics card.
* FIX: Images other than PNG can now be displayed (smilies for instance).
* FIX: Tweet and Like button should now be able to open a new browser window to be able to log in.
* FIX: The config should be able to load again.
* FIX: The fixed context menu is now shown when resetting the windows.
* FIX: New scene now pause the simulation again.
* FIX: The shrinking of sim-settings and force-settings should now be working.
* FIX: Rulers no longer make everything transparent.
* FIX: The killer planes is again added when a new scene is created and unchecking the button removes them all.

* IMP: A ground plane is now added when a new scene is created, but not when clear scene is pressed.
* IMP: The welcome screen has been reworked and shows up every time Algodoo starts, unless "Do not..." is marked.
* IMP: Reworked the border size a bit.
* IMP: The clouds have been reworked a bit.
* IMP: The Mac version is now working well enough for a beta.
* IMP: Some widgets have been reduced in size.
* IMP: Scenes can now be delete in the scene browser by clicking on the red X in the corner (when mouse over).

* NEW: Added a feedback button.
* NEW: Added a button to open the welcome screen again in options.
* NEW: The eraser tool is now in the tutorials.
* NEW: The welcome scene has been renamed Quick tour and some helpful info has been added to it.
* NEW: A lot of the icons have been reworked.
* NEW: New skins have been added.


=== Algodoo 1.9.5 beta, 2011-05-08 ===
* FIX: Bug with some graphic cards that did not load textures correctly has been fixed.
* FIX: Thrusters does not reset their direction when changing their attachment any more.
* FIX: The selection menu also contains thrusters
* IMP: End points of springs now work better, along with selection of these.
* IMP: New textures for the default skin.
* FIX: Fixed a bug that could cause the tracking of geometries to be unchecked.
* FIX: Fixed a bug that caused a spring to be deleted when attached to two fixated geoms.
* FIX: Several fixes to the side menues, and how they behave.


=== Algodoo 1.8.5, 2010-12-10 ===
* IMP: Window fading out time now depends on GUI.Skin.fadeTime.
* FIX: Algodoo does not crash when shake-disbanding the chain tool.
* NEW: Russian translation added.

=== Algodoo 1.8.4, 2010-12-01 ===
* NEW: Buttons for removing a bound button or geom controller.
* NEW: "Expand UI" button for expanding all expandables.
* IMP: More precision in slider values.
* FIX: Bug concerning "lucky aiming" of sliders, i.e. hitting a nice round value.
* FIX: Rare bug that would cause a slider to show another value than it was set to.

=== Algodoo 1.8.3, 2010-11-26 ===
* IMP: With force visualization on, forces are now caluclated even when simulation is paused.
* IMP: Added maximum force arrow size.
* FIX: force/velocity settings now show up in options whenever an object has visualization on.
* FIX: Enabled auto-position of texture on planes.
* FIX: Attraction is now applied based on the center of geometries instead of composite bodies. The behaviour is kept for older scenes.
* FIX: Solved problem with button selectors (i.e. mirror, motor, ...).
* IMP: Major changes to expandables: better looking, with mouse-over cursor change and with a small button to toggle between default size and full size. Also, the expand-bar never moves to left/top anymore.
* NEW: Buttons for finding scene folder and saved plot files in OS.
* FIX: May have fixed the huge "Algodoo sometimes takes very long time to switch language/skin/scale" bug.
* FIX: Tool options button will no longer fade out underlying windows.
* NEW: Brush tool multidraw erase now erases selected first (if any).

=== Algodoo 1.8.2, 2010-11-04 ===
* Replaced old system of simple/medium/advanced mode with "expandables".
* Improved menus.
* Improved tutorials.
* Better access to tool options.
* Replaced some text in the menu bar with icons.
* Nicer looking plot window.
* Changed to always show update messages if the user clicked check for update manually.
* When being informed of a new version, a button "Don't remind me again" will be shown.
* Added suggestion to upgrade graphics drivers if frame rate is too low.
* Partially covered windows now fade out.
* Middle-clicking or double-clicking the panner/zoomer drag-buttons now resets the pan/zoom.
* Varius improvments for use on touch screens, including press-and-hold tooltips.
* Somewhat improved undo/redo.
* Changed behavior:
** Click an object on the move to freeze its velocity.
** Brush tool now also erases water.
** Click-holding a button will now ALWAYS click in on release, and NEVER before.
* Improved air friction calculation to use the true diameter of an object rather than a quick estimate (switch using Sim.airFrictionVersion).
* Fixed a CSG bug.
* Fixed scale center for lasers and tracers.
* Fixed bug with drawing a chain whith snap-to-grid.
* Fixed a bug where a laser would sometimes loose too much intensity when entering water.
* Fixed air switch not switching of air friction/buoyancy for water.
* Fixed size of fallback fonts with GUI.scale!=1 (Big Buttons).
* Fixed cloning moving objects (clone preview is now kept still).
* Fixed copy-pasting of planes.
* Added new skins.


=== Algodoo 1.8.0, 2010-09-16 ===
* Tab-completion and search (/) in console now shows information about suggestions (value, default, description).
* Better choice of default resolution when starting Algodoo.
* Fixed missing "Eraser" checkbox from brush tool menu.
* Fixed problem with laser pen tool and snapping.
* Better looking thin polygons while drawing with brush tool.
* Changed scaling factors (App.scalePow*) so as to ensure same behavior when scaling uniformly, given no external forces.
* Changed force and velocity arrow scales to be of more natural units (m/N and m/(m/s)=s respectively)
* Improved plane sketch recognition.
* Fixed minor issue when setting negative speed for a group of glued geometries.
* Made the text in the information window (under the context menu) selectable for easy copying of values.
* Fixed issue with cutting an object remotely glued to another.
* Fixed undo for color sliders.
* Fixed problem where tracer head would not draw, or draw with wrong color.
* Fixed gear-tool not creating a group.
* Fixed bug where entering a slider value with the keyboard would sometimes not do anything, and/or not be undoable.
* Console now keeps command history between runs.
* Fixed some fonts sometimes missing cursor for empty text boxes.
* Fixed "Random Color(s)" always picking a color from palette, even for color sliders which didn't affect entities.
* Enabled throwing with clone tool.
* Fixed issue with logfile sometimes not being written if Algodoo crashed (which is exactly when you want it to be written).
* Fixed issue with showing plot for spring.
* The hinge sketch now works like the hinge tool, in that it splits glued bodies.
* Fixed units for some plot derivates.
* Added preview of spring length when using spring tool.
* Fixed some Mac-specific bugs, including over-eagerness to recognize the plane sketch.
* Fixed scaling of attraction and controller acceleration for geometries.
* Improved sketch morphing of straight-edged polygons.
* Added Chinese, Slovak and Spanish translations.
* Fixed issue with undo/redo-lists coming up when clicking on something above them.

=== Algodoo 1.7.8, 2010-09-03 ===
* Made the first tutorial image clickable.
* Fixed some polygon-related collision bugs, were two deeply penetrating objects would not separate.
* Fixed collision problem with boxes that deeply penetrate polygons.
* Fixed an issue where the hinge tool would split remotely glued bodies.
* Added ability to close context menu, sub-menus and (some) windows with escape.
* Added unlock fallback: if Algodoo fails to register the unlock information for the entire machine (i.e. if the user does not run Algodoo as administrator), then Algodoo will still register for the local user.
* Windows: Fixed a bug that would cause Algodoo to incorrectly claim a successful unlock.
* Fixed a few unlock-related issues.
* Added ability to erase selected water by drawing a line over it with appropriate tool.

=== Algodoo 1.7.7, 2010-09-01 ===
* Fixed "Shrinking joints on mirror" problem from 1.7.5
* One can once again place lasers by clicking background.
* "Hide windows" will now also hide the context menu.
* Removed ability to move slider with arrow keys.
* Much more sensible App.GUI.panFactor.
* Fixed issue with text cursor position when erasing text.
* Fixed issue with velocity-freeze.
* Fixed issue with setting 180° in velocity sliders.
* Fixed default plot-source for springs.
* Fixed problem with glued geometries splitting when deleting or moving one of them.
* Fixed problem with undo deleting scripts referencing Scene.my.*;
* Fixed problem with dragging the clone button to create a clone (one can now create a clone directly on top of prototype by press-holding the clone button).
* Fixed problem with multiple tool options open at once.
* Added tooltips about tool options.
* Added tool option titles.
* Re-added sketch tool options.
* Improved positioning of tool options.
* Added hexadecimal input of Unicode characters via ALT+ (e.g. press and hold ALT, and type +221E). Decimal input is still possible w/o the '+' (e.g. ALT 8776)
* dy/dx in plot output now uses approximately equal sign (it's only a numeric approximation).
* Changed translations so that "camera" has been replaced with "view" to avoid confusion with the "webcam" meaning of the word.
* Added tooltips for window buttons.
* Slightly improved laser and tracer textures.
* Fixed shift/ctrl/alt not working as controller buttons (for hinge motors etc).
* Fixed Scene.controllAccelerationFollowCamera not working with joysticks/gamepads.
* Fixed Scene.controllAccelerationFollowCamera not working with swapped/inverted x/y directions.
* Input using ALT now works (like ALT+2 for @ on some systems).
* Disabled the sketch tool selection circle when not using touch screens (change with Tools.SketchTool.enableSelectCircleMouse).
* Fuzzy lasers: lasers now draw a bit fuzzy. Controllable via App.laserFuzziness. Old scenes retain fuzziness=0.
* Lasers look better without shaders than before (even without fuzz). Get old rendering with "App.useLaserFuzzNoShaders=false";
* Improved vertex drawing of polygons with shaders (no more shrinkage after brush tool has finished drawing)
* Fixed bug where the "Opaque borders" palette attribute went ignored.
* Added translations for (included) materials, skins and palettes.
* Fixed issue with lingering tooltips.

=== Algodoo 1.7.6, 2010-08-20 ===
* Added System.zDepth cvar.
* Added a few fallback video-modes if the default one (or the one given in config) fails.
* Fixed "Deselect everything".
* Fixed problem with positions of snapped windows when hiding/unhiding them.
* Fixed texture tool undo.
* Fixed backwards compatibility of scripted motor-strength.
* Increased friction for thrown windows when a side is snapped or outside of window.
* Reverted tracer trial rendering to old style (switch with App.tracerOverdraw).
* Added checkbox for gluing new geometry to existing geometry when using brush tool.
* The brush tool now also glues to plane if set to glue at all.
* Fixed rare problem with widget movement on Algodoo window resize.
* Fixed issue with Thyme on Mac.
* Fixed issue with Unicode paths on Mac.
* Fixed the motor torque in the entity information window.
* Fixed window caption still saying "Algodoo Demo" when unlocking.
* One can now click on a Plot to get info about that point.
* Double-clicking a window title-bar now toggles it.
* Fixed huge problem with hinge options.
* Improved sliders:
** Enter equations as values, e.g. "10^3" or "15*3"
** Use x to refer to current value(s), e.g. enter "x*2" to double every value the slider controls.
** Enter a range by separating with " - ", e.g. "10 - 20" specifies a range but "10-20" a value (=-10).
* Some Thyme optimization.
* Improved change of hinge and spring attributes when scaling.
* Fixed big collision bug (thanks, Kilinich!)
* Moved "App.controllerAccelerationFollowsCamera" to "Scene.controllerAccelerationFollowsCamera" and made true by default.
* New behavior: Objects drawn or erased with brush tool will not move until the user is done.
* Fixed an issue with clicking when FPS is low.

=== Algodoo 1.7.5, 2010-08-13 ===
* Fixed rare bug with spawning joints from Thyme
* Fixed camera-follow being suspended only by drag tool and not by any other tool, instead of the the other way around.
* Fixed problem where the camera-tracked group would not be saved.
* Fixed double-clicking issue where second click would be at same position as first.
* Fixed issues with right/middle-click pan while using a tool.
* Fixed problems with positioning of sub-menus of especially the water context menu.
* Fixed problem with some text, especially italic text, being clipped prematurely.
* Fixed problem with plane sketch shake disband.
* Re-allowed very thin polygons.
* Fixed problem with triple-click zooming on objects.
* Throwing things with the move tool and rotate tool now takes simulation speed into account.
* Removed superfluous "Opaque borders" options from appearance menu for non-geometries.
* One can no longer rename non-scene-specific windows.
* Fixed disband of select with move tool by pressing escape.
* Fixed ugly morphing when drawing clockwise box using sketch tool.
* Fixed very irritating fullscreen bug (thanks, Kilinich!)
* Fixed file menu link to algobox not working (thanks, tatt).
* Changed file writing functions to only write BOM:s if needed, meaning better forwards-compatibility (i.e.: a scene saved with 1.7.5 will work in 1.7.1 iff the scene has only ASCII text/author/comments etc in it).
* Font menu: added ability to only show fonts that work with the current test text (i.e. "The quick brown fox..." etc).
* Fixed a bug where Algodoo crashes if a joint or laser is scaled outside the object it is fixed to.
* Fixed a bug where pausing/playing Algodoo could cause key-guided motors to be stuck in a particular fashion.
* Improved plot mouse-over caption to show derivate and tangent for closest plot line.
* A maximum number of points for plots to be drawn with can now be set via the console, by App.maxPlotPoints. 
* App.controllAccelerationFollowCamera can now be set to true, making geometry controllers follow the camera instead of the scene orientation.
* Made all GUI border textures twice as large so that they now look better with Big Buttons.
* Fixed an issue with the unlock menu.
* Added -reset argument option in Algodoo to quickly reset config and autosave. Under Windows a shortcut is created to this in the start menu.
* Algodoo now restarts self after clicking the reset button in the options menu.
* Algodoo now makes backup copies of the files it deletes when reseting.
* Fixed move and rotate tools freezing object velocities even when simulation was paused.
* Fixed bug where clones would always get zero velocity.
* Fixed directional controllers from still being active when entering text.
* Fixed bug where a hinge motor button released when paused would not be registered.
* Fixed problem with double-clicking destroy/mirror button fields.
* Fixed unexpected sub-menu open when dragging slider over menu button.
* Added a checkbox in Options->Simulation for toggling the existence of killer planes on/off.
* Fixed issue where one could move and pan with drag tool (which is confusing behavior).
* Changed pan button drag behavior (now sets panning speed and direction).
* Fixed a bug where the size of tracers were not saved.
* Forced font shadows for HUD-text (like rotate angle) even when skin has it disabled (for readability reasons).
* Removed warnings from console when browsing for scenes outside Documents/Algodoo/
* You can now always select non-geometries with hinge/fixate/tracer/laser tools (and as before, any other tool as well).
* Improved drag-responsiveness. When doing a drag, Algodoo should now respond immediately.
* Improved the code for throwing objects and windows, making false positives less likely.
* Fixed minor bug with rotate tool.
* Improved rotate visuals.
* Fixed some issues with tablets (including ignored "Pressure sensitive" option).
* Context menu can now be toggled with "Menu button" (on the left of right_ctrl on most keyboards).
* Fixed memory leak.
* Fixed motor torque to acctually control motor torque.
* Scaling/rotating/mirroring now also transforms velocities, motor strength, hinge impulse break limit and spring constant (controllable via "App.transformAttribs"). Mirror by button is an exception (keeps velocities).
* Added "Freeze" button to velocity menu.
* Changed select-behavior: CTRL toggles selection, CTRL+SHIFT adds to selection and SHIFT deselects (as before). The old behavior is available via "App.GUI.ctrlSelection = false")
* Fixed horrible bug where, after installing Algodoo for the first time, the program won't run at all.
* New icons for a few things.
* Holding down SHIFT and CTRL while starting Algodoo now resets Algodoo.

=== Algodoo 1.7.4, 2010-06-18 ===
* Fixed problem where registration info with namnes containing non-ascii characters (such as ü, ä, etc) wasn't working.
* Fixed problem where SHIFT-click would not deselect objects.
* Fixed problem where click on unselected object would not always select it.
* Fixed selecting using sketch/poly tools ignoring SHIFT/CTRL modifiers.
* Fixed a few potential crashes.
* Fixed problem where Algodoo sometimes would reject perfectly good polygons (even ones old versions would accept).
* Fixed problem with serializing spring strength of springs with legacyMode<2.
* Added Thyme command "geval" which acts like "eval", but always evaluates in the root scope/closure.
* Fixed a problem where undo would sometimes reset values in the script menu.
* Texture tool no longer scales textures when scrolling over unselected objects (just selected ones).
* Changed unlock-command from ctrl-u to ctrl-shift-u to remove conflict with ungroup.
* Fixed a problem with mouse input in fullscreen.
* Fixed tooltip from coming up when mouse is on the move over a component (such as a slider).
* Fixed rare problem with bad polygon distance maps.
* Fixed wrong penetration distance for large overlaps for scaled polygons.
* Fixed close button on context menu not closing the context menu (it will now - and it will disable "fixed context menu" if it is enabled)

=== Algodoo 1.7.3, 2010-06-14 ===
* Fixed plane tool degree character being rendered incorrectly.
* Added UTF-8 BOM to all text files written by Algodoo (.csv, .phn, .cfg, Logfile.txt, ...), fixing mojibake issues.
* The press and hold context menu open is now available only if App.GUI.pressAndHoldMenus is set to true (false by default).
* Clicking a selected object now does nothing. This means you can double-click one of several selected objects to get the context menu.
* Fixed tool-bar-flip-crash.
* Fixed nicer tool-bar flip (based on tatt's suggestion).
* Fixed sketch tool ring showing too often.
* Re-added close button to context menu.
* Fixed problem reading UTF-16 encoded text files.
* Changed translation system for Type_:s to allow for more complex plural systems.
* Re-added App.mousePos Thyme function.
* Fixed the "cairo_image_surface_create_for_data failed for size=[1, 256], channels=1" crash.
* Fixed some checkboxes not being grayed out when they should have been.
* Fixed the "The procedure entry point CreateSymbolicLinkW could not be located in the dynamic link library KERNEL32.dll" startup crash
* Lowered default box text font resolution from 48 to 32 to save memory.
* Fixed issue of sometimes not being able to load old .phz:s containing textures.
* Fixed issues with opening files with unicode names.
* Fixed bug causing crash when shake-disbanding sketch tool with recognized box, circle or polygon.
* Moved font quality options (AA, metrics and hinting) from Skin to Resources.
* Added the ability to turn on subpixel font anti-aliasing (see Resources.fontAASubPixel).
* Entity and simulation information windows now only gets updated every App.GUI.infoUpdateInterval seconds to save on cpu.

=== Algodoo 1.7.2 (beta), 2010-06-08 ===
* Added full unicode support, both in UI (translations) and for file paths etc.
* Changed font engine to Pango, giving:
** Improved text readability.
** Support for text markup (bold, italic, color etc) in language files as well as in box texts (see http://library.gnome.org/devel/pango/stable/PangoMarkupFormat.html).
** Support for switching the typeface of the skin (Options -> Skin -> Typeface) and box-text to any system font via a nice menu.
* Added console search via / (example: type in "/gravity" and press enter).
* You can now select text (for copying) in the console.
* You can now 'throw' things with the rotate tool.
* Rescaling a box now leaves the text scale be unless the scale is axis-uniform (Scale-tool + SHIFT).
* Added three attributes to skins that controlls the size of things: sliderHeight, smallIconSize, largeIconSize.
* Added clarification for when users enters an invalid serial key.
* Fixed the joint de-serialization bug introduced in 1.7.1.
* Fixed a bug that would cause bad water rendering on screens wider than 2048 pixels.
* Fixed collision respons issues with objects sliding along curved polygons.
* Improved algorithm for transforming polygons into boxes.
* Changed the simulation information window to use the same font as everywhere else (used to be a monospace font).

=== Algodoo 1.7.1, 2010-03-26 ===
* The checkbox for unlocking windows can now be found by right-clicking or double-clicking locked windows.
* The triple-click-drag zoom gesture now zooms centered on the origin of the gesture.
* Improved click tolerance for touch screens.
* Improved detection of failure to save unlock info on Mac and Linux.
* Improved behavior of throwing windows and objects (with the mouse and move tool respectively).
* Fixed a bug preventing Algodoo from being correctly unlocked/registered on Mac and Linux.
* Fixed an issue where having GUI.scale!=1 (e.g. Big buttons set to true) would sometimes move about the tool-bars on small screens.
* Fixed a bug that would sometimes cause a crash when using a custom chain.
* Fixed a bug that would sometimes cause things to be rendered too darkly.
* Fixed a bug that caused invalid widgets when changing language, UI level or skin.
* Fixed a problem with the context menu moving when supposedly fixed.
* Fixed a problem with language miss-matches of window titles.
* Fixed a problem with the position of sub-menus of sub-menus (namely the sub select menu).
* Fixed a problem with the position of the plot source selection window.
* Fixed a bug with press-and-holding using the sketch tool.

=== Algodoo 1.7.0, 2010-03-22 ===
* Fixed Swedish translation.
* Made parsing of translation files more forgiving.
* Fixed an issue with the command history of the console.
* Fixed a issue where FontFormater.Gen would not overwrite existing files.
* Fixed so that all boxes now have the classic arial_black font.
* You can now double/triple click to pan/zoom on any object (not only background).
* Fixed icons for mirror buttons in camera menu (thanks Kilinich).
* Fixed an issue whith scenes moving when loaded from _ONEXITSAVE (thanks again, Kilinich).
* Hinge sketch snaps to center of circles.
* Fixed a bug with slider ranges (thanks tatt).
* Fixed a problem with some fonts/encodings not being able to display "²" (these now show "^2" instead).
* Hid the "colorHSVA" attribute from the script menu since it isn't serialized (use "color = math.HSV2RGB([h,s,v])++[a]" instead).
* Fixed more forgiving parsing of serial key.
* Fixed sketch tool fixate preview.

=== Algodoo 1.6.6, 2010-03-17 ===
* Removed shader linking spam
* Smoother auto-apply of palette
* Fixed a problem with Key.bind (F12 should now work again for screenshots)
* Reverted the "delete geometries both glued and fixated" fix from before since it caused more bugs that it solved
* Added cvar App.killerPlanes to easily add and remove the default killer planes
* Fixed a problem with drawing self-intersecting polygons (like pentagrams).
* Added slider for chain size (no longer zoom dependent)
* Fonts now have equal width for characters +-0123456789
* Slight redesign of entity information
* Button input chooser (for stuff like laser activation) now uses left/right shift/alt/ctrl/meta buttons explicitly instead of the commons (e.g. "left shift" instead of just "shift")
* Clicking and holding to open context menu now only occurs if no modifiers (CTRL, SHIFT, ...) are down.
* Being slow in using drag, move and rotate tools should now never open the context menu
* Script menu now comes in just one long list, but you can throw the window to "scroll" down.
* Fixed an issue with widgets disappearing when closing Algodoo with hidden windows.
* Scale tool now resizes single objects immediately even when ALT is not pressed.
* Added "Select by encircling" options to Sketch, cut, box and polygon tool options (all linked to App.GUI.allowDrawSelect)
* Added serialization of tool options (so that brush size etc are now saved between sessions).
* Added Swedish translation.

=== Algodoo 1.6.5, 2010-03-09 ===	
* Script menu:
** You now have to press shift-enter to make a new-line in the script menu.
** When making coding mistakes in the script menu the code is no longer erased.
** Entering something in the command box will now rebuild the script menu (showing any new attributes).
* Increased GUI.clickTimeTolerance from 0.3 to 0.4 seconds.
* Fixed a problem with .phi files not creating the necessary directories (thanks tatt).
* Fixed problem with minimizing in Windows.
* Reverted to old behavior when dragging an object tracked/followed by camera.
* Improved the behavior of using a tool (other than drag tool) on objects tracked/followed by camera (e.g. moving it). You can change this behavior with "Scene.Camera.suspendFollowIfTooling".
* Fixed a minor issue with skin and palette list reloading every second.
* Fixed a problem where undoing with the context menu open would yield a bad context menu.
* Erase buttons are now hidden when not unlocked.
* Added error message if failing to save a palette.
* Fixed a problem with the spring menu not opening for spring between two world bodies.
* Fixed spring strength being naught when coming loose after being connected to two world bodies.
* Fixed clouds from moving around when reloading GUI.
* Fixed an issue where joints would always change color when modifying a palette with auto-apply palette set to true.
* Fixed an issue where GUI-windows wouldn't hide when move, rotate or drag-tool was triggered by the sketch tool.

=== Algodoo 1.6.4, 2010-03-05 ===
* Slider labels now lose focus when you press enter (thanks Roast Beef)
* The results of shader compilation is no longer spammed into the log file and console (thanks tatt)
* Improved script menu allowing multi-line functions
* Fixed a crash caused by typing stuff in the script command box
* Fixed a bug with cutting selected objects where unselected joints would also be cut
* Fixed some bugs related to removing geometries that where both glued and fixated
* Fixes some issues with widgets moving on top of each other when resizing window or changing GUI.scale (Big buttons)
* Algodoo now works correctly with Windows Aero Snap
* Global variables with names conflicting with entity attributes (e.g. "color", "pos" etc) no longer interferes with deserialization
* Fixed a problem where a lasers would not be able to point in perfect multiples of 45°.
* Fixed spelling mistake for Plot_Energy_Potential_Gravity_Output (thanks tatt)
* Fixed a problem with press-and-holding the mirror button for a bunch of objects.
* Fixed a problem with the context menu not closing when deleting a selected object.
* Slightly better border coloring
* Tracers can now grow arbitrarily long
* Fixed unlock menu not closing after successful unlock
* Fixed "Meta_ForcedFont" not working (thanks yet again, tatt!)
* Added logic that tries to figure out if an old scene had border on or off by default.
* Added missing jpeg.dll (Windows)
* Fixed a bug that would change the values of sliders just by inspection
* Fixed an issue with drawing a selection for translucent white water with shaders
* Added ability to erase scenes in the "Load scene" menu
* Added Japanese translation by tatt

=== Algodoo 1.6.3, 2010-03-01 ===
New features:
* The sketch tool is back - with a vengeance! Use it to create polygons, circles, boxes, planes, hinges, fixates, springs, chains, tracers and more!
* A much improved help menu with a few wizard-like tutorials.
* Skins - Change the textures, colors and font of the menus in Algodoo. Read about how to make your own in "/skins/About skins.txt" under the installation directory.
* Palettes - Change the default color scheme of new or existing objects.
* Algodoo Installer files (*.phi) - A simple .zip archive that when opened in Algodoo gets extracted to the users home directory. Using .phi files you can easily share fonts, translations, palettes, scenes, skins and textures.
* Better sliders: When changing the attributes of several objects: drag the right mouse button on the slider to define a range of values. Move that range with the middle mouse button.

Changed behavior:
* Brush size is now zoom-independent
* In the appearance menu all geometries have an option to show all forces acting on them, thus showing forces for a single object. There is also a similar options for velocities.
* Visualize Forces now visualizes contact forces in both direction (Newtons third)
* Selection rectangles around springs and laser pointers are now anti aliased
* Several instances of Algodoo can now run at once, but opening an Algodoo file (*.phz, *.phn, *.phi) will still open it in the previous instance (if any)
* Shaders are on by default

UI changes:
* Algodoo now uses an entirely new default skin, created by Algodoo's new artist Jonathan.
* All GUI windows are now movable and snaps to other windows and to the screen edges. They can also be thrown. Toolbar switches between horizontal and vertical based on what it snaps to.
* The context menu can now be set to only appear when you right-click, double-click or click-hold objects (classic behavior)
* When you save a file, the standard author is changed to the name which the file is saved in
* The cursor always shows up when options are open (and the options can now be opened with ctrl+p).
* You must now right-click or double-click a tool-icon to bring up its settings (Brush, Gear and Chain-tool only)
* "New scene" now clears force/velocity visualization settings
* Some fixes for plots
* Added "Big buttons" button to increase GUI.scale
* To select objects you no longer need to encircle them entirely (just some 4/5 of them). Change with App.GUI.selectFactor

Other:
* Added the ability to generate font files for a specific 8-bit character set. See console command FontGenerator.Gen for details.
* Better support for multiple screens in Windows
* Translucent and transparent objects now have brighter borders (for objects with opaque borders)

Bug fixes:
* Fixed a problem when pasting into a text field. Should now allow for several lines being pasted
* Fixed a problem with Thyme code disappearing
* Fixed an issue with force vectors being drawn the wrong way
* Tools now disband if the objects they operate on disappear
* When cutting a internal gear the hinge is now kept intact
* Fixed a bug with incorrect inertia calculations for polygons
* Fixed a bug that would cause object borders to be incorrectly serialized
* The hue color slider will no longer reset when saturation or brightness reach singularities.
* Fixed a problem with Keys.bind which sometimes caused button pressed to be ignored if the simulation was paused


=== Algodoo 1.6.0, 2009-08-31 ===
New features:
* Lasers  -  they can refract, reflect and even cut
* Plots/graphs  -  explore everything from energy conservation to harmonic oscillators
* Web camera support  -  get real world objects into Algodoo easily
* Generation of geometry from semi-transparent textures
* Visualization of forces and velocities
* Grid, with optional snapping and custom number of axes (make squares as well as hexagons)
* Velocity menu  -  set precise velocities for selected objects
* Incompressible fluids  -  a far better fluid simulation using a completely novel method (switch to old behavior in the options menu)
* A texture tool to move, rotate and scale textures
* A startup check for updates (can be disabled in options)
* The ability to turn a circle into a protractor
* Support for the accelerometer of the Intel Powered Convertible Classmate PC

Changed behavior:
* Everything in Algodoo is now saved to the user home directory (e.g. My Documents/Algodoo on Windows). Nothing is ever written to the installation folder.
* Constrained Algodoo to one instance at the time. Opening a scene file will open it in the previous instance
* Changed spring behavior slightly to make it conserve energy better. The old behavior is available by setting legacyMode=0 in the script menu. This is done automatically for springs imported from old Phun scenes.
* Spring strength is now entered as standard spring constant (unit N/m)
* When scaling a geometry, any attachments are now kept on the same world coordinate
* The hinge tool can now separate glued geometries. This means that when used together with the brush tool, creating rag dolls etc is very fast.
* cut tool now deletes FixJoints
* Hinge motor is now unchecked if the user selects a key controller for it instead
* Made camera zoom resolution independent.
* Changed drag tool behavior: When failing to drag a static geometry, nothing will now happen
* Added limitation of only calling "onCollide" for one contact per geometry pair per time step
* Disabled water vaporization (re-enable with "SPH.vaporizeTime = 5")
* When moving a stretched hinge, the hinge will now connect at its center instead of at its old stretched coordinates
* Changed the pan button pan direction to correspond to "normal" mouse panning
* Undo:
** Changed undo behavior: when undoing with no previous redo, an extra snapshot will be added to the redo-list, so one can go back to the future.
** Several subsequent drags, moves and slider modifications are now combined into one undo
** Added smart enforcing of "App.maxUndo": low priority actions (like drag) are removed first from the undo list.
** When undoing, the position of the clouds are now also undone

UI changes:
* Better load scene menu:
** Added a full path text field
** Added a file filter
** Added the ability to sort file list by date
** Changed color of directories
* Added the ability to reset the Algodoo configuration (useful for when playing to much with scripting)
* Box text settings are now hidden if there is no box text
* Made simple mode even simpler (less buttons)
* Clicking twice on the "show widget objects" button (the eye) returns you to the old view
* Better alignment of digits in entity information widget.
* Fixed slightly nicer printing of floats
* Text editing: double click now selects a word while triple click selects an entire line in textboxes
* Added welcome text when running Algodoo the first time
* Sliders: if marked objects have different values, the sliders will now show the range of different values instead of "NaN".
* Added the ability to freeze water
* Improved entity information
* Changed some icons
* Added the ability to shift the selected collision group of selected objects
* GUI windows now fade out temporarily when using a tool in their vicinity
* Added translations of the simulation info
* Turned off the custom cursors per default (due to performance issues).
* Moved help and about buttons to the file menu
* Added scale tool labels showing the current scale factors
* Increased clickable area of button selector (hinge and laser control)

Visual changes:
* Added a fade in effect when loading a scene (eye candy)
* Made the default sky color brighter to better distinguish it from the water color
* Added better color cues to make it easier to spot what a hinge or spring is attach to
* Added cute clouds - similar to the 16-bit clouds. Turn off in background menu in advanced mode.
* Better looking borders
* The geometry border width is now limited by a fraction of the geometry area (controlled by App.maxBorderArea)
* Better looking polygons
* Selected objects now always have a white border round them, even if textured.

Improvements:
* Improved spring tool to connect to top two geometries (so you can now connect objects that fully covers each other)
* Added preview to polygon tool, and changed polygon tool to close polygons more often
* Improved spring tool to connect to top two geometries (so you can now connect objects that fully covers each other)
* Bound together color sliders: changing one updates others bound to the same object
* Added the ability to disband a tool by shaking the mouse violently. Set the sensitivity by App.GUI.toolGestureSensitivity. Turn off with App.GUI.toolGestures
* Solved some instances of deeply penetrating objects getting stuck inside each other
* Lowered Sim.targetPenetration to make most constraints more stiff
* Improved the Polygon-Circle collision detection code to get better normals and fewer contact points
* Slightly improved distance maps for small polygons and for long, thin polygons
* The English tool-tip will now be used when a tool-tip translation is missing
* Slightly improved gearification
* Added support for right-to-left languages (e.g. Arabic). See English translation file for details

Windows specific:
* Removed the ugly console window
* Algodoo will now restore to maximized window if it was running as such the last time
* Changed full screen mode to fake full screen mode to fix issues with touch-screens and other alternative input devices
* The installer will now prompt you to close Algodoo if it's running

Advanced:
* Added variable information (where available) when entering name of a variable in the console
* Added the ability to create conveyor belts through the script variable "materialVelocity" (experimental feautre)
* Added command System.regularScreenshots for taking a screenshot every N:th simulation step
* Added new Thyme meta function "eval": Example code:  eval("bar:=1; foo:={bar=bar+1;}; foo*eval(\"foo\")");
* Added Thyme type conversion functions: math.toBool, math.toInt, math.toFloat and math.toString.
* Added console command App.forceVertexPolygonDrawing - set to true to get a more accurate, but slower, rendering of polygons. Will also save video memory.
* Removed the writing of Unlogged.txt

Bug fixes:
* Fixed a lot of problems regarding gluing and fixates
** Fixed a problem where objects that had never been explicitly glued would still still stick together if previously attached to it via fixates
** Fixed a bug that would cause problems when trying to loosen a group of geometries containing a plane
** Fixed an issue with incorrectly reconnected FixJoints after scaling, moving or cloning
** Fixed a bug concerning the transformation of FixJoints
** Fixed a problem where geometries glued together would sometimes come appart when moved/rotated/mirrored
** Fixed a problem where moving a geometry would strangely move fixates attached to it
** Fixed a problem where glued objects would not come loose if a geometry connecting them was removed
* Fixed a problem where Ctrl-C could stop working on windows
* Fixed a problem where a scene could fail to save but would not give an error message
* Fixed borders from growing while modifying a polygon with brush tool
* Fixed problems with the chain tool that caused it to attach to the wrong geometries
* Fixed unit of hinge impulse (Nm to Ns)
* Improved CSG, brush and cut tool
* Fixed a bug that would make water particles disappear on undo
* Fixed a problem where importing a Phunlet would affect old objects
* Fixed several bugs regarding the serialization of groups
* Made the background colors of the color sliders more accurate
* Fixed a bug that would sometimes allow transformed (moved/rotated) joints to attach to something new in the transformed group
* Fixed a bug that prevented very small polygons from being loaded or created
* Fixed a bug that would prevent files from being saved in subdirectories (i.e. saving to "foo/bar" will now save the file to "My Documents/Algodoo/scenes/foo/bar.phz")
* Fixed a bug that caused App.maxSPHSpawn to be ignored
* Fixed a bug that would sometimes incorrectly separate geometries upon undo
* Fixed hinges from jerking when modifying a polygon
* Fixed a graphics glitch concerning the borders of scaled polygons
* Fixed an issue with the undo/redo buttons
* Fixed a bug that regarding cloning of things with "onCollide":s
* Fixed a bug that would sometimes cause "onCollide" to be called for geometries that had been removed from the simulation during the same time step
* Collision detection:
** Solved several problems that caused instabilities in box-box contacts
** Fixed a small bug with the circle-circle collision detection (singularity issue with perfectly aligned centers)
* Cables:
** Fixed a problem with cables that caused attached objects to act jumpy
** Fixed a bug concerning cables that could cause hinged objects to rotate when they shouldn't
* Fixed a bug that caused drift in object positions and rotation when moving, rotating undoing or loading
* Fixed a rare problem with attraction between geometries of the same body
* Fixed a small energy glitch (source)
* Fixed a bug that could cause a crash when objects had a non-positive mass
* Fixed a bug that would cause objects of the same body to collide

Optimizations:
* Serious optimization of core physics engine (almost twice as fast in some cases!)
* Added polygon contact reduction (will speed up any scene with many flat-sided polygons)
* Optimized broad-phase collision detection by a factor 2 (most noticeable when cloning or moving many objects, e.g. water)
* Optimized broad-phase for any scene containing lots of polygons
* Optimized scene loading
* Optimized Thyme parsing
* Optimized memory usage: undo snapshots now take up about 50% less RAM
* Optimized rendering with shaders by about 8x.
* Optimized moving and rotating objects slightly
* Many small optimizations


=== Beta 1.5.65, 2009-08-27 ===
* Fixed a bug that would cause a crash if onHitByLaser has a Scene.Open event.
* Changed onCollide arguments: the normal will always point towards the other object (e.other)
* Fixed a bug that would crash algodoo if Ctrl-Q was pressed during startup


=== Beta 1.5.64, 2009-08-26 ===
* Fixed unicode home directory paths in Windows for real this time (thanks a lot for the help, Tatt!)
* Disabled Thyme command Scene.SaveAs due to security conserns
* Reenabled saving scenes anywhere (not only in home dir)
* Fixed a minor problem with rotation tool and hinged circles
* Fixed problem with bringing window to front (windows only)
* Fixed huge memory leak that would sometimes occur on heavy Thyme scripting.
* Fixed joints from attaching to new stuff if the geometry it was attached to got scaled so that the joint was no longer on top of it.
* Removed ability to place plane and laser points by clicking (doesn't quite fit in with the rest of the tools)
* Fixed problem with flickering objects.
* Fixed a problem (introduced in 5.58) where hinge tool could sometimes create double hinges in the simulation


=== Beta 1.5.63, 2009-08-25 ===
* New icon for texture tool
* Made texture tool an advanced move only feature
* Added the ability to load scenes with Unicode file names from the load scene menu.
* If trying to save file to a directory that does not exist, that directory will be created.
* Added "Loading, please wait" splash for when switching on/off cute clouds, 16-bit textures or shaders.


=== Beta 1.5.62, 2009-08-24 ===
* Added ability to add planes by clicking
* Fixed some forward compatibility issues regarding glued objects
* Fixed a bug regarding gestures and camera movements
* Removed the writing of Unlogged.txt
* Fixed support for unicode paths and user names on Windows


=== Beta 1.5.61, 2009-08-21 ===
* Fixed box text in right-to-left languages
* Fixed a bug where deleting something glued to the world would loosen everything glued to the world (bug introduced in 5.57)
* Added the ability to disband a tool by shaking the mouse violently. Set the sensitivity by App.GUI.toolGestureSensitivity. Turn off with App.GUI.toolGestures
* Fixed a bug where making diagonals with grid axes=2 would no longer work (introduced in 1.5.60)
* Fixed a bug where lasers could be placed by dragging with the right mouse button
* Solidify renamed as "Freeze water". The resulting polygon(s) will get ice-like attributes (friction etc) and will also get glued to all geometries the water touches.
* New icon for Algodoo scenes (.phz/.phn)


=== Beta 1.5.60, 2009-08-19 ===
* Fixed a few bugs related to "communication.cfg"
* Slight narrow phase optimization
* Fixed a bug where the collision sets of lasers would go ignored
* Added better color cues to make it easier to spot what a hinge or spring is attach to
* Fixed saving plot as image from changing the scene aspect ratio.
* Fixed gear hinge becoming larger than gear
* The installer will now prompt you to close Algodoo if it's running
* You can now choose the angle of the laser when using the laser tool by dragging the mouse
* Slightly improved distance maps for long, thin polygons
* Changed the pan button pan direction to correspond to "normal" mouse panning.
* Added slider for grid base
* Force visualization settings are now disabled if force visualization is.
* Fixed unit of hinge impulse (Nm to Ns)
* Spring strength is now entered as standard spring constant (unit N/m)
* Added the ability to have more than 2 grid axes (great for making regular polygons)
* Improved spring tool to connect to top two geometries (so you can now connect objects that fully covers each other)
* EntInfoAngularMomentum is now around center of mass of selected objects
* Box test settings are now hidden if there is no box text


=== Beta 5.58, 2009-08-13 ===
* Turned off blocked contact solving due to instabilities
* Fixed a bug that would allow a plot window to shrink beoynd its bounds.
* Reintroduced arrow cursors when scaling or resizing the plot window
* Increased clickable area of buttonselector (hinge and laser control)
* Changed behavior of borders slightly
* Snap to grid can now be disabled by holding down ALT
* Fixed a bug where the scale tool box around a polygon would be too big
* Major optimization of laser-world test (excluding water). Feel the difference by toggling App.laserBroadPhase
* Slightly improved normals for laser-polyon
* Added a startup check for updates (can be disabled in options)
* The hinge tool can now separate glued geometries. This means that when used together with the brush tool, creating ragdolls etc is very fast.
* Small optimizations here and there


=== Beta 5.57, 2009-08-03 ===
* Constrained Algodoo to one instance at the time. Opening a scene file will open it in the previous instance
* Lasers can now cut the results of old cuts if the laser beam is interrupted
* Fixed a glitch in the overwrite scene dialog
* Fixed an issue with the undo/redo buttons
* Fixed an issue with undo/redo going to a paused state without pausing
* Fixed a bug that would cause selection, camera tracking and bind to gravity not to be serialized for one-object groups
* The english tooltip will now be used when a tooltip translation is missing
* Changed drag tool behavior: When failing to drag a static geometry, nothing will now happen
* Fixed a problem where Ctrl-C could stop working on windows
* The geometry border width is now limited by a fraction of the geometry area (controlled by App.maxBorderArea)
* Fixed a bug that would cause sort-by-date not to work in the load file menu
* Improved contact solver (added a direct solver for normal forces for when two bodies have exactly two contacts). Turn off with "Sim.blockedContactSolver = false"
* Hid force arrows for deleted objects
* Fixed a problem where glued objects would not come loose if a geometry connecting them was removed


=== Beta 5.56, 2009-07-02 ===
* Optimized rendering with shaders by about 8x.
* Fixed a bug that would in rare cases cause a major slow down of collision detection
* Added support for right-to-left languages (e.g. arabic). See english translation file for details
* Several subsequent drags, moves and slider modifications are now combined into one undo.
* When scaling a geometry, any attachments are now kept on the same world coordinate
* Lasers can now be made to cut through any mortal geometry
* Added cute clouds - similar to the 16-bit clouds. Turn off in background menu in advanced mode.
* File load menu now shrinks again after leaving folder with many files
* Added texture tool to move, rotate and scale textures
* Hid force arrow labels and values in simple mode
* Removed the ability to move objects with the arrow keys (more confusing than usefull)
* Improved the precision of very small polygons.


=== Beta 5.55, 2009-06-17 ===
* Fixed a big memory leak introduced in 5.54
* Fixed major circle-polygon collision detection bug also introduced in 5.54
* Transform into box/circle and gearify will no longer detach glued objects.


=== Beta 5.54, 2009-06-16 ===
* Serious optimization of core physics engine (almost twice as fast in some cases!)
* Added polygon contact reduction (will speed up any scene with flat-sided polygons)
* Re-enabled script menu by default (still only in advanced mode though)
* Solved some instances of deepely penetrating objects getting stuck inside each other
* Fixed some issues with the scene/file name


=== Beta 5.53, 2009-06-11 ===
* Fixed a problem with writing Algodoo registry information on Vista.
* Fixed a bug where geometries would sometimes be incorrectly marked as glued
* Fixed a problem where fixated objects would sometimes come loose
* Optimized scene loading by a lot
* Optimized broad-phase for any scene containing lots of polygons.
* Made camera zoom resolution independent.


=== Beta 5.52, 2009-06-09 ===
* Fixed problems with the chain tool that caused it to attach to the wrong geometries
* Optimized Thyme parsing
* Fixed a bug with laser vs water
* Fixed several bugs with CSG, brush and cut tool
* May have fixed a problem with reading Algodoo registry information on Vista.
* Added a fade in effect when loading a scene (yay for eye candy)


=== Beta 5.51, 2009-06-03 ===
* Fixed the drawn angle of the rotation tool (bug introduced in 5.50)
* Added a "remove gravity group" button after the gravitation offset slider in options->simulation
* The options menu now remember which tab is open
* Fixed yet another small source of box-box contact instability
* Improved circle-polygon collisions
* Fixed a problem where polygons would sometimes spawn in the wrong location
* Added scale tool labels showing the current scale factors
* Improved CSG, brush and cut tool


=== Beta 5.50, 2009-05-29 ===
* Fixed a graphics glitch concerning the borders of scaled polygons (for real this time!)
* Fixed hinges from jerking when modifying a polygon
* Added console command App.forceVertexPolygonDrawing - set to true to get a more accurate, but slower, rendering of polygons. Will also save video memory.
* Fixed a bug concerning cables that could cause hinged objects to rotate when they shouldn't
* Fixed a problem with cables that caused attached objects to act jumpy
* Solved several problems that caused instabilities in box-box contacts
* Slightly improved gearification
* Fixed a bug concering calling liquify from event handlers (onCollide) on cloned, scaled, or otherwise modified geometries.
* Added explicit close buttons to the help and about menus
* Lowered Sim.targetPenetration to make most constraints more stiff
* Fixed a bug that would sometimes allow transformed (moved/rotated) joints to attach to something new in the transformed group
* When moving a stretched hinge, the hinge will now connect at its center instead of at its old stretched coordinates

Algodoo only:
* Added trailing zeros to force arrow strength
* Added force arrows for cable impulses (named the same as hinge forces)
* When trying to register Algodoo as non-admin, Algodoo will now prompt the user to login as admin.
* Made the water less viscous by lowering SPH.solveT


=== Beta 5.49, 2009-05-25 ===
* Moved help and about buttons to the file menu
* Fixed a problem where textures would be reloaded twice when toggling back from fullscreen after going to it from a maximized state (windows only)
* Algodoo will now use the default wm cursor if the fps drops below 20
* Turned off the custom cursors per default. Turn on again with "GUI.forceOSCursor=false"
* Fixed a graphics glitch concerning the borders of scaled polygons
* Added preview to polygon tool, and changed polygon tool to close polygons more often

Algodoo only:
* Fixed a bug with viscous incompressible fluid


=== Beta 5.48, 2009-05-19 ===
* Fixed strange positioning of some windows

Windows only:
* Changed fullscreen mode to fake fullscreen mode to fix issues with touch-screens and other alternative input devices

Algodoo only:
* Fixed a bug that would cause a laser to be able to enter a non-transparent material with undiminished intensity
* Changed a few phunland.com references to algodoo.com
* Made grid and force visualization scene specific
* The friction between incompressible water and geometries are now multiplied by the friction coefficent of the geometry
* Incompressible water now can have a vsicocity, set with "SPH.viscosity"

Classmate convertible specific:
* Fixed a bug problem that would make the accelerometer non-functional after exiting Algodoo


=== Beta 5.47, 2009-05-18 ===
* Fixed a problem involving smooth camera pan and the brush tool (again!)
* Hinge motor is not unchecked if the use selectes a key controller for it instead
* Fixed a problem where a scene could fail to save but would not give an error message

Algodoo only:
* Fixed a bug where mirrored polygons would not refract lasers
* Fixed a problem with missing laser bemas
* Changed laser to fade out ultra-violet light to make it slightly more realistic
* Moved "Send into orbit" to the velocity menu


=== Beta 5.46, 2009-05-15 ===
* Fixed strange background to start-up "Loading!" message
* Fixed a bug that would cause the scene to look stretched after saving
* Fixed a bug that prevented scenes to be opened with Algodoo from shell

Algodoo only:
* Fixed a bug that would cause lasers to crash


=== Beta 5.45, 2009-05-14 ===
* Added the ability to translate the simulation info
* Added the ability to reset the Algodoo configuration.

Algodoo only:
* Fixed yet another problem with self-intersecting polygons created with snap to grid
* Fixed problems with a laser hitting very thin objects
* Snap to grid now does diagonal snapping for cut and polygon tools
* Added the ability to "draw back" drawn lines when using the cut and polygon tools with snap to grid on
* Laser events (onHitByLaser, onLaserHit) are now only called when the simulation is running


=== Beta 5.44, 2009-05-13 ===
* Removed console window
* Fixed a bug that would make water particles disappear on undo.
* Removed surperfluous "phunlets/" from phunlet saving menu.
* cut tool now deletes fixjoints

Algodoo only:
* Fixed a problem that prevented Algodoo from restoring to a registered state when running as non-admin user on windows
* Changed laser behavior: the laser is now in only one material at the time; originally the top material and then later the latest entered material. It only enters water if there is no other material.


=== Beta 5.43, 2009-05-12 ===
* Added SPH.vaporizeTime to scene file
* Fixed a problem where springs from before beta 5.31 would have the wrong legacyMode, and so behave badly.
* Fixed a problem with deleting fixates with glued objects involved
* Fixed a bug where adding a phunlet would affect old objects

Algodoo only:
* Fixed certain plot features not fading out when window does
* Fixed a laser precision problem where a laser would miss a geometry edge when two geometry edges was perfectly aligned


=== Beta 5.42, 2009-05-08 ===
* Fixed a problem that would incorrectly close then selection menu when hovering over the select menu
* Fixed a problem where geometries glued together would sometimes come appart when moved/rotated/mirrored
* Fixed a problem where moving a geometry would strangly move fixates attached to it
* Fixed a bug that would sometimes incorrectly separate geometries upon undo
* Fixed a bug that caused App.maxSPHSpawn to be ignored
* Fixed a bug that would cause objects of the same body to collide
* Renamed phunlets/official to phunlets/prefabs
* Disabled water vaporization (re-enable with "SPH.vaporizeTime = 5")
* GUI windows now fade out temporarily when using a tool in their vicinity
* Added Thyme type conversion functions: math.toBool, math.toInt, math.toFloat and math.toString.
* Added new Thyme meta function "eval": Example code:  eval("bar:=1; foo:={bar=bar+1;}; foo*eval(\"foo\")");

Algodoo only:
* Fixed better snap to grid for planes


=== Beta 5.41, 2009-05-07 ===
* Fixed a problem that caused objects to slowly rotate when undoing, loading a scene, moving etc.
* Fixed a huge problem introduced in 5.40 where geometries could get the wrong position and scale
* Fixed symmetry issues - with the aid of snap-to-grid, one can now produce a stack of circles on plane that never crumbles.


=== Beta 5.40, 2009-05-06 ===
* Fixed a bug that could cause an objects attributes to be changed by observing them via a slider
* Fixed a bug that could cause a crash when objects had a non-positive mass
* Fixed cloning of the "glued" attribute
* Fixed a bug with the move tool


=== Beta 5.39, 2009-05-06 ===
* Fixed several problems regarding fixates and gluing
* File filter now gets focus by default
* Fixed a bug that would prevent files from being saved in subdirectories (i.e. saving to "foo/bar" will now save the file to "My Documents/Algodoo/scenes/foo/bar.phz")
* Optimized broadphase collision detection by a factor 2 (most noticeable when cloning or moving many objects, e.g. water)


=== Beta 5.38, 2009-05-04 ===
* Added the ability to shift the selected collision group of selected objects
* Added command System.regularScreenshots for taking a screenshot every N:th simulation step
* Fixed a bug that prevented very small polygons from being loaded or created
* Fixed ugly phunlet menu
* Fixed file filter "phz" not matching any .phz files
* Fixed a problem where objects that had never been explicitly glued would still still stick together if previously attached to it via fixtes
* Fixed a bug that would cause problems when trying to loosen a group of geometries containing a plane


=== Beta 5.37, 2009-04-29 ===
* Fixed a small bug with the circle-circle collision detection (singularity issue whith perfectly aligned centers)
* Rewrote the Polygon-Circle collision detection code to get better normals and fewer contact points
* Fixed a small energy glitch (source)
* Changed the "attach tracer" icon
* Hid the script menu unless App.enableScriptMenu is set to true.
* Added moment of inertia to entity information menu
* Aligned the numbers of the entity information
* Added a full path text field to the load scene/phunlet menus
* Added a filter to the load scene/phunlet menus
* Added the ability to sort file list by date
* Changed color of directories in the file list.
* Various optimizations

Algodoo only:
* Fixed a bug that would sometimes cause plot to crash
* Fixed a bug that would cause a crash when improper code was entered in the console
* Made the x=0 and y=0 grid lines distinct from the others
* After 30 days of using the Algodoo demo (without unlocking), Algodoo will now still start, but only the Unlock menu will be available.
* Fixed several problems with zero-width polygons caused by snap-to-grid-perfect CSG and/or polygon drawing
* Snap to grid now also snaps the edges of the axis aligned bounding box of the moved objects.
* Hid irrelevant plot sources (e.g. potential spring energy for a box)


=== Beta 5.36, 2009-04-27 ===
* Added slider ranges to color sliders
* Made the background colors of the color sliders more accurate
* Bound together color sliders: changing one updates others bound to the same object(s)
* Made the default sky color brighter to better distinguish it from the water color
* Added limitation of only calling onCollide for one contact per geometry pair per time step
* Fixed a bug that would sometimes cause onCollide/onLaserHit/onHitByLaser to be called for geometries that had been removed from the simulation during the same time step
* Algodoo will now restore to maximized window if it was running as such the last time (Windows only)
* Changed undo behavior: when undoing with no previous redo, an extra snapshot will be added to the redo-list, so one can go back to the future.
* Changed undo behavior: redoing Sim start won't start the simulation
* Added smart enforcing of App.maxUndo: low priority actions (like drag) are removed first from the undo list.

Algodoo only:
* Added watermark to locked Algodoo Demo
* Fixed incompressible fluid not being deleted by killer objects
* Added the ability to "solidify" water


=== Beta 5.35, 2009-04-23 ===
* Sliders: if marked objects have different values, the sliders will now show the range of different values instead of "NaN".
* Selected objects now always have a white border round them, even if textured.
* Menus opened with mouse-over will now close if the mouse is outside it for too long
* Fixed a bug that regardning cloning of things with onCollide:s
* Added welcome text when running Algodoo the first time
* Made simple mode the default mode
* Made simple mode even simpler (less buttons)
* Added support for the Classmate PC

Algodoo only:
* Added activation key to laser
* Made App.laserEvents true by default
* When liquifying something while plotting it, the plot will continue plotting the same attributes for the water (when possible)
* Added the ability to turn a circle into a protractor
* Improved the smoothness of the laser color gradient when in a gravity field
* Added the ability to switch between new and old fluid behavior in the options menu.
* Added scene serialization of fluid type
* Turned off velocity smoothing for incompressibel fluids (making them less viscious)


=== Beta 5.34, 2009-04-21 ===
* Prevented phunlets larger than 100 objects to be saved in demo mode
* Fixed a bug concerning the transformation of fixjoints
* Double click now selects a word while triple click selects an entire line in textboxes
* Hid "information" and "plot" menu option when unnecessary
* When undoing, the position of the clouds are now also undone

Algodoo only:
* Added App.laserSuperBoost, App.numColorsInRainbow and App.laserResolution to scene files
* Fixed a problem with very light objects in contact with water that would sometimes cause the simulation to blow up.


=== Beta 5.33, 2009-04-17 ===
* Fixed the problem with added file path when saving
* Fixed some window positioning issues
* Changed touch screen behaviour: enable to get correct touch screen mouse coordinates in full screen (but mouse coordinates will be wrong).
* Removed duplicate "phunlets" directories from load scene dialog
* Moved official scenes to separate subfolders of scenes/ and scenes/phunlets
* Fixed a bug that caused drift in object positions when moving or rotating a group of objects
* Optimized moving and rotating objects slightly

Algodoo only:
* Unified Algodoo and Algodoo Demo: unlock Algodoo Beta with username, e-mail and serial key to get Algodoo.
* Added constraints on Algodoo Demo (annoying splash screen, max 30 day usage, and max 100 objects)
* Made attraction-bent lasers zoom-independant.
* Added cvar App.laserResolution to control the resolution of the bent laser beam
* Added cvar App.laserEvents that has to be set to true to activate onLaserHit and onHitByLaser


=== Beta 5.32, 2009-04-15 ===
* Optimized memory usage: undo snapshots now take up about 50% less RAM

Algodoo only:
* Force visualization now turns off Sim.solveRandomizeConstraints to give less jitter in the force arrow strengths. This will, however, make towers less stable.
* Removed the energy chart (the plot is better anyway)
* May have fixed yet another entity information related crash


=== Beta 5.31, 2009-04-09 ===
* Changed spring behavior slightly to make it conserve energy better. The old behavior is available by setting legacyMode=0 in the script menu. This is done automatically for springs imported from pre 5.31 scenes.
* Bumped file version up to 5
* Added default value information (where available) when entering name of a variable in the console
* Fixed slightly nicer printing of floats
* Fixed a bug regarding the serialization of groups
* Fixed an issue with incorrectly reconnected fixjoints after scaling, moving or cloning

Algodoo only:
* Fixed a bug that would cause Algodoo to incorrectly think the time limit had expired
* Added the ability to create conveyor belts through the script variable "materialVelocity" (experimental feautre)
* Fixed a bug that would sometimes cause a crash when showing entity info or plotting a graph


=== Beta 5.30, 2009-04-07 ===
* Everything in Algodoo is now saved to My Documents/Algodoo . Nothing is ever written to the installation folder.
* Better number alignment in entity information widget.
* Groups containing water is now properly serialized in scene files and undo snapshots

Algodoo only:
* Added mouse-over information for plot
* Plots now keeps old data when undoing, so that you now can compare several runs side by side in the same plot


=== Beta 5.29, 2009-04-06 ===
* Clicking twice on the "show widget objects" button returns you to the old view
* Better looking opaque borders around transparent objects
* Fixed borders from growing while modifying a polygon with brush tool
* Fixed a rare problem with attraction between geometries of the same body

Algodoo only:
* Added a menu for setting object velocities
* Added the ability to plot the angle of the velocity vector of an object
* Added command SPH.SetNewSPH to activate new experimental fluids. Get the old SPH fluid with the command SPH.SetClassicSPH.


=== Beta 5.28, 2009-03-31 ===
* Added immortality - geometries that are immune against killers.
* Made the default killer planes immortal so that falling killers won't remove the killer planes.
* Fixed a bug introduced in 5.27 that stacked widget descriptions (e.g. "Appearance for 2 circles for 2 circles")
* Fixed a bug that caused widgets to not be serialized at all.
* Fixed yet another bug where objects would incorrectly be grouped together
* Fixed a problem where ungrouping (Ctrl-U) would close widgets
* Removed extra "..." from translations
* Added Polish translation by Pitros


=== Beta 5.27, 2009-03-30 ===
* Changed the look of the fixjoint to reflect what it is connected to
* Changed autosave time from every 30 seconds to every 5 minutes.
* Added a checkbox in options to turn autosave off
* Changed cloning behavior to clone attributes with any scripts intact
* Fixed a bad bug concerning "Transform into box" and other geometry actions.
* Fixed a problem where Phun would fail to find textures in .phz
* Fixed a bug that would incorrectly group together objects
* Fixed some problems regarding moving or cloning joints (springs, hinges, fixates)
* Added serialization of "Draw Hinges/Fixes when running" options to scene file
* May have fixed a problem with serialization of spring lengths
* Optimized rendering slightly
* Changed layer filter to completely hide objects from view
* Added serialization of layer filter to scene
* Tracers now gets erased when moved to the background
* Turned off alpha channel in screenshots. Turn on again with "App.screenshotsWithAlpha=true"
* Changed "Attach tracers" feature to scale tracers with geometry size instead of camera zoom
* Fixed better contrast colors when having a white or very bright background color.
* Readded the descriptive text of widgets (e.g. "Geometry actions for 2 polygons")
* Added "show group" button to widgets
* Added Dutch translation by Mike-RaWare


=== Beta 5.26, 2009-03-24 ===
* Fixed a bug that prevented textures from being loaded correctly from .phz files
* Fixed a problem where an aborted chain would not be undoable
* Fixed a problem where scaling an object would close any widgets related to it (like the color menu)
* Fixed a bug where deleting an object while scaling it would crash Phun
* Fixed a bug where pressing delete/backspace while cloning would always delete the original
* Fixed a bug that caused submenus and popups to be closed when dragging a slider with an object behind it.
* Fixed a bug that would cause some sliders to erroneously go to zero instead of infinity
* Fixed a bug that would cause Phun to crash when editing the box text of several boxes at the same time
* Fixed a problem with holding down SHIFT before moving or rotating an object
* Fixed a bug where redo could create invisible objects
* Made it simpler to move, rotate and scale objects tracked by camera
* Added Math.and (&&) and Math.or (||) to Thyme
* Renamed "Color menu" to the more accurate "Appearance"
* Added the ability to script length, damping and strength of a spring
* Added german translation by KaLul


=== Beta 5.25, 2009-03-19 ===
Rendering:
* Added support for textured geometries
* Added new optional rendering mode for water: software meta surface.

Scene files:
* New file format: .phz which is a zip containing the scene, a thumbnail and any used textures.
* Velocities for objects and water particles is now saved to the scene files.
* Water and groups can now be saved in phunlets

Tools:
* New brush tool
* New gear tool
* New cut tool
* Polygon tool: self-intersecting polygons are now handled (e.g. figure-of-eight:s)
* Added the ability to choose the chain building blocks (right-click a group of objects with exactly two hinges attached to the world)
* When reconnecting a chain to the first geometry in the chain, the chaintool will now create a perfect closed chain with no hinges to the background
* New behavior: to move or drag something, first select it and then drag it with most any tool.
* Hinge/fixjoint/spring now attaches to selected geometries first (used to always attach the top two entities)
* Added the ability to throw things with the move-tool
* Added 'snap to axis' functionality when holding down SHIFT for Move and Clone tool.

UI:
* Added three levels to the user interface: Simple, Medium and Advanced
* Made the camera move smoothly
* Added the ability to rotate the camera with an object (reset rotation with "Zoom to scene" or "Default view")
* Made Phun more touch-screen friendly (especially when "pen input" is selected)
* Added the ability to add text onto boxes
* Pens no longer draw anything when moved in paused mode.
* Added the ability to select water and move it around, clone it etc.
* Added extra cursor icon to indicate which tool is selected
* Added support for non-Latin1 8-bit character sets (you'll need to create a new font file and set Font in the translation file).
* Added a loading screen
* Added a splashscreen
* Changed how a hinge is drawn if it is a motor
* Added support for pen tablets (including pressure sensitivity when using new brush tool)
* Mouse-over object highlighting is now only active if the simulation is paused.
* Fixed so that Phun binds ctrl over left_ctrl and right_ctrl (same for alt, shift and meta) in hinge/geom controllers and Keys.bind.
* Changed mirror/kill/motor key behavior to only work when the simulation is running
* When rotating objects or creating planes you will now get automatic 15° snapping when the cursor is close to the origin.
* Added the ability to drag-and-drop images and scenes into Phun from explorer (Windows only)

Menus:
* Went back to the old GUI with rounder and larger components
* The context menu is now always open instead of poping up on right-click
* Sliders now round to closest integer or other "simple" number
* Added a few predefined materials (and you can create your own if you like - see the "materials" folder)
* Dragging the clone button now creates a clone of the selected objects
* Added "select alike" button, that selects identical objects (good for finding clones)
* Added sliders for gravity strength and direction in options
* Added a button to the menu bar to hide all other gui components.
* Added the ability to automatically attach tracers to selected geometries
* Added option "gearify" to add gears to an object (cog sizes decided in the gear tool options)
* Added "transform into box" action alongside the old "transform into circle".
* Added a layer filter menu - now specific collision layers can be filtered out from rendering and interaction
* Changed the color picking sliders from HSL to HSV. Change back by setting "App.GUI.useHSL = true;" in either console or config.cfg
* Added Sim.time to the simulation info box
* Reorganized the user interface a lot
* Added cvar GUI.tooltips so the user can disable tooltips.

Physics:
* Added support for holy polygons (polygons with holes)
* Added Constructive Solid Geometry (CSG) - select one of two intersecting objects and in the CSG menu select Cut, Intersect, Subtract or Add.
* Added the ability to create "killer" geometries, that removes anything they touch from the simulation.
* Replaced Scene.fallLimit with four "killer planes" that removes anything they touch from the simulation. These can be deleted if desired.
* Added the ability to link the rotation of an object to the direction of gravity
* Increased the number of collision groups to seven.

Physics engine:
* Added attraction: a distance dependent forces between geometries in the same collision group
* Added the concept of cables - transparent code that makes chains far more robust than before even under large stress. See the old behavior with "Sim.cables = false;"
* Greatly improved the stability of towers/stacking
* Fixed an energy- and momentum leak caused by interaction between forces (springs, gravity, ...) and constraints (hinges, contacts).

Scripting:
* Added a scripting menu in advanced mode where object attributes can be set.
* Added onCollide function to geometries - this is a function that is called when two objects collide. It has an event argument e with members e.pos, e.normal, e.other and e.this.
* Added closure "Scene.my" that can contain user defined scene specific variables that will be serialized with the scene.
* Added two Thyme-meta-functions: Reflection.ExecuteCode and Reflection.ExecuteFile
* Added command Scene.Open which opens a scene given a filename.
* Added command Scene.SaveAs which saves the current scene to a given file. WARNING: Will overwrite any existing file without asking!
* Thyme is now Turing complete through an if-else-clause of the form: (foo ? bar : baz)
* Improved the Thyme parser to be able to handle chained infix operators (e.g. "4/2*2") without extra parentheses.
* Thyme is now case insensitive
* Added Thyme support for hexadecimal and binary numbers (0xf0a1, 0b101011)
* Added Thyme support for the operators == and != for lists.

Fixes:
* Fixed text input of characters with Alt Gr, i.e. []{}" etc depending on keyboard layout
* Changed screenshot format from tga to png.
* Fixed a problem with drawing mouse-cursors when in fullscreen mode.
* Fixed a problem where thin polygons would get really fouled up distance maps
* Fixed copy-and-paste of text and phunlets
* Removed the cmd window in Windows
* A lot more fixes and tweaks that I've forgotten

Optimization:
* Speeded up mirror and uniform-axes scaling of polygons while also saving memory
* General speedups, especially for large scenes
* Added (very) limited support for multicore; type in "Threading.numThreads = N" (no quotations) in your console or config.cfg, where N is your number of cores. May speed up really huge scenes slightly, but may also slow it down.

Translations:
* Japanese translation by tatt61880
* Brazilian Portuguese translation by xxGLHRMxx
* Russian translation by Kilinich
* English and Swedish by emilk


=== Beta 4.22, 2008-08-12 ===
* Fixed a bug where Phun would crash when cloning after first deleting items (thanks for helping me replicate, tatt61880)
* Added the console command App.GUI.dragUndo. If set to false, drags can't be undone.
* When uploading a bug report and logfile is checked, the logfile from the previous Algodoo session will also be sent, so that we can debug a crash.


=== Beta 4.21, 2008-08-12 ===
* Changed so that the clone tool only selects both the original and the clone iff ctrl is pressed upon release (good idea, tatt61880)
* Fixed a bug where the clone tool would sometimes leave one object out of the clone preview
* Fixed a bug where the scaletool would try to scale an empty group and crash (pointed out by tatt61880)
* Fixed a bug where "toggle" in the hinge controls would be reset on undo (pointed out by vovams).
* Fixed it so that a hinge toggle button that was on gets restored to being on when undoing or loading a scene.
* Added improved logic for determening the mirror axis when binding a key to the mirror command.
* Fixed a bug where the polygon positions after scale/mirror would be very inaccurate for objects far from origo (bug noticed by lucidliquid)
* Added the command "Scene.MoveToOrigo" which moves the entire scene to the center of the world coordinate system. Improves floating point precision.
* Fixed a problem with panning and zooming while using the clone tool (problem pointed out by guyboy)


=== Beta 4.20, 2008-08-08 ===
* Added the ability to assign a key to destroy entities (extrapolated from an idea by Ze Roob)
* Added the ability to assign a key to mirror a group of entities
* Added the ability to turn off collisions between geometries with identical collision settings
* Changed scale tool behavior to scale single circles towards their center
* When cloning objects by holding down CTRL, the simulation is no longer automatically paused, and the cpu work is done when the copy has been dropped. Also, both the original and the clone is selected once the clone is done, which helps when cloning up massive amounts of anything. The clone button in the popup menu is unaffected.
* You can now clone with CTRL when using the drag-tool
* Reduced cpu usage on large scenes
* Fixed a bug where binding certain buttons (.,;=[]{}\) to control a hinge would create a useless .phn file (thanks for pointing it out, Cyanide Cloud et al)
* Fixed a rare problem with moving pens and attaching them to new geometries
* Fixed a bug where cloning, scaling or moving several objects would sometimes attach joints to the wrong entities
* Fixed a bug where glued geometries (geoms sharing the same body without a fixjoint) would detach when scaled (thanks, tatt61880)
* Fixed a bug where objects once connected with hinges would never collide again, even when the hinges were removed (thanks for pointing it out, are11)
* Fixed a bug where a cloned entity would loose some of its attributes (density, restitution etc) when undoing or saving the scene (pointed out by RicH).
* Fixed a bug where Phun would crash if pressing escape while rotating, moving or dragging an object (it now aborts the operation).
* Fixed a problem where very small polygons would sometimes crash Phun (and also decreased the likelihood of them looking very weird).
* Fixed a problem where two or more water particles would get 'tied' together
* Fixed it so that dragging something is (again) an undoable action
* Fixed a bug where the Scene title would be lost when Undoing (pointed out by tatt61880).
* Fixed a bug where objects fixated together would get incorrect velocities when the fixate was removed (bug found by Rabidmonkey)


=== Beta 4.13, 2008-07-15 ===
* Fixed a problem in 4.12 where the brake-button on hinges in old beta 4 scenes wouldn't work (since I used to misspell them "break"...)
* Fixed a problem with cloning pens		
* Added a menu option to change the target length of a spring (I know this has been requested for quite some time now...)
* Added the ability to click with your middle mouse button to reset the geom directional controller selectors as well as the hinge controller selectors.
* May have solved the horrible "pressing undo clears the scene and won't let me redo" bug. (time will tell)
* Added a auto-brake option to the hinge controller. When this is on, the hinge will brake whenever the forward, back or brake buttons aren't pressed (so the brake-key becomes the neutral-key). Suggested by ostfisk and others
* Added error messages with line numbers on tokenizer errors - should help translators.
* Added translation: Francais
* Fixed a problem with loading old .phn files: when joints were attached to planes they would often get messed up positions
* Fixed so that the camera pans to any tracked objects when loading old .phn files.
* Slightly enhanced scale tool visual aid
* Slightly enhanced rotation- and scale center choice algorithm
* Added undo/redo for common scene settings (water color, gravity etc) - should fix the "I need to re-enter the scene info each time I save" bug
* Fixed a bug where removing a hinge between two objects would automatically turn on collision for those objects, even if there were still another hinge connecting them.
* Added the ability to bind a combination of several keys with the console command Keys.bind


=== Beta 4.12, 2008-07-09 ===
* Optimized input handling, especially on Linux
* Fixed a problem where water wouldn't show behind a transparent object
* Fixed a bug where circles, boxes and planes couldn't be transparent when there was water in the scene and anti-aliasing and simple water was both off.
* Fixed some issues with the water rendering when anti-aliasing and simple water was both off.
* Added texture prefetching so that phun doesn't freeze up the first time you draw a circle or open a menu
* Added unit to the density slider (kg/m²)
* Fixed a bug where the directional controller on a geometry would apply a force proportional to the frame rate (and much less force than it should)
* Added four translations: Czech, Deutsch, Español and Portugues brasileiro
* Fixed some problems with undoing water
* Fixed some strange behavior regarding fixjoints and glue
* Added the ability to double-click to open context menus, and to select all the text in a textbox
* Fixed a problem with zero-fade time of pens (thanks, VeeT?)
* Added the ability to pan by holding down both mouse buttons (left and right). This means you can pan anytime, anywhere: in the middle of drawing a polygon you can pan away and then continue drawing, and you can start panning without access to the background.
* Optimized scenes with pens slightly


=== Beta 4.11, 2008-07-02 ===
* Fixed a bug where undo:ing would reset the sky color, gravity etc
* Fixed a bug where scenes would be saved to the phunlet directory
* Fixed a bug where importing a phunlet would change the scene name
* Restored the "clear scene" file menu button


=== Beta 4.1, 2008-07-02 ===
* Included a default config.cfg (so backup your old one if you want it saved)
* Turned shaders/anti-aliasing off by default
* Added some tooltips (explaining that shaders and anti-aliasing is the same thing, and that you can load/import both scenes and phunlets)
* Fixed the cloning of springs
* Fixed some problems with scene loading:
**  Controlled hinges have their motors off by default if loading pre beta-4 scenes
**  Bad geometry is forgiven and ignored, and scene loading continues
**  Things with the same body id no longer needs to be attached with a fixjoínt (although it is recommended)
**  Fixed a bug where fixed geometry would sometimes end up in wrong places (bug have been present for quite a while)
* Less lagg when moving the mouse on slow computers
* Changed back to the old behavior of loading scenes in paused mode
* Fixed box scale/mirror bug
* Fixed so that the circle 'cake' is affected by scale/mirror
* More fixate related bugs fixed (causing problems ranging from crashes to invisible planes)
* Fixed controller input (for hinge motors etc) missing key events
* Fixed a problem where deleting the entities used by a free window (like changing color) would make Phun crash.
* Fixed math.pi not working in Thyme
* Fixed a problem where you could lose the cursor in the console
* Pressing backspace now deletes selected entities (as does pressing delete)
* Using fixedsys font for the profilers again
* Increased the hinge impulse break limit slider maximum from 10 to 100
* Fixed a problem where the zoom slider wouldn't be updated when zooming using the scroll wheel.
* Added "Free drawing" checkbox to the options menu - clicking this will allow you to draw inside and around old objects
* Re-added simulation info to the file menu.
* Added cvar Sim.time (good idea, Zuriki)
* Replaced "Clear scene" with "New scene" in the file menu. Pressing this will also reset all the cvars saved in a scene file (water color etc). You can clear the scene without resetting the cvars by pressing "ctrl+a, delete" and then "erase water" in the file menu.
* Added information about the maximum hinge impulse for selected entities in the information window (usefull for determening a good hinge impulse break limit). (Thanks for the idea, Rabidmonkey)
* Removed the ability to set a distance break limit for hinges (you should only need to use the impulse break limit).
* Added a Glue option under the geometry menu (magicly glues objects to the background)
* Added an auto-glue checkbox to the option menu (automatically glues all new geometry to the background)
* Fixed the "are you sure you want to overwrite..." dialog to work for scenes as well as phunlets.


=== Beta 4.0, 2008-06-27 ===
* Removed superfluous full program path in the save dialog. 
* Removed dependency on OpenGL 2.0 for shaders (should fix the "NULL-function in Shader::Shader" reported by agsgymboy etc)
* Set shaders to be on by default where available (hope this won't foul things up anymore)
* New highlight system: a white border around selected objects (no more blinking)
* Objects can now be translucent
* Added a pen tool that attaches to a geometry and draws a line tracing its path.
* Vastly improved text input system with mouse selection and a lot more
* Hinge motors can now be bound to any keyboard key or joystick/gamepad button
* Geometries can have forces added to them controlled by either keyboard or joysticks/gamepads
* Hinges can be set to break if stretched or strained too much
* The plane tool now angles the plane in 15° increments if shift is pressed, so it is now simple to create horizontal planes.
* Rotating with shift pressed will now re-align single boxes or planes to 15° increments 
* Added scene meta info: title, author and description
* Added setting (gravity, air friction, camera etc) to scene files
* Upgraded the chain tool to work like the brush tool (ie freehand drawing of chains)
* New box primitive (boxes are no longer box-shaped polygons)
* New scale tool
* Added a mirror command to the popup menu
* Added the cvar Resources.force16BitTextures for those having texture problems (type "Resources.force16BitTextures = true" in console)
* Added tooltips for some menu items, such as the tools.
* Holding down the shortcut key for a tool will now only temporarily select it, while quickly pressing it will select it for real.
* Redone the menus quite a bit. They can now be collapsed, renamed (click their titles) and are automatically saved in the scene and config files.
* You can now have the canera follow a group of objects instead of just one
* You can now move the camera relative to the object (or group of objects) you are following.
* Extended the number of collision groups to five (used to be three).
* Added Phunlets (save a phunlet by right-clicking a group of objects, import a phunlet by right-clicking the background).
* Added the ability to copy- and paste phunlets/objects/thyme-code in Phun (ie: select something, press ctrl-c, and then ctrl-v it where you want a copy or want the code)
* Changed fixate behavior to always fixate the top two geometries, even if they're already connected (same for hinges and springs)
* Phun now starts the simulation whenever a new scene is loaded (though you can immediatly undo this)
* Added ability to change water and sky color in the right click menu.
* Removed some rather arbitrary limits on position, speed and angular velocity
* Fixates and hinges now have a small plus (+) added to them when attached to the background (thanks for the suggestion, Melchior)
* Fixed GUI mouse input opacity (you can no longer click through a GUI window)
* Fixed a few fixate-related bugs
* Fixed a bug where water particles would sometimes collide with a polygon bounding box.
* Various fixes and tweaks


=== Beta 3.5, 2008-03-27 ===
* Ctrl-G now groups objects together, and Ctrl-U ungroups them
* When clicking an object in a group, the entire group is now selected (unless ALT is pressed)
* Fixed a major circle-circle collision bug
* Fixed so that gui windows now get on top when dragged
* Fixed so that more scenes can be displayed under File->Load Scene as well as subdirs to Phun/Scenes
* Optimized the GUI rendering slightly
* Optimized entity rendering by 'frustum' culling
* Added separate option controlling an objects collision with water; making things watertight should now be easy (thanks for suggestion, Chad Autry)
* Added (three) collision groups; objects in one group will only collide with other objects in the same group
* Added an options for showing some simple statistics for selected objects (mass, area, velocity, ...)
* F8 now shows the collision points and their counter force and direction (used to be the collision normal)
* Added the ability to turn on and off the drawing of object borders from the options menu (even in the no-shader path)
* Added translations (accessible under the file menu). Phun now supports (in Latin1):
	Català (Catalan), Deutsch (German), English, Espanol (Spanish), Francais (French), Italiano (Italian), Magyar (Hungarian), Nederlands (Dutch), Polski (Polish), Portugues (Portuguese), Romanian, Suomi (Finnish) and Svenska (Swedish).


=== Beta 3.12, 2008-02-21 ===
* Beta 3.12 removed the dependency on multi texturing support.


=== Beta 3.11, 2008-02-21 ===
* Beta 3.11 fixed a bug Stric pointed out to me


=== Beta 3.1, 2008-02-21 ===
* Removed the dependency on vcredist by compiling with mingw instead (thanks to Zao for the help)
* The linux version now figures out it's path.
* Moving objects moves them to the front of the screen again.
* Moving a geometry does no longer move all objects fixated to it
* You can now set a geometry not to collide with anything else by a checkbox in popup->geom.
* Added two console commands: System.minFPS and System.maxFPS. The simulation will be slowed down to match an FPS of System.minFPS; and the program will sleep so it won't go past System.maxFPS.
* Added the ability to click on a slider value and enter a new one.
* Fixed a bug where the text cursor would be drawn in the wrong place.
* Fixed so air buoyancy and friction adds to the rotation of an object (the heaviest part of an object will tend to fall first etc)
* Set Resources.shaders to false per default. Turn on shaders in the options menu.
* Added an option to turn off the clouds.


=== Beta 3.0, 2008-02-20 ===
* Added the ability to choose object color
* Added the ability to follow objects (right-click them to do so, and right-click background to stop).
* Optimized any scene containing water (more speed improvements to come though).
* Added a file command for removing all water from a scene
* Holding down shift while rotating now rotates in increments of 15°
* Prevented popups from coming to close to the bottom right corner of the screen.
* Set vsync off by default for better performance. Turn on again with System.vSync = true;
* Removed a couple of usages of OpenGL before I had a GL context (may have caused some start-up crashes).
* Fixed a bug where deleting things while moving them would cause the program to crash.
* Added circle LOD; if a circle is less than 10 pixels wide, it will be drawn in a simpler and faster way.
* No longer create the last hinge of a chain connected to the same body (like the world).
* Fixed a bug where you couldn't undo a clone
* Several minor fixes and tweaks.
* Added a Phun program icon by Marty
* Renamed scene files from .cfg to .phn (your old files will be renamed automatically at startup, and there is full backwards-compability by just renaming).
* Fixed so you know can tell Windows explorer so associate .phn files to Phun (you could before too, but now it works)
* Added an option for simple water rendering (good for FPS and for those having trouble with the other water render paths)
* Holding down ALT while clicking a chain let's you select individual joints.


=== Beta 2.51, 2008-02-17 ===
* Renamed App.shaders to Resources.shaders (just to confuse you), and made it actually work this time.
* Water droplets lie flat on surfaces (looks better)


=== Beta 2.5, 2008-02-16 ===
* Added a non-shader render path (turn on by putting "App.shaders=false;" in autoexec.cfg).
* Added the ability to control hinge motors with the arrow keys.
* Upgraded the tools so that you can draw with the hinge-, drag- and fixate-tools.
* Upgraded the brush tool to drawing straight lines when SHIFT is pressed (thanks to the people who suggested this feature)
* Added an option for drawing objects inside other objects
* Added an option for hiding hinges and fixates when the simulation is running (thanks for the tip, Jooh4n).
* Added autosave of config file.
* Fixed a bug where moving hinged objects may break the hinge
* Fixed a bug where 'Zoom to scene' wouldn't work
* Added detachable submenus to the popup-menu.
* Did some small rendering optimizations
* Added air buoyancy (lighter-than-air flight possible for light-weight objects)
* Renamed CRASH.cfg and LAST.cfg to _AUTOSAVE.cfg and _ONEXITSAVE.cfg


=== Beta 2.3, 2008-02-13 - First public beta ===
* Fixed a bug where motor hinges would add velocity to the objects attached to it
* Fixed a bug where you could click right through a GUI window


=== Beta 2.2, 2008-02-12 ===
* Redesigned the UI, with new File and Options menus.
* Disallowed left-click-menus by default. Turn back on in the new options menu
* Slightly better box-box collision detection
* Fixed a bug where the length of springs would be forgotten when moved
* Lowered the default spring strength to make it act a bit more springy by default
* Lowered the default water droplet size
* Fixed a problem where button-clicks would go undetected at low frame-rates
* You can now change the scale of the UI with the console command GUI.Scale
* Optimized the GUI rendering slightly


=== Beta 2.0, 2008-02-07 ===
* Made it easier to rotate planes.
* Added groups. You can now assign objects to group (0-9 on the keyboard) using ctrl-#, and select them by pressing that number.
* Added friction to water, so water droplets no longer slide frictionless over a surface
* Water no longer bounces on objects
* The water is now more stable
* Optimized water-world collision.
* Changed the object look slightly (removed polygon borders)
* Optimized polygon drawing for older hardware (no more floating point textures)
* Fixed a problem where Fixate-crosses would disappear when they were being moved
* Fixed a bug where a hinge motor would have trouble rotating with a spring attached
* Fixed three seperate instances of the NULL SharedPtr crash, involving geometry-fixating (often occuring during Undo:ing), water and bad objects. Hopefully this will fix all crashes (dream on, Emil...)
* Fixed a major memory leak. Things should run a lot smoother and use less memory from now on.
* Added a window title


=== Beta 1.7, 2008-01-30 ===
* A swedish translation accessible by a clicking the Swedish flag on the left
* Prettier background (clear blue sky with clouds floating)
* Max and minimum zoom level
* Zoom slider
* Help window
* About window
* Redesigned UI
* Single water droplets now evaporates after a while
* New keyboard shortcuts
* A lot of bugfixes
* Bundled TODO.txt and BUGS.txt for all to see
* More things I have forgotten about


=== Beta 1.6, 2008-01-24 ===
* Added Linux binary
* Fixed a bug regaring drawing squares (hold down shift while usign the box tool)
* Removed the guitar background


=== Beta 1.5, 2008-01-23 ===
* Ability to clone objects (drag while holding control, or click selection and choose "clone")
* Objects now have color
* Added hinge motors
* More stable drag tool
* Varius speed optimizations
* Improved UI
* Animated background


=== Beta 1.2, 2007-12-18 ===
* Fixed a bug where adding a fixjoint at the wrong place would crash the program
* Added arrows for the undo/redo buttons making the measier to spot
* Added a (stable) linux binary


=== Beta 1.1, 2007-12-18 ===
* Fixed a bug in the physics solver
* Fixed a bug causing the program to crash when adding zero sized objects
* Rearanged the menu bar and added icons for the panner and zoomer
* Optimized the rendering slightly


=== Beta 1.0, 2007-12-17 ===
* A completely new physics solver!
* A new Chain tool for placing out a string of circles connected with hinges
* The ability to tweak object restitution and friction
* A lot of fixes and tweaks


=== Alpha 4.5, 2007-12-13 ===
* Added support for simpler shaders
* Added sliders for adjusting simulation speed, object density and spring settings
* Added stripes on circles so their rotation can be observed
* Fixed a lot of bugs with the tools
* Fixed crash at exit (at least on Windows)


=== Alpha 4.1, 2007-11-30 ===
* Fixed rendering to work on older hardware


=== Alpha 4, 2007-11-28 ===

Changed:
* Added three tools: Box, FixJoint and Drag
* Added undo/redo
* Added ability to save and load scenes to file
* Visual upgrades
* Friction (Sim.friction)
* Added cvars antiAlias, fullscreen, resizable, resolution and vSync under System. Modify these in the config, or in the console at runtime (follow with a call to System.recreateWindow to apply).


=== Alpha 3, 2007-11-08 ===

Added:
* Fix joints
* Rotational joints
* Water
* Popup-menus for bodies (only two options: erase and liquify)
* Unified rendering for polygons, circles and planes

Fixed:
* Collision detection bugs
* Lots more


=== Alpha 2, 2007-10-31 ===

Features:
* Polygons, circles, planes and springs
* A very simple physics engine (temporary)
* A GUI for choosing different tools (brush, plane, circle and spring)
* A console and the Thyme scripting language (my own)
* Bugs!

Known issues:
* Crashes at exit
* The simulation checkbox not showing the simulation status

------------

That's it! Have a nice day.
