$ ->
  $icon = $('#header li.header-dropdown-section')
  $dropdown = $('#dropdown')
  $icon.hover ->
    $dropdown.css('left', $icon.position().left - $dropdown.innerWidth() + $icon.width())
    $dropdown.show()
  , ->
    $dropdown.hide()

