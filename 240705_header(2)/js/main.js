$(document).ready(function(){
    /*
        1025이상 pc
        1024이하 mobile
    */
    let pc_mobile //현재 pc인지 mobile인지 상태를 저장하는 변수
    let window_w //브라우저의 넓이

    function resize_chk(){
        window_w = $(window).width()
        if(window_w > 1024){ //1025이상 - pc버전
            pc_mobile = 'pc'
        }else{
            pc_mobile = 'mobile'
        }//if
        console.log(pc_mobile)
    }//function

    resize_chk() //html이 로딩된 이후 단 1번 실행
    $(window).resize(function(){//브라우저가 리사이즈 될때마다
        resize_chk()
    })

    /* 
        pc에서 메뉴에 마우스를 오버하면 
        header에 menu_over 클래스 추가
        오버한 li에(header .gnb .gnb_wrap ul.depth1 > li)만 on클래스 추가
    */
    $('header .gnb .gnb_wrap ul.depth1 > li').on('mouseenter focusin', function(){
        /* pc일때만 작동되어야함
           on이라는 명령은 이벤트핸들러(감시)로 pc에서만 작동(감시)되게 못함
           무조건 작동(감시)됨 
           이벤트가 발생했을때 작동되는 실행문에 if문 걸어서 pc일때만 실행되도록 해야함  */
        if(pc_mobile == 'pc'){
            $('header').addClass('menu_over')
            $('header .gnb .gnb_wrap ul.depth1 > li').removeClass('on')
            $(this).addClass('on')
        }//if
    })//on
    $('header').on('mouseleave', function(){
        if(pc_mobile == 'pc'){
            $('header').removeClass('menu_over')
            $('header .gnb .gnb_wrap ul.depth1 > li').removeClass('on')
        }//if
    })//on
    $('header .gnb .gnb_wrap ul.depth1 > li:last-child > ul.depth2 > li:last-child').on('focusout', function(){
        /* 1차메뉴 li 중 마지막 li의 하위메뉴 li중 마지막 li  */
        if(pc_mobile == 'pc'){
            $('header').removeClass('menu_over')
            $('header .gnb .gnb_wrap ul.depth1 > li').removeClass('on')
        }//if
    })
})