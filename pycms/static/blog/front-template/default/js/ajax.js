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
                $('#user-panel').fadeIn(1000);;
            }else if (data.status == "user not active"){
                alert('用户已被禁用');
            }else{
                alert("用户名或密码错误");
            }
        }
    );
    return false;
});
$('.panel-function a:last').bind('click',function(){
    $.ajax({type:"get",url:"/logout/"});
    $('#user-panel').hide();
    $('#user_login_div').fadeIn(1000);
    return false;
});
/*
$('#tellMeformSubmit').bind('click',function(){
    var fname_val = $('#fname').val();
    var fnext_val = $('#fnext').val();
    var femail_val = $('#femail').val();
    var fwebsite_val = $('#fwebsite').val();
    var fmessage_val = $('#fmessage').val();
    var csrfmiddlewaretoken_val = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type:"post",
        url:"/ajax/makecomment/",
        data:{'fusername':fname_val,
            'femail':femail_val,
            'fnext':fnext_val,
            'fwebsite':fwebsite_val,
            'fmessage':fmessage_val,
            'csrfmiddlewaretoken':csrfmiddlewaretoken_val,
            },
        success:function(data){
                alert(data);
            }
        });
        
    return false;
});
*/
jQuery.validator.setDefaults({
    debug: true,
    success: "valid"
});
$("#postComments").validate({
    onfocusout:true,
    rules: {
        fmessage: {
            required: true
        },
        fusername: "required",
        femail:{
            required: true,
            email: true,
        }
    }, 
    submitHandler: function(form){
        var fname_val = $('#fname').val();
        var fnext_val = $('#fnext').val();
        var femail_val = $('#femail').val();
        var fwebsite_val = $('#fwebsite').val();
        var fmessage_val = $('#fmessage').val();
        var csrfmiddlewaretoken_val = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type:"post",
            url:"/ajax/makecomment/",
            data:{'fusername':fname_val,
                'femail':femail_val,
                'fnext':fnext_val,
                'fwebsite':fwebsite_val,
                'fmessage':fmessage_val,
                'csrfmiddlewaretoken':csrfmiddlewaretoken_val,
                },
            success:function(data){
                    alert(data);
                }
            }); 
        return false;
    },
    invalidHandler: function(form, validator) {  //不通过回调
       return false;
    },

});
$.validator.messages = {
        required: "▲ 以上字段是必填的",
        email:"请输入合法E-mail",
        };
