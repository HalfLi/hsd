$(document).ready(function(){
	/*
		header .gnb .gnb_wrap ul.depth1>li>a에 마우스를 오버하면
		
		1.header에 menu_over 라는 class 추가
		2.over한 메뉴(this)의 li에 on class 추가
		--메뉴에서 mouseenter는 디테일하게 mouseleave는 header --
	*/
	$('header .gnb .gnb_wrap ul.depth1>li').on('mouseenter focusin',function(){
		$('header').addClass('menu_over');
		$('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
		$(this).addClass('on');
	})
	$('header').on('mouseleave',function(){
		$('header').removeClass('menu_over');
		$('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
	})
	/* depth1중 마지막 li(company)중 depth2(회사연혁)에서 포커스아웃 */
	$('header .gnb .gnb_wrap ul.depth1>li:last-child ul.depth2>li:last-child').on('focusout',function(){
		$('header').removeClass('menu_over');
		$('header .gnb .gnb_wrap ul.depth1>li').removeClass('on')
	})
})