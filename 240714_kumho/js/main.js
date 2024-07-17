$(document).ready(function(){
    const visual_swiper = new Swiper('.visual .swiper', { /* 팝업을 감싼는 요소의 class명 */

        //effect: "fade", /* fade 효과 */

        autoplay: {  /* 팝업 자동 실행 */
            delay: 5000,
            disableOnInteraction: true,
        },

        loop: true,  /* 마지막 팝업에서 첫번째 팝업으로 자연스럽게 넘기기 */

        pagination: {  /* 몇개의 팝업이 있는지 보여주는 동그라미 */
            el: '.visual .paging', /* 해당 요소의 class명 */
            clickable: true,  /* 클릭하면 해당 팝업으로 이동할 것인지 값 */
            
        },
        

        navigation: {  /* 이전, 다음 버튼 */
            nextEl: '.visual .btn_next',  /* 다음 버튼의 클래스명 */
            prevEl: '.visual .btn_prev',  
        },

    });
    visual_swiper.autoplay.stop();  /* 일시정지 기능 */
    visual_swiper.autoplay.start();  /* 재생 기능 */

    /*

    btn_stop(.visual .btn_wrap button.btn_stop)버튼을 누르면
    1.팝업 일시정지
    2.일시정지 버튼은 숨겨짐, 재생버튼 나타남
    btn_play(.visual .btn_wrap button.btn_play)버튼을 누르면
    1.팝업 재생
    2.재생버튼은 숨겨짐, 일시정지버튼 나타남
    
    */
    $('.visual .btn_wrap button.btn_stop').on('click',function(){
        visual_swiper.autoplay.stop();
        $(this).hide()
        $('.visual .btn_wrap button.btn_play').show()
    })
    $('.visual .btn_wrap button.btn_play').on('click',function(){
        visual_swiper.autoplay.start();
        $(this).hide()
        $('.visual .btn_wrap button.btn_stop').show()
    })
    /*
        (PC)
        .biz .list ul li 에 마우스를 올리면
        올린 li에는 "on" class 추가,올리지 않은 li에는 "off"클래스 추가
    */
    $('.biz .list ul li').on('mouseenter',function(){
        if($(window).width() > 881){ // width 881px보다 클때만 적용
        $('.biz .list ul li').addClass('off')
        $('.biz .list ul li').removeClass('on')
        $(this).removeClass('off')
        $(this).addClass('on')
        }
    })
    $('.biz .list').on('mouseleave',function(){
        $('.biz .list ul li').removeClass('on')
        $('.biz .list ul li').addClass('off')
    })

})//document.ready
