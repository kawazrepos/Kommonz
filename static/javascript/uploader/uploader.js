(function() {
  $(function() {
    var $uploader;
    $uploader = $('#material-uploader');
    $uploader.fileupload({
      done: function(event, response) {
        return $(response.result).each(function() {
          var data;
          data = this;
          return console.log(this);
        });
      }
    });
    $.getJSON($uploader.find('form').prop('action'), function(files) {
      var fu;
      fu = $uploader.data('fileupload');
      fu._adjustMaxNumberOfFile(-files.length);
      return fu._renderDownload(files).append(material.find('.files')).fadeIn(function() {
        return $(this).show();
      });
    });
    return $uploader.find('.files a:not([target^=_blank])').live('click', function(e) {
      e.preventDefault();
      return $('iframe').css('display', 'none').prop('src', this.href).appendTo('body');
    });
  });
}).call(this);
