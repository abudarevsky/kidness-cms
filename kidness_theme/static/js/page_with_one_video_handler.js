jQuery(document).ready(function() {
	var videos$ = $("object");
	videos$.each(function(){
		var image$ = $(this).closest("p").prev().find("img").first();
		$(this).hide();
		image$.fancybox({
	        'titleShow'     : false,
	        'transitionIn'  : 'elastic',
	        'transitionOut' : 'elastic',
	        'href' : $(this).find("embed").attr("src"),
	        'type'      : 'swf',
	        'swf'       : {'wmode':'transparent','allowfullscreen':'true'}
	    });
	});
});