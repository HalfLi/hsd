$(document).ready(function(){
    /*
        현재 pc모드인지 mobile 모드인지..
        1024 이하는 mobile 1025이상는 pc이고

        header .header_sub .gnb .gnb_wrap ul.depth1 > li 
        pc모드일때 메뉴에 마우스를 오버하면 
        1. header에 menu_over 클래스 추가
        2. 1차 메뉴 li에 over 클래스 추가

        브라우저의 스크롤을 조금만 내리면 header fixed 클래스 추가
        다시 맨 꼭데기로 이동하면 fixed 클래스 삭제
    */

    let scrolling 
    let scroll_top //header 고정 시작 값
    let window_w
    let mobile_size = 1024
    let pc_mobile

    function scroll_chk(){
        if(pc_mobile == 'pc'){
            scroll_top = 50
        }else{
            scroll_top = 0
        }
        scrolling = $(window).scrollTop()
        console.log(scrolling)
        if(scrolling > scroll_top){//0보다 크다면 - 조금이라도 스크롤
            $('header').addClass('fixed')
        }else{//0이거나 0보다 작을때
            $('header').removeClass('fixed')
        }
    }

    function resize_chk(){
        window_w = $(window).width()
        console.log(window_w)
        if(window_w > mobile_size){ //pc일때
            pc_mobile = 'pc'
        }else{ //mobile
            pc_mobile = 'mo'
        }
        console.log(pc_mobile)
    }
    resize_chk() // 문서가 로딩 되었을때 1번
    $(window).resize(function(){
        resize_chk()
    })

    scroll_chk() //로딩되었을때 1번 실행
    $(window).scroll(function(){ //스크롤할때마다 1번 실행
        scroll_chk()
    })


    $('header .header_sub .gnb .gnb_wrap ul.depth1 > li').on('mouseenter focusin', function(){
        if(pc_mobile == 'pc'){
            $('header').addClass('menu_over')
            $('header .header_sub .gnb .gnb_wrap ul.depth1 > li').removeClass('over')
            $(this).addClass('over')
        }
    })
    $('header').on('mouseleave', function(){
        $('header').removeClass('menu_over')
        $('header .header_sub .gnb .gnb_wrap ul.depth1 > li').removeClass('over')
    })
    $('header .header_sub .gnb .gnb_wrap ul.depth1 > li:last-child ul.depth2 > li:last-child').on('focusout', function(){
        $('header').removeClass('menu_over')
        $('header .header_sub .gnb .gnb_wrap ul.depth1 > li').removeClass('over')
    })


    /* 
        모바일 메뉴 
        header .header_sub .gnb .gnb_wrap .depth1 > li > a 를 클릭했을때

        1차 메뉴 a의 href값을 무력화 (즉, 클릭해도 해당 페이지로 이동 되지 않도록)
        li에 open클래스를 줘야함
        열려있는 메뉴를 클릭하면 닫히고, 닫힌 메뉴를 클릭하면 열림 
        (동시에 여러개의 메뉴가 열릴 수 있음)
    */
    $('header .header_sub .gnb .gnb_wrap .depth1 > li > a').on('click', function(e){
        if(pc_mobile == 'mo'){ //모바일에서만 작동
            e.preventDefault();		/* a 태그의 href를 작동 시키지 않음 */
            $(this).parent().toggleClass('open')
        }
    })

    $('header .header_sub .gnb .gnb_open').on('click', function(){
        $('header').addClass('menu_open')
        //하단 콘텐츠 스크롤 금지
        $("html, body").css({overflow : "hidden", height : $(window).height()}).bind("scroll touchmove mousewheel", function(e){e.preventDefault();e.stopPropagation();return false;},function(){passive:false});
    })
    $('header .header_sub .gnb .gnb_close').on('click', function(){
        $('header').removeClass('menu_open')
        //하단 콘텐츠 스크롤 금지 해제
        $("html, body").css({overflow : "visible", height : "auto"}).unbind('scroll touchmove mousewheel');
    })

    $('.quick .open').on('click', function(){
        $('.quick').addClass('open')
    })
    $('.quick .close').on('click', function(){
        $('.quick').removeClass('open')
    })

    $('.quick .top').on('click', function(){
        $('html, body').animate({
            scrollTop : 0
        }, 500)
    })

})//$(document).ready