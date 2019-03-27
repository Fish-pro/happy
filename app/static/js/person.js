<!-- 展开按钮 -->
$(function () {
    $(".contentBottom .extend").each(function () {
        $(this).click(function () {
            $(this).parent("div").prev("input").prev("div").css("height", "auto");
        });
    });
    $(".talk").each(function () {
        $(this).click(function () {
            $(this).parent("ul").parent(".contentBottom").next(".commit").css("display", "block");
        });
    });

    //全局变量记录登录状态
    var user_active = $("#user_active").val();
    //评论操作
    $(".submit_comment").click(function () {
        if (user_active != "0") {
            var note_id = $(this).parents(".commit").prev(".contentBottom").prev(".note_id").val()
            var text = $(this).prev(".talkContent").val();
            console.log(note_id);
            console.log(text);
            var commitTalk = $(this).parents(".commitTalk");
            $.ajax({
                url: "/comment",
                data: "note_id=" + note_id + "&" + "text=" + text,
                type: "get",
                dataType: "json",
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i].date);
                        console.log(data[i].content);
                        var html = "";
                        html += "<div class='commitHistory'><div class='head1'><img src='";
                        html += data[i].head_path + "'></div><div class='historyContent'><p><b>";
                        html += data[i].name + "说：</b>";
                        html += data[i].comment_content + "(";
                        html += data[i].date + ")</p></div><div class='commitlike'><ul><li><img src='../static/images/like.jpg'>";
                        html += data[i].raise + "</li><li><img src='../static/images/unlike.png'>";
                        html += data[i].down + "</li></ul></div></div>";
                        commitTalk.after($(html));
                    }
                }
            });
        } else {
            alert("你还没有登录呢")
        }
        $(this).prev(".talkContent").val("");
    });

    //点赞功能
    //全局变量记录点赞次数
    $(".contentBottom .like img").click(function () {
        if (user_active == "0") {
            alert("登陆之后才能点赞哦！");
        } else {
            var note_id = $(this).parent(".like").parents(".contentBottom").prev(".note_id").val();
            var span = $(this).next("span");
            $.ajax({
                url: "/like",
                type: "get",
                data: "note_id=" + note_id,
                dataType: "json",
                async: false,
                success: function (data) {
                    span.html(data.raise);
                }
            });
        }
    });


    //踩功能
    $(".contentBottom .unlike img").click(function () {
        if (user_active == "0") {
            alert("登陆之后才能踩哦！");
        } else {
            var note_id = $(this).parent(".unlike").parents(".contentBottom").prev(".note_id").val();
            var span1 = $(this).next("span");
            $.ajax({
                url: "/unlike",
                type: "get",
                data: "note_id=" + note_id,
                dataType: "json",
                async: false,
                success: function (data) {
                    span1.html(data.down);
                }
            });
        }
    });

    //评论点赞
    $(".com_like img").click(function () {
        if (user_active == "0") {
            alert("登陆之后才能点赞哦！");
        } else {
            var com_id = $(this).parents(".commitlike").prev(".com_id").val();
            console.log(com_id);
            var span3 = $(this).next("span");
            console.log("haha");
            $.ajax({
                url: "/com_like",
                type: "get",
                data: "com_id=" + com_id,
                dataType: "json",
                success: function (data) {
                    span3.html(data.raise);
                }
            });
        }
    });


    //评论踩
    $(".com_unlike img").click(function () {
        if (user_active == "0") {
            alert("登陆之后才能踩哦！");
        } else {
            var com_id = $(this).parents(".commitlike").prev(".com_id").val();
            console.log(com_id);
            var span4 = $(this).next("span");
            console.log("haha");
            $.ajax({
                url: "/com_unlike",
                type: "get",
                data: "com_id=" + com_id,
                dataType: "json",
                success: function (data) {
                    span4.html(data.down);
                }
            });
        }
    });
    $(".addbook img").click(function () {
        if (user_active == "0") {
            alert("登陆之后才收藏哦！");
        } else {
            var note_id = $(this).parents(".contentBottom").prev(".note_id").val();
            console.log(note_id);
            console.log("haha");
            $.ajax({
                url: "/addbook",
                type: "get",
                data: "note_id=" + note_id,
                dataType: "json",
                success: function (data) {
                    if (data.num == 1) {
                        alert("收藏成功，你可以前往个人中心查看");
                    } else if (data.num == 2) {
                        alert("你已经收藏过该帖子了，请前往个人中心查看")
                    } else {
                        alert("出错了，请稍后重试");
                    }
                }
            });
        }
    });

    //指定页数跳转
    $("#choosePage").click(function () {
        var lastPage = Number($("#lastPage").text());
        console.log(lastPage);
        var choosepPage = $("#pageinput1").val();
        var id = $("#pageinput2").val();
        if (choosepPage > 0 && choosepPage <= lastPage) {
            window.location.href = "/person?user_id=" + id + "&choosePage=" + choosepPage
        } else {
            alert("不在页数范围之内呢")
        }
    });

    //页面指定关注
    $(".becomeFan").click(function () {
        var star_id = $(this).next("input").val();
        var oper = $(this);
        console.log(star_id);
        $.ajax({
            url: "/becomeFan",
            type: "get",
            data: "star_id=" + star_id,
            dataType: "json",
            success: function (data) {
                if (data.num == 1) {
                    oper.html("已关注");
                } else if (data.num == 2) {
                    alert("你已经关注了该用户!")
                } else {
                    alert("关注失败！请稍后重试");
                }
            }
        });
    });
});