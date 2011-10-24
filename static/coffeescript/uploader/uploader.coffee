$ ->
  $uploader = $('#material-uploader')
  $uploader.fileupload
    done : (event, response) ->
      $(response.result).each ->
        data = this
        console.log(this)
        form_url = data['form_url']
        table = $uploader.find('table.files')
        $tr = $('<tr>').addClass('material-info-form')
        $tr.load form_url, (data) ->
          table.append($tr)
          $tr.toggle(false)
            .toggle('normal')
          $tr.find('input[type=submit]').click ->
            console.log($tr.find('form').serialize())
            $.post form_url, $tr.find('form').serialize(), (data) ->
              console.log(data)
            return false
  
  $.getJSON $uploader.find('form').prop('action'), (files) ->
    fu = $uploader.data('fileupload')
    fu._adjustMaxNumberOfFile(-files.length)
    fu._renderDownload(files)
      .append(material.find('.files'))
      .fadeIn -> 
        $(this).show()
  
  $uploader.find('.files a:not([target^=_blank])').live 'click', (e) ->
    e.preventDefault()
    $('iframe').css('display', 'none')
      .prop('src', this.href)
      .appendTo('body')
