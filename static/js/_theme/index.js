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

import '../../sass/_theme/_main.scss';
import 'ionicons/css/ionicons.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import "./_core_theme";

import $ from "jquery";
import WOW from 'wowjs';

function handleCart(){
    // Cart toggle
$('#cartToggle').on('click', function(e) {
  e.preventDefault();
  $('#miniCart').toggle();
});

// Close cart when clicking outside
$(document).on('click', function(e) {
  var $cart = $('#miniCart');
  var $toggle = $('#cartToggle');
  if (!$cart.is(e.target) && $cart.has(e.target).length === 0 &&
      !$toggle.is(e.target) && $toggle.has(e.target).length === 0) {
    $cart.hide();
  }
});
}

$(function(){
handleCart();

  // WOW.WOW({
  //   boxClass: 'wow',
  //   animateClass: 'animated',
  //   offset: 0,
  //   mobile: true,
  //   live: true,
  //   scrollContainer: null,
  //   resetAnimation: true,
  // }).init();
})