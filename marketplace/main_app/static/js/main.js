jQuery(function(){
  // Switch between languages 
  $('.choose-lang').click(function(e){
    e.preventDefault();
    $('.hidden-form-1').submit();
  });

  // Send like/watch
  $('.send-like-watch').click(function(e){
    e.preventDefault();

    console.log(e.target)
    var verb = $(e.target).data('verb'),
	pk = $(e.target).data('pk'),
	csrf = $(e.target).data('csrf'),
	url = '/' + verb + '/' + pk + '/';

    $.ajax({
      url : url,
      type: "POST",
      data : {csrfmiddlewaretoken: csrf},
      dataType : "json",
      success: function( data ){
        window.location.reload();
      }
    });
  });

  // Show "send bid" button
  $('.show-send-bid').click(function(){
    $('.place-bid-inp').show();
    $('.place-bid-send').show();
  });

  // Send bid
  $('.place-bid-send').click(function(e){
    var actualPrice = parseInt($(e.target).data('actual-price')),
	usersBid = parseInt($('.place-bid-inp').value());

    console.log(actualPrice, usersBid)
	
    // if()
    
    if(confirm($(e.target).data('confirm'))){
      $.ajax({
	url : url,
	type: "POST",
	data : {csrfmiddlewaretoken: csrf},
	dataType : "json",
	success: function( data ){
          window.location.reload();
	}
      });
    }else{
      $('.place-bid-inp').hide();
      $('.place-bid-send').hide();
    };
  });
  
});
