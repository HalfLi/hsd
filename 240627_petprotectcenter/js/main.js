$(document).ready(function(){
    const visul_swiper = new Swiper('.visual .swiper', { /* 팝업을 감싼는 요소의 class명 */

		autoplay: {  /* 팝업 자동 실행 */
			delay: 3000,
			disableOnInteraction: true,
		},
		loop: true,  /* 마지막 팝업에서 첫번째 팝업으로 자연스럽게 넘기기 */
		navigation: {  /* 이전, 다음 버튼 */
			nextEl: '.visual .btn_next',  /* 다음 버튼의 클래스명 */
			prevEl: '.visual .btn_prev',  
		},

	});
	
	
	/* .btn_play 버튼을 누르면 숨김처리하고 .btn_start가 나타나고
	 .btn_start을 누르면 숨김처리하고 .btn_play는 사라짐*/
	 $('.visual .btn_wrap button.btn_start').on("click", function(){
		visul_swiper.autoplay.stop();  /* 일시정지 기능 */
		$(this).hide();
		$('.visual .btn_wrap button.btn_play').show();
	 }); //btn_start
	 $('.visual .btn_wrap button.btn_play').on("click", function(){
		visul_swiper.autoplay.start();  /* 재생 기능 */
		$(this).hide();
		$('.visual .btn_wrap button.btn_start').show();
	 }) //btn_play

	 /*
	 	페이지가 스크롤되면 header에 fixed클래스 추가,맨 위로 올라가면 fixed클래스 제거
	 */

	let scrolling

	function scroll_chk(){
		scrolling = $(window).scrollTop()
		console.log(scrolling)
		if(scrolling > 0){
			$('header').addClass('fixed')
		}else{
			$('header').removeClass('fixed')
		}
	}//function

	scroll_chk() //문서가 처음 로딩되었을때 1번 실행

	$(window).scroll(function(){
		scroll_chk() //브라우저를 스크롤 할때마다
	})//window
})//$(document).ready
