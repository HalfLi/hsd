$(document).ready(function(){

	/* width가 1024px이하면 모바일 이상이면 pc */
	let pc_mobile //현재상태가 PC인지Mobile인지를 저장하는 변수
	let window_w  //브라우저 넓이 저장

	function resize_chk(){
		window_w = $(window).width()
		if(window_w > 1024){ /* 현재 브라우저 넓이가 1024보다 크면 PC */
			pc_mobile = 'pc'
		}else{ /* 그 외는 모바일 */
			pc_mobile = 'mobile'
		}
		console.log(pc_mobile)
	}
	 //처음에 로딩 됐을때 실행
	resize_chk() 
	
	//브라우저가 리사이즈 될때마다 실행
	$(window).resize(function(){
		resize_chk()
	})

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

	/* 메뉴에 마우스를 올리면..
	   header에 menu_over라는 클래스 추가,마우스를 오버한 li에만 on이라는 클래스를 추가
	   메뉴 : header .gnb .gnb_wrap ul.depth1>li
	   -->다른 메뉴(li)에 마우스를 오버하면 이전에 오버했던 li에는 on클래스 삭제
	      모든 메뉴의 on class를 삭재했다가 오버한 this만 on 클래스 추가
	   -->header에서 마우스를 아웃하면 그때 header의 menu_over클래스 삭제
		  모든 메뉴에서 li의 on class 삭제   	  	  
	*/
	$('header .gnb .gnb_wrap ul.depth1>li').on('mouseenter',function(){
		if(pc_mobile == 'pc'){ //pc일 경우에만
			$('header').addClass('menu_over')
			$('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
			$(this).addClass('on')//마우스를 오버한 해당
		}//if		
	})//on
	$('header').on('mouseleave',function(){ //선택자에 마우스를 오버 후에 아웃 했을때
		if(pc_mobile == 'pc'){	
			$('header').removeClass('menu_over')
			$('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
		}//if
	})
	
	$('header .gnb .gnb_open').on('click',function(){
		if(pc_mobile == 'mobile'){
			$('header').addClass('mobile_open')
		}
	})

	$('header .gnb .gnb_close').on('click',function(){
		if(pc_mobile == 'mobile'){
			$('header').removeClass('mobile_open')
		}
	})
	
	//find~ swiper//

	const find01_swiper = new Swiper('.find .tap .find01 .swiper', { /* 팝업을 감싼는 요소의 class명 */
		slidesPerView: 'auto', /* 한번에 보일 팝업의 수 - 모바일 제일 작은 사이즈일때 */
		spaceBetween: 16, /* 팝업과 팝업 사이 여백 */
		breakpoints: {
			768: {    /* 768px 이상일때 적용 */
				slidesPerView: 4,
				spaceBetween: 24,
			},
		},
		
		loop: true,  /* 마지막 팝업에서 첫번째 팝업으로 자연스럽게 넘기기 */
		navigation: {
			nextEl: '.find .tap .find01 .btn_wrap .next',
			prevEl: '.find .tap .find01 .btn_wrap .prev',
		},
	}); //find01_swiper

	const find02_swiper = new Swiper('.find .tap .find02 .swiper', { /* 팝업을 감싼는 요소의 class명 */
		slidesPerView: 'auto', /* 한번에 보일 팝업의 수 - 모바일 제일 작은 사이즈일때 */
		spaceBetween: 16, /* 팝업과 팝업 사이 여백 */
		breakpoints: {
			768: {    /* 768px 이상일때 적용 */
				slidesPerView: 4,
				spaceBetween: 24,
			},
			// 1024: {   /* 1024px 이상일때 적용 */
			// 	slidesPerView: 4,
			// 	spaceBetween: 24,
			// },
		},
		
		loop: true,  /* 마지막 팝업에서 첫번째 팝업으로 자연스럽게 넘기기 */
		navigation: {
			nextEl: '.find .tap .find02 .btn_wrap .next',
			prevEl: '.find .tap .find02 .btn_wrap .prev',
		},
	}); //find02_swiper
	
	/*
		find의 탭메뉴
		.find .tap>ul>li를 클릭하면
		클릭한 li에만 on클래스를 줌
		.. 원래 html에 기본적으로 하나의 li에 on클래스가 있어야함
			제이쿼리에서 클릭하면 on을 다른 li에게 주는것뿐
	*/

	$('.find .tap>ul>li').on('click',function(){
		$('.find .tap>ul>li').removeClass('on')//모든 li에 있는 on클래스를 모두 지웠다가
		$(this).addClass('on') //click한 li에만 다시 on 클래스를 줌
	})

	//family swiper
	const family_swiper = new Swiper('.family .swiper', { /* 팝업을 감싼는 요소의 class명 */
		slidesPerView: 'auto', /* li의 넓이 비율로 안함 - css에서 준 넓이대로 함 */
		spaceBetween: 17, /* li와 li사이 - 제일 작은 여백 */
		breakpoints: {
			768: {  
				slidesPerView: 'auto',
				spaceBetween: 24,
			},
		},
		centeredSlides: true, /* 팝업을 화면에 가운데 정렬(가운데 1번이 옴) */
		loop: true,  /* 마지막 팝업에서 첫번째 팝업으로 자연스럽게 넘기기 */
		navigation: {
			nextEl: '.family .btn_wrap .next',
			prevEl: '.family .btn_wrap .prev',
		},
	}); //family swiper

	/*footer faily_site 열고 닫기
	footer .family_site button.open을 클릭하면 family_site에 on클래스 추가
	footer .family_site button.close를 클릭하면 family_site에 on클래스 삭제
	*/

	$('footer .family_site button.open').on('click',function(){
		$('footer .family_site').addClass('on')
	})
	$('footer .family_site button.close').on('click',function(){
		$('footer .family_site').removeClass('on')
	})
	
})//$(document).ready
