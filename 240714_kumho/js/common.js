/* header,footer 공통요소에 들어가는 jquery가 포함 */
$(document).ready(function(){
    /*
        header에 마우스 오버,
        브라우저 스크롤되면 header에 fixed 클래스 추가
        --> pc,mobile 상관없이 언제나 구현

        header .gnb .gnb_wrap ul.depth1>li 메뉴에 마우스를 오버시
        1.메뉴에 마우스를 올리면 header에 menu_over 클래스 추가
        2.마우스를 오버한 li에 on 클래스 추가
        --> pc에서만 구현
    */
   let window_w
   let pc_mobile
   let scrolling

   function resize_chk(){
    window_w = $(window).width()
    if(window_w >= 881){
        pc_mobile = 'pc'
    }else{
        pc_mobile = 'mobile'
    }
        console.log(pc_mobile)
    }//function resize_chk
    // 브라우저가 로딩 되었을때 단 한번 실행

    resize_chk()

    $(window).resize(function(){ //브라우저가 리사이징 될때마다 1번 실행
        resize_chk()
    })//(window).resize

    $('header').on('mouseenter',function(){
        $(this).addClass('fixed')
    })
    $('header').on('mouseleave',function(){
        if(scrolling <= 0){
            $(this).removeClass('fixed')
        } 
    })
    
    function scroll_chk(){
        scrolling = $(window).scrollTop()
        if(scrolling > 0){ // 스크롤이 조금이라도 되었다면
            $('header').addClass('fixed')
        }else{
            $('header').removeClass('fixed')
        }
        console.log(scrolling)
    }
    scroll_chk() // 브라우저가 로딩 되었을때 한번 실행

    $(window).scroll(function(){ // 스크롤 할때마다 scroll_chk를 실행
        scroll_chk()
    })

    $('header .gnb .gnb_wrap ul.depth1>li').on('mouseenter',function(){
        if(pc_mobile == 'pc'){
            $('header').addClass('menu_over')
            $('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
            $(this).addClass('on')
        }
    })
    $('header').on('mouseleave',function(){
        if(pc_mobile == 'pc'){
            $('header').removeClass('menu_over')
            $('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
        }
    })

    /*
        모바일 메뉴를 클릭하면
        1. a링크값 삭제 .... (이동을 못하게 막아야함)
        2. li에 open클래스 추가 (open클래스 있으면 삭제) --> 한번 클릭하면 열리고 두번 클릭하면 닫힘
    */
    
    $('header .gnb .gnb_wrap ul.depth1>li>a').on("click", function(e){
        if(pc_mobile == 'mobile'){
            e.preventDefault();		/* a 태그의 href를 작동 시키지 않음 */
            $(this).parent().toggleClass('open')
        }
    });

    /*
        메뉴열기를 클릭하면 header에 menu_open 클래스 추가
        메뉴닫기를 클릭하면 header에 menu_open 클래스 삭제  
        header .gnb .gnb_open (메뉴열기)
        header .gnb .gnb_close (메뉴닫기)
    */
    $('header .gnb .gnb_open').on('click',function(){
        $('header').addClass('menu_open')
        $("html, body").css({overflow : "hidden", height : $(window).height()}).bind("scroll touchmove mousewheel", function(e){e.preventDefault();e.stopPropagation();return false;},function(){passive:false});
    })
    $('header .gnb .gnb_close').on('click',function(){
        $('header').removeClass('menu_open')
        $("html, body").css({overflow : "visible", height : "auto"}).unbind('scroll touchmove mousewheel');
    })
})//document.ready