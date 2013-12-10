$('#login-submit').bind('click',function(){
    var username_val = $('#username').val();
    var pwd_val = $('#pwd').val();
    var csrfmiddlewaretoken_val = $('[name=csrfmiddlewaretoken]').val();
    $.post("/ajax/login/",
        {"username":username_val,
        "password":pwd_val,
        "csrfmiddlewaretoken":csrfmiddlewaretoken_val,
        },
        function(data){
            data = $.parseJSON(data);
            if (data.status == "success"){
                $('#user_login_div').hide();
                $('#user-panel .widget a').html(data.username);
                
                $('#user-panel').show();
            }else if (data.status == "user not active"){
                alert('用户已被禁用');
            }else{
                alert("用户名或密码错误");
            }
        }
    );
    return false;
});
