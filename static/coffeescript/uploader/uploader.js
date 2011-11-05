(function() {
  $(function() {
    var $infoForms, $uploader;
    $uploader = $('#material-uploader');
    $infoForms = $(".material-info-forms");
    $uploader.fileupload({
      autoUpload: true,
      maxNumberOfFiles: 1,
      send: function(event, response) {
        var $infoForm, form_url;
        form_url = $infoForms.attr('form-url');
        console.log(form_url);
        $infoForm = $('<div>').addClass('material-info-form');
        $infoForm.load(form_url, function(data) {
          $(this).find("form").attr('action', form_url);
          $infoForms.append(this);
          return $(this).toggle(false).toggle('slow');
        });
        return true;
      },
      done: function(event, response) {
        $(response.result).each(function() {
          var $fileField;
          $fileField = $('#id__file');
          console.log($fileField);
          console.log(this['id']);
          return $fileField.val(this['id']);
        });
        return true;
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
