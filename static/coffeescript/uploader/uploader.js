$(function() {
  var $uploader;
  $uploader = $('#material-uploader');
  $uploader.fileupload({
    done: function(event, response) {
      return $(response.result).each(function() {
        var $tr, data, form_url, table;
        data = this;
        console.log(this);
        form_url = data['form_url'];
        table = $uploader.find('table.files');
        $tr = $('<tr>').addClass('material-info-form');
        return $tr.load(form_url, function(data) {
          table.append($tr);
          $tr.toggle(false).toggle('normal');
          return $tr.find('input[type=submit]').click(function() {
            console.log($tr.find('form').serialize());
            $.post(form_url, $tr.find('form').serialize(), function(data) {
              return console.log(data);
            });
            return false;
          });
        });
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