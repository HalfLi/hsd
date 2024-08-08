$(document).ready(function(){
    $('.visual_popup .popup').slick({
        autoplay: false, //팝업 자동 실행
        autoplaySpeed: 5000, //팝업이 머무는 시간
        speed: 700, //팝업 전환 속도
        fade: true,  //페이드 효과 적용
        dots: true, //하단 페이지 버튼 (true, false)
        arrows: false,  //다음, 이전팝업 (true, false)
        //pauseOnHover: true, //마우스호버시 일시정지
        //infinite: false, //무한반복
    });
})//document.ready
