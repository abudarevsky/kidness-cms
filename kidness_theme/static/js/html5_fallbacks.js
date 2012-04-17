(function( $ ){

	  $.fn.placeholder = function( options ) {  
		  function valueIsPlaceholder(input) {
				return ($(input).val() == $(input).attr("placeholder"));
		  }
			
	    return this.each(function() { 
	    	
	    	$(this).find(":input").each(function(){
				
				function showPlaceholder(input, reload) {
					if($(input).val() == "" || 
							(reload && valueIsPlaceholder(input))) {
						$(input).val($(input).attr("placeholder"));
					}
				};
				
				$(this).focus(function(){
					if($(this).val() == $(this).attr("placeholder")){
						$(this).val("");
					}
				});
				
				$(this).blur(function(){
					showPlaceholder($(this), false);
				});
				showPlaceholder($(this), true);
			});
	    	
	    	$(this).submit(function(){
				console.log("www");
				return false;
			});

	    });

	  };
	})( jQuery );