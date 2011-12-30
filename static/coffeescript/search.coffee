$ ->
  $info = $('li.list-material li.info').click ->
    $(@).closest('li.list-material').find('article.material-info').toggle()
    $(@).toggleClass('open')
