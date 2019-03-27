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



//网页加载后需要执行的操作:
$(function () {

    // 注册用户名限制
    reg_match($('#uname'), /^[a-zA-Z\u4e00-\u9fa5_0-9]{3,15}$/);


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


function change_check() {
    var name = $("#uname-tip").html() == "通过验证";
    var email = $("#email-tip").html() == "通过验证";
    var upwd = $("#upwd-tip").html() == "通过验证";
    var ifupwd = $("#upwd2-tip").html() == "两次密码一致";
    console.log("name"+name);
    console.log("email"+ email);
    console.log("upwd"+ upwd);
    console.log("ifupwd"+ ifupwd);
    if (name && email && upwd && ifupwd) {
        alert("修改成功");
        return true
    } else {
        alert("信息不正确，请重新填写");
        return false
    }
}