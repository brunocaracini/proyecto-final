function set_light_mode(){
  $.getJSON("/config/set-light-mode",function (result){
    if (result == true){
      location.reload(true);
    }
  });
}

$(function() {
    // Sidebar toggle behavior
    $('#sidebarCollapse').on('click', function() {
      $('#sidebar, #content').toggleClass('active');
    });
  });




document.body.scrollTop = 0;

$( window ).resize(function() {
  navbarResize();
});

$.getJSON("/config/get-light-mode",function (result){
  if (result == 'day'){
    $('head').append('<link rel="stylesheet" type="text/css" href="/static/css/layout.css">');
    $(".nav-link").removeClass('text-light');
    $(".nav-link").addClass('text-dark');
    $("#theme-label").text("Tema oscuro");
    $(".fa-sun").hide();
    $(".fa-moon").show();
  }
  else{
    $('head').append('<link rel="stylesheet" type="text/css" href="/static/css/layout-oscuro.css">');
    $(".nav-link").removeClass('text-dark');
    $(".nav-link").addClass('text-light');
    $("#theme-label").text("Tema claro");  
    $(".fa-sun").show();
    $(".fa-moon").hide();
  }
  $("body").fadeIn();
});

$("#img-nav-bar").fadeIn(1000);
$("#img-nav-bar").css("transform","translateZ(0)");

function navbarResize(){
  if( $( window ).width() < 768){
    $("#up-bar").css({"width":"100%"});
    $("#up-bar").css({"margin-left":"0px"});
  }
  else{
    $("#up-bar").css({"margin-left":"calc(15.5rem - 8px)"});
    $("#up-bar").css({"width":"82.3%"});

  }
}

$.getJSON("/layout/datos-usuario",function (result){
    showElementos(result["modulos"])
    $("#nombreUsuarioNavBar").text(result["nombre"]);
    $("#cantEPNavBar").text(result["totalEP"]);
    $("#user-profile-img-navbar").attr("src", result["img"]);
    if (result["carrito"]== false){
      $("#carrito-cant-items").text("0");
    }
    else{
      cantidad = 0;
      carrito = result["carrito"];
      for (var item in carrito){
        cantidad += parseFloat(carrito[item]);
      }
      $("#carrito-cant-items").text(cantidad);
    }
});

//Redirige al url que recibe como parámetro.
function redirect(link){
  window.location.href = link;
}

//Redirige al url que recibe como parámetro en una nueva pestaña.
function redirectBlank(link){
window.open(
  link,
  '_blank' // <- This is what makes it open in a new window.
);
}

function isNumberKey(txt, evt) {
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if (charCode == 46) {
    //Check if the text already contains the . character
    if (txt.value.indexOf('.') === -1) {
      return true;
    } else {
      return false;
    }
  } else {
    if (charCode > 31 &&
      (charCode < 48 || charCode > 57))
      return false;
  }
  return true;
}

function isNumberKeyEntiresOnly(txt, evt) {
  var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 &&
      (charCode < 48 || charCode > 57))
      return false;
  return true;
}



function showElementos(modulos){
  if(modulos.length >= 1){
    if(modulos.includes(8) || modulos.includes(12)){
      $("#layout-li-pedidos").show();
    }
    if(modulos.includes(9)){
      $("#layout-li-depositos").show();
    }
    if(modulos.includes(2)){
      $("#layout-li-articulos").show();
    }
    if(modulos.includes(1)){
      $("#layout-li-insumos").show();
    }
    if(modulos.includes(16)){
      $("#layout-li-materiales").show();
    }
    if(modulos.includes(11)){
      $("#layout-li-stock").show();
    }
    if(modulos.includes(5)){
      $("#layout-li-produccion").show();
    }
    if(modulos.includes(4) || modulos.includes(10)){
      $("#layout-li-usuarios").show();
    }
    if(modulos.includes(6)){
      $("#layout-li-entidades").show();
    }
    if(modulos.includes(3)){
      $("#layout-li-niveles").show();
    }
    if(modulos.includes(7) || modulos.includes(15)){
      $("#layout-li-puntos").show();
    }
    if(modulos.includes(14)){
      $("#layout-li-reportes").show();
    }
    if(modulos.includes(13)){
      $("#layout-li-config").show();
    }
  
    $("#admin-label").show();
    $("#layout-li-ayuda").show();
  }
}