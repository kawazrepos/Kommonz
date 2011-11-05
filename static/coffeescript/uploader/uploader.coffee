$ ->
  $uploader = $('#material-uploader')
  $infoForms = $ ".material-info-forms"
  $uploader.fileupload
    autoUpload : true
    maxNumberOfFiles : 1
    send : (event, response) ->
      form_url = $infoForms.attr 'form-url'
      console.log form_url
      $infoForm = $('<div>').addClass 'material-info-form'
      $infoForm.load form_url, (data) ->
        #$(@).find("input[type='submit']").hide()
        $(@).find("form").attr('action', form_url)
        $infoForms.append @
        $(@).toggle(false)
         .toggle 'slow'
      true
    done : (event, response) ->
      $(response.result).each ->
        $fileField = $('#id__file')
        console.log($fileField)
        console.log(@['id'])
        $fileField.val(@['id'])
      true
  
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
