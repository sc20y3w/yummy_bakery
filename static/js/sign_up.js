function bind(){
    $("#captcha-btn").on("click",function (event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if (!email){
            alert("Please enter email address");
            return;
        }
        // Send a net request by ajax
        $.ajax({
            url:"/baker/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res){
                var code = res['code'];
                if(code == 200){
                    $this.off("click"); // Cancel the click
                    var count=60;// Start the countdown
                    var timer = setInterval(function (){
                        count = count-1;
                        if(count > 0){
                            $this.text(count+"resend 1s later");
                        }else {
                            $this.text("send");
                            bind(); // re-bind
                            clearInterval(timer); //clear countdown
                        }
                    },1000) // Start the countdown
                    alert("success")
                }else {
                    alert(res['message']);
                }
            }
        })
    });
}

$(function (){
    bind();
});