$(function(){
  'use strict';
  $('#material-uploader').fileupload();
  // Load existing files:
  $.getJSON($('#material-uploader form').prop('action'), function (files) {
    console.log('hoge');
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
    $('<iframe style="display:none;"></iframe>')
    .prop('src', this.href)
    .appendTo('body');
  });

});
