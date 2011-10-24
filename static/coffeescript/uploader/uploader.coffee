$ ->
  $uploader = $('#material-uploader')
  $uploader.fileupload
    done : (event, response) ->
      $(response.result).each ->
        data = this
        console.log(this)
  
  $.getJSON $uploader.find('form').prop('action'), (files) ->
    fu = $uploader.data('fileupload')
    fu._adjustMaxNumberOfFile(-files.length)
    fu._renderDownload(files)
      .append(material.find('.files'))
      .fadeIn -> 
        $(this).show()
  
  $uploader.find('.files a:not([target^=_blank])').live 'click', (e) ->
    e.preventDefault()
    $('iframe').css('display', 'none').prop('src', this.href).appendTo('body')
