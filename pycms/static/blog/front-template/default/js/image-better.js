$(document).ready(function(){
		$('article img').each(function() {
			var maxWidth = 700; // 图片最大宽度
			var ratio = 0;  // 缩放比例
			var width = $(this).width();    // 图片实际宽度
			var height = $(this).height();  // 图片实际高度
		 
			// 检查图片是否超宽
			if(width > maxWidth){
				ratio = maxWidth / width;   // 计算缩放比例
				$(this).css("width", maxWidth); // 设定实际显示宽度
				height = height * ratio;    // 计算等比例缩放后的高度 
				$(this).css("height", height);  // 设定等比例缩放后的高度
			}
		});
		$("article img").wrap('<a class="contentPhoto" rel="prettyPhoto"></a>');
		$("article a.contentPhoto img").each(function(){
			$(this).parent().attr('href',$(this).attr('src'));
		});
		//img box start
		$("a[rel^='prettyPhoto']").prettyPhoto(
			{
				allow_resize:true,
				social_tools:false
			}
		);
		//img box end
		$( "#navTabs" ).tabs();
		//执行代码高亮   
		SyntaxHighlighter.all();
});















/*function DrawImage(ImgD,iwidth,iheight){    
    //参数(图片,允许的宽度,允许的高度)    
    var image=new Image();    
    image.src=ImgD.src;    
    if(image.width>0 && image.height>0){    
      if(image.width/image.height>= iwidth/iheight){    
          if(image.width>iwidth){      
              ImgD.width=iwidth;    
              ImgD.height=(image.height*iwidth)/image.width;    
          }else{    
              ImgD.width=image.width;      
              ImgD.height=image.height;    
          }    
      }else{    
          if(image.height>iheight){      
              ImgD.height=iheight;    
              ImgD.width=(image.width*iheight)/image.height;            
          }else{    
              ImgD.width=image.width;      
              ImgD.height=image.height;    
          }    
      }    
    }    
} */
//JQuery style
/*$('article img').each(function() {
    var maxWidth = 700; // 图片最大宽度
    var ratio = 0;  // 缩放比例
    var width = $(this).width();    // 图片实际宽度
    var height = $(this).height();  // 图片实际高度
 
    // 检查图片是否超宽
    if(width > maxWidth){
        ratio = maxWidth / width;   // 计算缩放比例
        $(this).css("width", maxWidth); // 设定实际显示宽度
        height = height * ratio;    // 计算等比例缩放后的高度 
        $(this).css("height", height);  // 设定等比例缩放后的高度
    }
});*/
//javascript style
/*
$("article img").wrap('<a class="contentPhoto" rel="prettyPhoto"></a>')
	var len = $('article a.contentPhoto img').length
	for (var i=0;i<len;i++){
    $('article a.contentPhoto')[i].href = $('article a.contentPhoto img')[i].src
}
*/
//jQuery style
/*$("article img").wrap('<a class="contentPhoto" rel="prettyPhoto"></a>');
$("article a.contentPhoto img").each(function(){
    $(this).parent().attr('href',$(this).attr('src'));
    }
);*/

