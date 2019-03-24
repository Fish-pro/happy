function reg_match(element, re) {
    element.blur(function () {
        var data = this.value;
        var check;
        var reg = re.test(data);
        if (reg) {
            $(this).next("span").html("通过验证").css("color", "green")
            return true
        } else {
            $(this).next("span").html("格式不正确").css("color", "red")
            return false
        }
    })
}

function send_phone() {
    $('#register_phone').blur(function () {
        var data = $(this).val();
        var re = /^\d{11}$/;
        var reg = re.test(data);
        if (reg) {
            $.ajax({
                url: "/reg_phone",
                type: 'get',
                dataType: "json",
                data: "phone_num=" + data,
                async: false,
                success: function (data) {
                    if (data.num == 1) {
                        $("#phone_tip").html('手机号已被注册').css("color", "red")
                        return false
                    } else {
                        $("#phone_tip").html('手机号可用').css("color", 'green')
                        return true
                    }
                }
            })
        } else {
            $("#phone_tip").html('手机格式不正确').css("color", "red")
            return false
        }
    });
}

function check_phone_key() {
    $("#check>input").blur(function () {
        var key = $(this).val();
        console.log(key);
        if (key == check_key) {
            $("#check-tip").html('验证成功').css("color", 'green');
            return true
        } else {
            $("#check-tip").html('验证码错误').css("color", 'red');
            return false
        }
    });
}


var check_key;//全局变量保存验证码

//网页加载后需要执行的操作:
$(function () {

    // 注册用户名限制
    reg_match($('#uname'), /^[a-zA-Z\u4e00-\u9fa5_0-9]{3,15}$/);

    // 注册手机限制
    send_phone();


    //点击获取验证码
    $("#check a").click(function () {
        var phone_num = $("#register_phone").val();
        $.ajax({
            url: "/check_phone",
            type: 'get',
            data: "phone_num=" + phone_num,
            dataType: "json",
            async: false,
            success: function (data) {
                if (data.code == 2) {
                    $("#phone_tip").html("验证码已发送").css("color", 'green');
                    check_key = data.key
                    console.log(check_key);
                } else {
                    $("#phone_tip").html('请稍后重试').css("color", 'red');
                }
            }
        });
    });

    //验证码核对
    check_phone_key();

    // 注册邮箱限制
    reg_match($('#email'), /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/);

    // 注册密码限制
    reg_match($('#upwd'), /^\w{6,16}$/);


    // 密码重复限制
    $('#upwd2').blur(function () {
        var data = $('#upwd').val();
        if ($(this).val() == data) {
            $(this).next('span').html("两次密码一致").css('color', 'green')
            return true
        } else {
            $(this).next('span').html("两次密码不一致").css('color', 'red')
            return false
        }
    });


});


function end_check() {
    var name = $("#uname-tip").html() == "通过验证";
    var ifcheck = $("#check-tip").html() == "验证成功";
    var email = $("#email-tip").html() == "通过验证";
    var upwd = $("#upwd-tip").html() == "通过验证";
    var ifupwd = $("#upwd2-tip").html() == "两次密码一致";
    console.log("name"+name);
    console.log("ifcheck:"+ ifcheck);
    console.log("email"+ email);
    console.log("upwd"+ upwd);
    console.log("ifupwd"+ ifupwd);
    if (name && ifcheck && email && upwd && ifupwd) {
        alert("注册成功");
        return true
    } else {
        alert("信息不正确，请重新填写");
        return false
    }
}