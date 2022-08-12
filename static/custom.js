$(document).ready(function(){

$(".choose-size").hide();

//default select first color and size and show price
    $(".choose-color").first().addClass('focused');
    var _vm=$(".choose-color").first().attr('data-color');
    
    $(".color"+_vm).show();
    $(".color"+_vm).first().addClass('active');
    var _price=$(".color"+_vm).first().attr('data-price');
    
    var _id=$(".color"+_vm).first().attr('product-id');
    $(".product-price").text(_price);
    $(".product-id").text(_id);
    
	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-color").removeClass('focused');
		$(this).addClass('focused');

		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color"+_color).first().addClass('active');

		var _price=$(".color"+_color).first().attr('data-price');
		var _id=$(".color"+_color).first().attr('product-id');
		$(".product-price").text(_price);
    $(".product-id").text(_id);
		console.log(_id,_price);

	});
	
	//choose Size

    $(".choose-size").on('click',function(){
    var _id=$(this).attr('product-id');
    var _price=$(this).attr('data-price');
    $(".choose-size").removeClass('active');
    $(this).addClass('active');
    $(".product-price").text(_price);
    $(".product-id").text(_id);
    

})


     $(".product-qty").keyup(function() {
     var qty=$(this).val();
     $(this).text(qty);
     })

//add to cart
    $(".add-to-cart").on('click',function(){
        
    var id=$(".product-id").html();
    
    var id1=$(".product-info").attr('data-id');
    var qty= $(".product-qty").val();
    var price=$(".product-price").html();
    var title=$(".product-title-"+id1).val();
    console.log(id); 
    
    
    $.ajax({
    url:'/addtocart',
    data:{
    'id':id,
    'qty':qty,
    'price':price,
    'title':title
    },
    datatype:'json',
    beforesend:function(){
    $(".add-to-cart").attr('disabled',true);
    
    },
    success:function(res){
    console.log(res.totalitems);
    $(".cart-list").text(res.totalitems);
    $(".add-to-cart").attr('disabled',false);
    }
    });
    
    });



    $(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

});