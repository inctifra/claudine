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

import Swiper from "swiper";
import {Navigation, Autoplay, Pagination} from "swiper/modules";


export function initSwiper(selector, options = {}) {
    const defaultConfig = {
        modules: [Navigation, Autoplay, Pagination],
        slidesPerView: 1,
        spaceBetween: 16,
        loop: false,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            640: { slidesPerView: 2 },
            768: { slidesPerView: 3 },
            1024: { slidesPerView: 4 },
        },
    };

    const config = { ...defaultConfig, ...options };

    const elements = document.querySelectorAll(selector);
    
    elements.forEach(el => {
        if (el.swiper) {
            el.swiper.destroy(true, true);
        }

        new Swiper(
            el,
            config);
    });
    return elements[0]?.swiper || null;
}