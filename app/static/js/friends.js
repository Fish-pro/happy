<!-- 展开按钮 -->
$(function (){
	$(".contentBottom>a").each(function (){
		$(this).click(function(){
			$(this).parent("div").prev("div").css("height","auto");
		});
	});
	$(".talk").each(function (){
		$(this).click(function(){
			$(this).parent("ul").parent(".contentBottom").next(".commit").css("display","block");
		});
	});
});