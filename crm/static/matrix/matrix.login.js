function keydown(e) {
    var e = e || event;
    var currKey = e.keyCode || e.which || e.charCode;
    if (currKey == 13) {
        checkLogin();
    }
}
function validatePwd(str) {
    if (str.length != 0) {
        reg = /^[A-Za-z]+[0-9]+[A-Za-z0-9]*|[0-9]+[A-Za-z]+[A-Za-z0-9]*$/;
        if (!reg.test(str)) {
            return false;
        } else {
            return true;
        }
    }
    return false;
}
$(document).ready(function () {
    var login = $('#loginform');
    var recover = $('#recoverform');
    var speed = 400;
    $('#to-recover').click(function () {
        $("#loginform").slideUp();
        $("#recoverform").fadeIn();
    });
    $('#to-login').click(function () {
        $("#recoverform").hide();
        $("#loginform").fadeIn();
    });
    if ($.browser.msie == true && $.browser.version.slice(0, 3) < 10) {
        $('input[placeholder]').each(function () {
            var input = $(this);
            $(input).val(input.attr('placeholder'));
            $(input).focus(function () {
                if (input.val() == input.attr('placeholder')) {
                    input.val('');
                }
            });
            $(input).blur(function () {
                if (input.val() == '' || input.val() == input.attr('placeholder')) {
                    input.val(input.attr('placeholder'));
                }
            });
        });
    }
    $("#modelClose").click(function () {
        $("#myModal").attr('class', 'modal hide');
    });



    $("#checkBtn").click(function(){

        $.ajax({
            url:"",
            type:"post",
            data:{
                user:$("#user").val(),
                pwd:$("#pwd").val(),
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()

            },
            success:function(res){
                console.log(res);
                if(res.user){
                    location.href="/stark/crm/customer/"
                }
                else{
                    alert("用户名或者密码错误!")
                }
            }
        })

    })
});