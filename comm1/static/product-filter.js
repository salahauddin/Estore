$(document).ready(function(){
	$(".ajaxLoader").hide();
	// Product Filter Start
	$(".filter-checkbox").on('click',function(){
		var _filterobj = {};
    	
    	
    	$(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
			console.log(_filterObj[_filterKey]);
		});
		

    	
    	
	// End

	// Filter Product According to the price
	
	// End
});