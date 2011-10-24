$(function(){
  'use strict';
  $('#material-uploader').fileupload({
    onComplete : function(event, files, index, xhr, handler){
      var data = handler.response;
      console.log(data);
    }
  });
  // Load existing files:
  $.getJSON($('#material-uploader form').prop('action'), function (files) {
    console.log(files);
    var fu = $('#material-uploader').data('fileupload');
    console.log(fu);
    fu._adjustMaxNumberOfFiles(-files.length);
    fu._renderDownload(files)
    .appendTo($('#material-uploader .files'))
    .fadeIn(function () {
      // Fix for IE7 and lower:
      $(this).show();
    });
  });

  // Open download dialogs via iframes,
  // to prevent aborting current uploads:
  $('#material-uploader .files a:not([target^=_blank])').live('click', function (e) {
    e.preventDefault();
    $('iframe').css('display', 'none').prop('src', this.href).appendTo('body');
  });

});
