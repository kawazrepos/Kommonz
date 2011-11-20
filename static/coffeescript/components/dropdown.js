$(function() {
  var $dropdown, $icon;
  $icon = $('#header li.header-dropdown-section');
  $dropdown = $('#dropdown');
  return $icon.hover(function() {
    $dropdown.css('left', $icon.position().left - $dropdown.innerWidth() + $icon.width());
    return $dropdown.show();
  }, function() {
    return $dropdown.hide();
  });
});