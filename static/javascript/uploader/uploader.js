(function() {
  $(function() {
    var $infoForms, $uploader, file_id;
    $uploader = $('#material-uploader');
    $infoForms = $(".material-info-forms");
    file_id = void 0;
    $uploader.fileupload({
      autoUpload: true,
      maxNumberOfFiles: 1,
      send: function(event, response) {
        var $infoForm, filename, form_url, validate_url;
        form_url = $infoForms.attr('form-url');
        validate_url = $infoForms.attr('validate-url');
        filename = response.files[0].fileName;
        $infoForm = $('<div>').addClass('material-info-form');
        $infoForm.load("" + form_url + "?filename=" + filename, function(data) {
          var $form, $syntax;
          $form = $(this).find('form');
          $form.attr('action', form_url);
          $form.find('#id__file').val(file_id);
          if (!file_id) {
            $form.find("input[type='submit']").hide();
          }
          $form.find('#id_label').val(filename);
          $syntax = $form.find('#id_syntax');
          if ($syntax && filename.match(/\.(.*?)$/)) {
            $syntax.val(RegExp.$1);
          }
          $form.submit(function() {
            $.post(validate_url, $form.serialize(), function(data) {
              var $e, field, value, values, _ref, _results;
              if (data['status'] === 'success') {
                return $form.get(0).submit();
              } else if (data['status'] === 'error') {
                _ref = data['errors'];
                _results = [];
                for (field in _ref) {
                  values = _ref[field];
                  _results.push((function() {
                    var _i, _len, _results2;
                    _results2 = [];
                    for (_i = 0, _len = values.length; _i < _len; _i++) {
                      value = values[_i];
                      $e = $('<p>').append(value).addClass('material-form-error');
                      $form.find('.material-form-error').remove();
                      _results2.push($form.find("#id_" + field).after($e));
                    }
                    return _results2;
                  })());
                }
                return _results;
              }
            }, 'json');
            return false;
          });
          $infoForms.append(this);
          return $(this).toggle(false).toggle('slow');
        });
        return true;
      },
      done: function(event, response) {
        $(response.result).each(function() {
          var $fileField;
          $fileField = $('#id__file');
          file_id = this['id'];
          $fileField.val(this['id']);
          return $('.material-info-form').find("input[type='submit']").show();
        });
        return false;
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
