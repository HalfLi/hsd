$(document).ready(function(){ /* <-- 무조건 작성해야 함 */
    
    console.log('테스트')
    
    let scrolling = $(window).scrollTop() // scrolling은 $(window).scrollTop() 
    
    //문서가 로딩된 이후 단1번만 실행
    console.log(scrolling)

    /* 브라우저가 스크롤이 조금이라도 되면
    header에 fixed라는 클래스 추가,
    다시 맨 위로 올라가면 fixed라는 클래스 제거 */
    
    function scroll_chk(){ //함수를 선언
        scrolling = $(window).scrollTop() //scrolling이라는 변수에 현재 스크롤 된 값 저장
        if(scrolling > 0){ //스크롤 된 값이 0보다 크면
            $('header').addClass('fixed')
        }else{ //스크롤값이 0이면 (맨 위)
            $('header').removeClass('fixed')
        }
    } // function scroll_chk

    scroll_chk() // 함수 호출

    //브라우저 스크롤을 할때마다 실행
    $(window).scroll(function(){
        scroll_chk()
    })

    /*

    .tour .list ul li 한테
    오버한 li에만 active 클래스 추가
    이전에 active를 가지고 있었던 li에서는 active 제거
    ---무조건 하나의 li에만 active 존재 (마우스 오버한것)

    ---이전에 오버한 li는 알기 어려움
    --모든 li에 있는 active를 모두 삭제하고 
    오버한 요소에만 클래스 추가
    */

    $('.tour .list ul li').on('mouseenter',function(){
        //수많은 li중 지금 마우스 오버한 li 한개
        $('.tour .list ul li').removeClass('active')
        $(this).addClass('active')
    })

    /* 

    footer .family button.btn_open을 클릭하면
    footer .family에 open 클래스를 줘야함
    footer .family button.btn_close을 클릭하면
    footer .family에 open 클래스를 삭제해야함 

    */
    $('footer .family button.btn_open').on('click',function(){
        $('footer .family').addClass('open')
        $('footer .family .list').slideDown()
    })
    $('footer .family button.btn_close').on('click',function(){
        $('footer .family').removeClass('open')
        $('footer .family .list').slideUp()
    })

}) // $(document).ready(function