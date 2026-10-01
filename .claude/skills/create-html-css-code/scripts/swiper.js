// 슬라이드 정지/재생 버튼 토글 기능
const handlePauseAndResume = (pauseBtn, playBtn, swiper) => {
  if (!pauseBtn || !playBtn || !swiper) return;

  playBtn.addEventListener('click', (e) => {
    e.preventDefault();
    // 재생 동작
    swiper.autoplay.start(); // Autoplay 재개
    playBtn.classList.remove('active');
    pauseBtn.classList.add('active');
  });

  pauseBtn.addEventListener('click', (e) => {
    e.preventDefault();
    // 정지 동작
    swiper.autoplay.stop(); // Autoplay 정지
    pauseBtn.classList.remove('active');
    playBtn.classList.add('active');
  });
};

const $slide_wrapper = $('.wrap_slide_') // 샘플 셀렉터 — 실제 마크업의 래퍼 클래스(ex. .wrap_slide_visual)로 바꾼다
if ($slide_wrapper.length) {
  $slide_wrapper.each(function (idx) {
    const areaSlide = this
    const slide = areaSlide.querySelector('.swiper')
    const prevEl = areaSlide.querySelector('.btn_prev')
    const nextEl = areaSlide.querySelector('.btn_next')
    const pause = areaSlide.querySelector('.btn_pause')
    const play = areaSlide.querySelector('.btn_play')
    const slideName = slide.getAttribute('data-swiper-name') || 'ㅇㅇㅇ 슬라이드'
  
    const swiperOptions = {
      a11y: {
        containerMessage: slideName, // 슬라이드 컨테이너의 제목(기본값 null)
        prevSlideMessage: '이전 슬라이드',
        nextSlideMessage: '다음 슬라이드',
        slideLabelMessage: '현재 슬라이드 : {{index}} / 전체 슬라이드 : {{slidesLength}}',
        paginationBulletMessage: '{{index}}번째 슬라이드로 이동',
      },
      on: {
        lock: swiper => swiper.el.classList.add('inactive'),
        unlock: swiper => swiper.el.classList.remove('inactive'),
        transitionStart: (swiper) => { // 다음이든 이전이든 슬라이드가 넘어가지 않아도 트렌지션이 시작되면 발생함
        },
        transitionEnd: (swiper) => { // 다음이든 이전이든 슬라이드가 넘어가지 않아도 트렌지션이 끝나면 발생함
        },
        slideChangeTransitionStart: (swiper) => { // 다음이든 이전이든 슬라이드가 넘어가게 되어 트렌지션이 시작했을 때 발생함
        },
        slideChangeTransitionEnd: (swiper) => { // 다음이든 이전이든 슬라이드가 넘어가게 되어 트렌지션이 끝났을 때 발생함
        },
        autoplayTimeLeft: (s, time, progress) => { // auto 플레이할 때 프로그래스바 사용시
          const num = Number((progress*100).toFixed(0))
          // HTMLElement.style.transform = `translateX(-${num}%`
        },
      },
      // observeParents: true,
      // observeSlideChildren: true,
      // observer: true,
      loop: true,
      // effect: 'fade',
      // fadeEffect: {
      //   crossFade: true
      // },
      autoplay: {
        delay: 1000, // autoplay 간격
        pauseOnMouseEnter: true, // 자동재생시 마우스 올리면 정지 (기본값 false)
      },
      navigation: { prevEl, nextEl },
      pagination: {
        el: areaSlide.querySelector('.paging_slide'),
        clickable: true, // 기본 페이징 클릭할 수 있게 설정 (기본값 false)
        
        // 기본 동그란 원형 블릿
        type: 'bullets',
        renderBullet: function (index, className) {
          return `<span class="${className}" title="${index + 1}번 슬라이드로 이동"></span>`;
        }
  
        // 1 / 6 과 같은 숫자 페이지네이션
        // type: 'custom',
        // renderCustom: function (swiper, current, total) {
        //   const currentPage = current < 10 ? `0${current}` : current
        //   const totalPage = total < 10 ? `0${total}` : total
        //   return `<span class="blind">현재 슬라이드 번호 : </span><em class="num_current">${currentPage}</em>
        //           <span class="bar">/</span>
        //           <span class="blind">총 슬라이드 : </span><em class="num_total">${totalPage}</em>`;
        // }
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 30,
        },
      },
      centerInsufficientSlides: true, // slidesPerView 보다 슬라이드가 적어질 때만 센터 정렬
      slidesPerView: 1, // 화면에 슬라이드를 몇개 노출 시킬 것인지 기본값 1 ('auto'는 .swiper-slide 요소의 css 너비를 선언해서 제어)
      spaceBetween: 20, // 슬라이드간 간격 너비(px)
    }
  
    const swiper = new Swiper(slide, swiperOptions)
  
    handlePauseAndResume(pause, play, swiper)
  })
}