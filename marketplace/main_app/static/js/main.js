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
});
