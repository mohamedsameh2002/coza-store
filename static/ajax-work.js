$(document).ready(function(){
	//remove load more button
	var _total=$('#loadMore').attr('data-total');
	var _totalShowing=$(".product-box").length;
	if(_totalShowing==_total){$("#loadMore").hide();}
    $(".ajaxLoader").hide();
    $(".loadmore-loder").hide();
    $(".filter-checkbox,#priceFilterBtn").on('click',function(){
		var _total=$('#loadMore').attr('data-total');
        var _filterObj={};
		var _minPrice=$('#maxPrice').attr('min');
		var _maxPrice=$('#maxPrice').val();
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;
        $(".filter-checkbox").each(function(index,ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
            });
		});
		var search_kewrd = new URLSearchParams(window.location.search).get('search');
		
        // ajax
        $.ajax({
			url:'/products/filter-data/',
			data:{
				_filterObj:_filterObj,
				search_kewrd:search_kewrd,

			},
			dataType:'json',
			beforeSend:function(){
                $(".ajaxLoader").show();
			},
			success:function(res){
				$(".ajaxLoader").hide();
				$("#filterProducts").html(res.data);
				var _totalShowing=$(".product-box").length;
				if(_totalShowing<_total){$("#loadMore").show();}
				if(_totalShowing==res.count){$("#loadMore").hide();}
				else {$("#loadMore").show();}
                
			}
		});
		
	});


	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		//
        var _filterObj={};
		var _minPrice=$('#maxPrice').attr('min');
		var _maxPrice=$('#maxPrice').val();
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;
        $(".filter-checkbox").each(function(index,ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
            });
		});
		var search_kewrd = new URLSearchParams(window.location.search).get('search');
		//ajax
		$.ajax({
			url:'/products/load/',
			data:{
				_filterObj:_filterObj,
				limit:_limit,
				offset:_currentProducts,
				search_kewrd:search_kewrd,
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".loadmore-loder").show();
				$(".loadmor-text").hide();
			},
			success:function(res){
				$("#loadMore").attr('disabled',false);
				$("#filterProducts").append(res.data);
				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){$("#loadMore").hide();}
				if(_totalShowing==res.count){$("#loadMore").hide();}
				else {$("#loadMore").show();}
				$(".loadmore-loder").hide();
				$(".loadmor-text").show();
				
				
			}
		});
	});



});