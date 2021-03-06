$ ->
  $uploader = $('#material-uploader')
  $infoForms = $ ".material-info-forms"
  file_id = undefined
  $uploader.fileupload
    autoUpload : true
    maxNumberOfFiles : 1
    send : (event, response) ->
      form_url = $infoForms.attr 'form-url'
      validate_url = $infoForms.attr 'validate-url'
      filename = response.files[0].name
      $infoForm = $('<div>').addClass 'material-info-form'
      $infoForm.load "#{form_url}?filename=#{encodeURI(filename)}", (data) ->
        $form = $(@).find('form')
        $form.attr('action', form_url)
        $form.find('#id__file').val(file_id)
        if not file_id
          $form.find("input[type='submit']").hide()
        $form.find('#id_label').val(filename)
        $syntax = $form.find('#id_syntax')
        if $syntax and filename.match(/\.(.*?)$/)
          $syntax.val(RegExp.$1)
        $form.submit ->
          $.post validate_url, $form.serialize(), (data) ->
            if(data['status'] is 'success')
              $form.get(0).submit()
            else if(data['status'] is 'error')
              for field, values of data['errors']
                for value in values
                  $e = $('<p>').append(value).addClass('material-form-error')
                  $form.find('.material-form-error').remove()
                  $form.find("#id_#{field}").after($e)
          , 'json'
          false
        $infoForms.append @
        $(@).toggle(false)
         .toggle 'slow'
      true
    done : (event, response) ->
      $(response.result).each ->
        $fileField = $('#id__file')
        file_id = @['id']
        $fileField.val(@['id'])
        $('.material-info-form').find("input[type='submit']").show()
      false
  
  $.getJSON $uploader.find('form').prop('action'), (files) ->
    fu = $uploader.data('fileupload')
    fu._adjustMaxNumberOfFile(-files.length)
    fu._renderDownload(files)
      .append(material.find('.files'))
      .fadeIn -> 
        $(@).show()
  
  $uploader.find('.files a:not([target^=_blank])').live 'click', (e) ->
    e.preventDefault()
    $('iframe').css('display', 'none')
      .prop('src', @href)
      .appendTo('body')
