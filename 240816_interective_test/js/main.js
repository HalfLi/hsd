$(document).ready(function(){
  let boost_top
  let life_top
  let hanwha_top
  let nature_top
  let paper_top
  let window_h
  let scrolling
  let life_w
  let nature_h2

  function scroll_chk(){
    window_h = $(window).height() //브라우저 높이
    scrolling = $(window).scrollTop() //스크롤 된 값
    boost_top = $('.boost').offset().top //해당 선택자의 전역좌표위치
    life_top = $('.life').offset().top
    hanwha_top = $('.hanwha').offset().top
    nature_top = $('.nature').offset().top
    paper_top = $('.paper').offset().top
    // console.log( window_h , scrolling , boost_top )

    if(scrolling > (boost_top - window_h + window_h/4)){
      $('.boost').addClass('active')
    }
    if(scrolling > (life_top - window_h + window_h/2)){
      life_w = (scrolling - (life_top - window_h))*1.2 + 200
      //넓이가 브라우저 넓이를 초과하지 않게
      if(life_w > $(window).width()){
        life_w > $(window).width()
        $('.life').addClass('end')
      }
      // console.log(life_w)
      $('.life .photo_wrap .photo').width(life_w)
    }
    if(scrolling > (hanwha_top - window_h + window_h/8)){
      $('body').addClass('black_bg')
    }else{
      $('body').removeClass('black_bg')
    }
    if(scrolling > (hanwha_top - window_h + window_h/4)){
      $('.hanwha').addClass('active')
    }
    if(scrolling > (nature_top - window_h + window_h/6)){
      $('.nature').addClass('active')
      nature_h2 = (scrolling - (nature_top - window_h))*0.1
      console.log(nature_h2)
      $('.nature h2').css('transform', 'translateY(-'+nature_h2+'%)')
      // transform: translateY(0);
      // .nature h2
    }
    if(scrolling > (paper_top - window_h + window_h/4)){
      $('.paper').addClass('active')
    }
  }
  scroll_chk() // 브라우저 로딩할때 한번...
  $(window).scroll(function(){ //브라우저가 스크롤 될때마다..
    scroll_chk()
  })
  $(window).resize(function(){ //브라우저가 리사이즈 될때마다..
    scroll_chk()
  })
})