jQuery(document).ready(function() {
	var video$ = $("object").first();
	var image$ = video$.closest("p").siblings("p").find("img").first();
	video$.hide();
	image$.fancybox({
        'titleShow'     : false,
        'transitionIn'  : 'elastic',
        'transitionOut' : 'elastic',
        'href' : video$.find("embed").attr("src"),
        'type'      : 'swf',
        'swf'       : {'wmode':'transparent','allowfullscreen':'true'}
    });
});