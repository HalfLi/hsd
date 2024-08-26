(function( $ ){
    $.fn.counterUp = function( options ) {
        // 클래스가 "counter"인 모든 요소를 선택합니다.
        const $counters = $(this);
            
        // 노출 비율(%)과 애니메이션 속도(ms)을 설정합니다.
        const exposurePercentage = 100; // ex) 스크롤 했을 때 $counters 컨텐츠가 화면에 100% 노출되면 숫자가 올라갑니다.
        const duration = 1500; // ex) 1000 = 1초

        // 숫자에 쉼표를 추가할지 여부를 설정합니다.
        const addCommas = true; // ex) true = 1,000 / false = 1000
		
		$counters.each(function() {
			const $el = $(this);
			const start = parseInt($el.data("start"));
			const end = parseInt($el.data("end"));
			// 숫자를 업데이트하고 애니메이션을 시작합니다.
			updateCounter($el, start, end);
		})

        // 숫자를 업데이트하고 애니메이션하는 함수 정의
        function updateCounter($el, start, end) {
            let startTime;
            function animateCounter(timestamp) {
                if (!startTime) startTime = timestamp;
                const progress = (timestamp - startTime) / duration;
                const current = Math.round(start + progress * (end - start));
                const formattedNumber = addCommas ? current.toLocaleString() : current;
                $el.text(formattedNumber);
                
                if (progress < 1) {
                    requestAnimationFrame(animateCounter);
                } else {
                    $el.text(addCommas ? end.toLocaleString() : end);
                }
            }
            requestAnimationFrame(animateCounter);
        }
    }
})( jQuery );