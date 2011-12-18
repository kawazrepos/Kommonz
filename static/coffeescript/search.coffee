$ ->
  $info = $('li.search-material li.info').click ->
    $(@).closest('li.search-material').find('article.material-info').toggle()
    $(@).toggleClass('open')
