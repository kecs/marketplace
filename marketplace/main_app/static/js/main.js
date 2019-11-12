// Switch between languages
jQuery(function(){
  $('.choose-lang').click(function(e){
    e.preventDefault();
    $('.hidden-form-1').submit();
  });
});
