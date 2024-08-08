$(document).ready(function(){
    /*
        1.Tab 클릭시 해당 li에 active 클래스 추가, 다른 li 클래스 삭제
            .cts_history .tab_area .tab_btn ul li
        2.클릭한 li만 [aria-selected=true] 나머지는 [aria-selected=false]
        3.클릭한 li에 aria-controls 값을 가져와"panel_00" 하단 콘텐츠중 같은 네이밍의 id "panel_00"
          에만 active 클래스 추가
          .cts_history .tab_area .tap_contents div[role="tabpanel"]
          find를 이용해 id가 aria-controls값과 같은 요소를 찾아야함.
          하지만 find는 하위요소만 검색 가능하기에 그 부모요소를 이용해야함
    */
   let tab_btn = $('.cts_history .tab_area .tab_btn ul li')
   //tab_btn은 $('.cts_history .tab_area .tab_btn ul li')
   let tab_name
   let tab_cnt = $('.cts_history .tab_area .tap_contents div[role="tabpanel"]')
   let tab_cnt_parent = $('.cts_history .tab_area .tap_contents')


   tab_btn.on('click',function(){
        tab_btn.removeClass('active')
        $(this).addClass('active')
        tab_btn.attr('aria-selected','false')
        $(this).attr('aria-selected','true')
        tab_name = $(this).attr('aria-controls')
        tab_name = '#' + tab_name // id선택자 (#)를 추가로 삽입
        tab_cnt.removeClass('active')
        tab_cnt_parent.find(tab_name).addClass('active')
   })
})