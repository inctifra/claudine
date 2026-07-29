// Copyright 2026 liont
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import $ from "jquery";
import Swiper from "swiper";
import { Navigation, Pagination, Autoplay, EffectFade } from "swiper/modules";
import "../../../sass/pages/home.scss";

function handleHeroSlider() {
  new Swiper(".bannerHeroSwiper", {
    modules: [Navigation, Pagination, Autoplay, EffectFade],
    loop: true,
    slidesPerView: 1,
    spaceBetween: 20,
    speed: 1000,
    autoplay: {
      delay: 3500,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },
    pagination: {
      el: ".bannerHeroSwiper .swiper-pagination",
      clickable: true,
    },
    breakpoints: {
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 3,
      },
    },
  });
}

function handleCategorySlider() {
  new Swiper(".categorySwiper", {
    modules: [Navigation, Autoplay, EffectFade],

    loop: true,

    speed: 900,

    spaceBetween: 30,

    autoplay: {
      delay: 3500,
      disableOnInteraction: false,
    },

    breakpoints: {
      0: {
        slidesPerView: 1,
      },

      576: {
        slidesPerView: 2,
      },

      992: {
        slidesPerView: 3,
      },

      1200: {
        slidesPerView: 4,
      },
    },
  });
}

function handleProductsSlider() {
  new Swiper(".productSwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      992: { slidesPerView: 4 },
      576: { slidesPerView: 2 },
      0: { slidesPerView: 1 },
    },
  });
}

function handleSellerSlider(){
  new Swiper(".sellerSwiper", {
        modules: [Navigation, Autoplay, EffectFade],

      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      grabCursor: true,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      pagination: {
        el: ".seller_pagination",
        clickable: true,
        dynamicBullets: true,
      },
       
        
      breakpoints: {
        576: {
          slidesPerView: 2,
          spaceBetween: 20,
        },
        768: {
          slidesPerView: 3,
          spaceBetween: 25,
        },

      },
    });
}

$(function () {
  handleHeroSlider();
  handleCategorySlider();
  handleProductsSlider();
  handleSellerSlider();
});
