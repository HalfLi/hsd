$(document).ready(function(){
    /*
        PC,모바일 구분 필요 PC(880px이상) 모바일(880px이하)

        PC일때 menu에 마우스를 오버하면
        1)header에 menu_over클래스 추가
        2)depth1 li에 over클래스 추가 [header .header_sub .gnb ul.depth1>li]

        브라우저의 스크롤을 내리면 header에 fixed클래스 추가
        다시 최상단으로 스크롤하면 fixed클래스 삭제
    */
   let scrolling
   let window_w
   let mobile_size = 880
   let scroll_top //header fixed 시작 값
   let pc_mobile

   function scroll_chk(){
        if(pc_mobile == 'pc'){
            scroll_top = 50
        }else{
            scroll_top = 0
        }
        scrolling = $ (window).scrollTop()
        console.log(scrolling)
        if(scrolling > scroll_top){
            $('header').addClass('fixed')
        }else{ // 그 외의 경우..
            $('header').removeClass('fixed')
        }
   }
   function resize_chk(){
        window_w = $(window).width()
        console.log(window_w)
        if(window_w > mobile_size){
            pc_mobile = 'pc'
        }else{
            pc_mobile = 'mobile'
        }
        console.log(pc_mobile)
   }
    resize_chk() //해당 common을 로딩했을때 1번
    $(window).reszie(function(){
        resize_chk()
    })
    scroll_chk() // 해당 common을 로딩했을때 1번
    $(window).scroll(function(){ //스크롤할때마다 실행
        scroll_chk()
    })

    $('header .header_sub .gnb ul.depth1>li').on('mouseenter focusin',function(){
        if(pc_mobile == 'pc'){
            $('header').addClass('menu_over')
            $('header .header_sub .gnb ul.depth1>li').removeClass('over')
            $(this).addClass('over')
        }
    })
    $('header').on('mouseleave', function(){
        $('header').removeClass('menu_over')
        $('header .header_sub .gnb ul.depth1>li').removeClass('over')
    })
    $('header .header_sub .gnb ul.depth1>li:last-child ul.depth2>li:last-child').on('focusout',function(){
        $('header').removeClass('menu_over')
        $('header .header_sub .gnb ul.depth1>li').removeClass('over')
    })
})