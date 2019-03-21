
// var check1,check2,check3,check4,check5,check6
//注册字段格式函数
function login_match(login_element,re){    
    login_element.blur(function(){
        var data =  this.value
        var check
        // 匹配相应的正则表达式,检查字符串是否合规
        var reg = re.test(data)
        if (reg){
            $(this).next('span').css('display','none')    
            check=true       
        }else{
            $(this).next('span').css('display','inline') 
            check=false
        }
        if (login_element.attr('name')=='phone_num' && check){
            var thisurl = '/register_phone?phone_num='+$(this).val()
            $.ajax({
                url:thisurl,
                type:'get',
                async:'false',
                success:function(data){
                    if (data == '1'){
                        console.log('1')
                        $("#phone_tip").html('手机号已被注册') 
                        $("#phone_tip").css('display','inline')
                    }else{
                        $("#phone_tip").css('display','none')
                        $("#phone_tip").html('格式不正确') 
                    }
                }
            })
        }
        return check
    })
}    
 


// //检查字段函数
// function re_check(elem,re){
//     var data =  elem.value
//     // 匹配相应的正则表达式,检查字符串是否合规
//     var reg = re.test(data)
//     if (reg){
//         $(elem).next('span').css('display','none')  
//         return true          
//     }else{
//         $(elem).next('span').css('display','inline') 
//         return false           
//     }
// }

// function register_check(){
//     if (
//         re_check($('#register_left input[name="uname"]'),/^[a-zA-Z\u4e00-\u9fa5_0-9]{3,15}$/) &&
//         re_check($('#register_left input[name="phone_num"]'),/^\d{11}$/) &&
//         re_check($('#register_left input[name="checkKey"]'),/^[0-9]{4}$/)&&    
//         re_check($('#register_left input[name="email"]'),/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)&&
//         re_check($('#register_left input[name="upwd"]'),/^\w{6,16}$/)&&
//         $('#register_left input[name="upwd"]').val() == $('#register_left input[name="upwd2"]').val()
//     ){
//         console.log(true)
//         return true
//     }else{
//         console.log(false)
//         return false
//     }
// }


 
//网页加载后需要执行的操作:
$(function(){
    // 注册用户名限制
    login_match($('#register_left input[name="uname"]'),/^[a-zA-Z\u4e00-\u9fa5_0-9]{3,15}$/)

    
    // 注册手机限制
    login_match($('#register_phone'),/^\d{11}$/)
    // 注册验证码限制:
    login_match($('#register_left input[name="checkKey"]'),/^[0-9]{4}$/)

    // // 注册邮箱限制
    login_match($('#register_left input[name="email"]'),/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)

    // 注册密码限制
    login_match($('#register_left input[name="upwd"]'),/^\w{6,16}$/)


    // 密码重复限制
    $('#register_left input[name="upwd2"]').blur(function(){
        var data = $('#register_left input[name="upwd"]').val()
        if ($(this).val()==data){
            $(this).next('span').css('display','none')    
            return true        
        }else{
            $(this).next('span').css('display','inline')            
            return false
        }
    })  
    
})