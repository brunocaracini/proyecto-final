var img_hide = false;
var email = false;
var password = false;
var first_time = true;
var first_time2 = true;
var repeat_password = false;
var domain = "";
var emails = [];

$.getJSON("/register/emails",function (result){
    emails = result;
});

$( window ).resize(function() {
    reduceWindow();
});

$(".content-container").fadeIn();
$(".content-container").css({"transform":"translateX(7rem)"});


function reduceWindow(){
    if($( window ).width() < 1050 && $( window ).width() > 800){
        $(".content-container").css({"transform":"translateX(4rem)"});
    }
    if ($( window ).width() < 800){
        if (img_hide == false){
            $(".img-login").fadeOut();
            $(".content-container").css({"transform":"translateX(-57%)"});
            $("#register-label").css({"width":"130%"});
            $("#register-label").css({"transform":"translateX(-57%)"});
            img_hide = true;
        }
    }
    else if ($( window ).width() > 800){
        if (img_hide == true){
            $(".img-login").fadeIn(1000);
            $(".content-container").css({"transform":"translateX(7rem)"});
            $("#register-label").css({"width":"96%"});
            $("#register-label").css({"transform":"translateX(0%)"});


            img_hide = false;
        }
    } 
}

function submitLogin(){
    if (email && password){
        email_val = $("#email-input").val();
        password_val = $("#password-input").val();
        $("#error-msg-login").hide();

        $("#loadingRowLogin").fadeIn();
        $("#loading-text-login").fadeIn();
        $("#olvido-password").hide();
        $("#start-button").hide();
        $("#email-input-group").hide();
        $("#password-input-group").hide();
        $("#pass-reqs-row").hide();
        $("#repeat-password-input-group").hide();
        $(".form-check").hide();
        $.getJSON("/register/alta-usuario/"+String(email_val)+"/"+String(password_val),function (result){
            if(result){
                domain = "";
                add = false;
                for (var i in String(email_val)){
                    if (add){
                        domain += email_val[i];
                    }
                    else if (email_val[i] == "@"){
                        add = true;
                    }
                }
                $("#email-button").text("Ir a " + domain);
                $(".register-form").fadeOut();
                $("#email-container").fadeIn();
                $("#email-direction-label").text(email_val);
            }
            else if (result == "Email"){
                $(".error-msg-text").text("¡Ups! Hay un problema con tu dirección de email")
                $("#loadingRowLogin").hide();
                $("#loading-text-login").hide();
                $("#error-msg-login").fadeIn();
                $("#olvido-password").fadeIn();
                $("#start-button").fadeIn();
                $("#email-input-group").fadeIn();
                $("#password-input-group").fadeIn();
                $("#pass-reqs-row").fadeIn();
                $("#repeat-password-input-group").fadeIn();
                $(".form-check").fadeIn();
            }
            else if (result == "Password"){
                $(".error-msg-text").text("¡Ups! Hay un problema con tu dirección de contraseña")
                $("#loadingRowLogin").hide();
                $("#loading-text-login").hide();
                $("#error-msg-login").fadeIn();
                $("#olvido-password").fadeIn();
                $("#start-button").fadeIn();
                $("#email-input-group").fadeIn();
                $("#password-input-group").fadeIn();
                $("#pass-reqs-row").fadeIn();
                $("#repeat-password-input-group").fadeIn();
                $(".form-check").fadeIn();
            }
            else{
                $(".error-msg-text").text("¡Ups! Algo salió mal al crear tu cuenta")
                $("#loadingRowLogin").hide();
                $("#loading-text-login").hide();
                $("#error-msg-login").fadeIn();
                $("#olvido-password").fadeIn();
                $("#start-button").fadeIn();
                $("#email-input-group").fadeIn();
                $("#password-input-group").fadeIn();
                $("#pass-reqs-row").fadeIn();
                $("#repeat-password-input-group").fadeIn();
                $(".form-check").fadeIn();
            }
        });
    }
}

function redirectBlank(){
    link = "https://" + domain;
    window.open(
        link,
        '_blank' // <- This is what makes it open in a new window.
    );
    }

function validateEmail(elementValue){      
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (emailPattern.test(elementValue) && !(emails.includes(elementValue))){
        email = true;
    }
    else{
        email = false;
    }
    if (email){
        $("#email-error").fadeOut();
        $("#email-vacio").show();
    }
    else{
        if ((emails.includes(elementValue))){
            $("#email-error").text("* El email que ingresó ya ha sido utilizado.");
        }
        else{
            $("#email-error").text("* Formato de email incorrecto.");
        }
        $("#email-error").fadeIn();
        $("#email-vacio").hide();
    }
    if (first_time){
        first_time = false;
    }
    enable_disable_button();
}

function validateEmail2(elementValue){
    if (String(elementValue) == ""){
        email = false;
        enable_disable_button();
    }
    
    if (first_time == false){
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (emailPattern.test(elementValue) && !(emails.includes(elementValue))){
            email = true;
        }
        else{
            email = false;
        }
        if (email){
            $("#email-error").fadeOut();
            $("#email-vacio").show();
        }
        else{
            if ((emails.includes(elementValue))){
                $("#email-error").text("* El email que ingresó ya ha sido utilizado.");
            }
            else{
                $("#email-error").text("* Formato de email incorrecto.");
            }
            $("#email-error").fadeIn();
            $("#email-vacio").hide();
        }
        enable_disable_button();
    }     
    
}

function validateEmail3(elementValue){ 
    alert(elementValue)
    if (elementValue == ""){
        email = true;
    }
    else{
        email = false;
    }
    enable_disable_button();
}

function validaPassword(){
    value = $("#password-input").val();
    var re = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[a-zA-Z!#$%&? "])[a-zA-Z0-9!#$%&?]{8,20}$/;
    if(re.test(value)){
        password = true;
    }
    else{
        password = false;
    }

    if(password){
        $("#password-error").fadeOut();
        $("#pass-vacio").show();
    }
    else{
        if (String(value) == ''){
            $("#password-error").fadeIn();
            $("#pass-vacio").hide();
            $("#password-error").text("* La contraseña no puede quedar vacía.");
        }
        else{
            $("#password-error").fadeIn();
            $("#pass-vacio").hide();
            $("#password-error").text("* La contraseña no cumple con los requisitos.");
        }
    }
    validaPassRep(false);
    enable_disable_button();
}

function enable_disable_button(){
    terms_and_conditions = $("#exampleCheck1").is(":checked");
    if (password && email && repeat_password && terms_and_conditions){
        $("#start-button").css({"background-color":"#95C22B"});
        $("#start-button").css({"border":"1px solid #95C22B"});
    }
    else{
        $("#start-button").css({"background-color":"#d8d9e2"});
        $("#start-button").css({"border":"1px solid #d8d9e2"});
    }
}


function validaPassRep(user_call=true){
    if (first_time2 & user_call){
        first_time2 = false;
    }
    if (first_time2==false){
        if ($("#repeat-password-input").val() == $("#password-input").val()){
            repeat_password = true;
            $("#repeat-password-error").hide();
        }
        else{
            repeat_password = false;
            $("#repeat-password-error").show();
        }
        enable_disable_button();
    }    
}

$("#start-button").css({"background-color":"#d8d9e2"});
$("#start-button").css({"border":"1px solid #d8d9e2"});

var pos_check = document.getElementById("exampleCheck1").offsetLeft;
$("#check-label").css({left: pos_check + 10, position:'absolute'});


