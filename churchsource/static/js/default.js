function toggle_check (id, value) {
  var obj = document.getElementById(id);
  if (obj.value == value) {
    obj.value = '';
  }
  
  else {
    obj.value = value;
  }
}
