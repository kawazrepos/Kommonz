$ ->
  $uploadButton = $('li.header-button-section a.upload-button')
  $uploadButton.click (e) ->
    url = $(@).attr 'href'
    $container = $('<div>').addClass('lightbox')
    $iframe = $('<iframe>')
    $iframe.attr 'src', url
    $('body').append $container
    $container.append($("<div>").addClass('close')).append($iframe)
    $container.ready ->
      $container.lightbox_me {
        closeClick : false,
        closeEsc : false,
      }
    false
