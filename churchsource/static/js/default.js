function toggle_check (id, value) {
  var obj = document.getElementById(id + "_hidden");
  if (obj.value == value) {
    obj.value = '';
    jQuery('#' + id + '_label img').attr('src', MEDIA_URL + 'img/unchecked.png');
  }
  
  else {
    obj.value = value;
    jQuery('#' + id + '_label img').attr('src', MEDIA_URL + 'img/checked.png');
  }
}

function display_errors (cname) {
  jQuery("ul." + cname).each(function () {
    jQuery(this).children('li').each(function () {
      if (jQuery(this).children('ul.errorlist').length > 0) {
        var html = jQuery(this).children('ul.errorlist').children().html();
        jQuery(this).append("<div class=\"error\">" + html + "</div>");
      }
    });
  });
  $('li').first()
}
