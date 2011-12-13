$(function(){
  $.fn.postConfirm = function(settings){
    settings = $.extend({
      messages : '',
      postURL : $(this).attr('href'),
      postParams : {},
      success : function (data){}
    }, settings);
    console.log(this);
    $(this).attr('href', 'javascript:void(0)');
    $(this).bind('click', function(){
      if(typeof(settings.messages) === 'string'){
        settings.messages = [settings.messages];
      }
      if(typeof(settings.messages) === 'object') {
        var size = settings.messages.length;
        var count = 0;
        var callback = function(){
          if(size-1 == count){
            $.post(settings.postURL, settings.postParams, settings.success);
          } else {
            ++count;
            if(confirm(settings.messages[count])) callback();
          }
        }
        if(confirm(settings.messages[count])) callback();
      }
      return false;
    });
  }
}());
