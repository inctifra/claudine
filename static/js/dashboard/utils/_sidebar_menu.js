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

$.sidebarMenu = function (menu) {
  var animationSpeed = 300,
    subMenuSelector = '.sidebar-submenu';
  $(menu).on('click', 'li a', function (e) {
    var $this = $(this);
    var checkElement = $this.next();
    if (checkElement.is(subMenuSelector) && checkElement.is(':visible')) {
      checkElement.slideUp(animationSpeed, function () {
        checkElement.removeClass('menu-open');
      });
      checkElement.parent("li").removeClass("active");
    } else if ((checkElement.is(subMenuSelector)) && (!checkElement.is(':visible'))) {
      var parent = $this.parents('ul').first();
      var ul = parent.find('ul:visible').slideUp(animationSpeed);
      ul.removeClass('menu-open');
      var parent_li = $this.parent("li");
      checkElement.slideDown(animationSpeed, function () {
        checkElement.addClass('menu-open');
        parent.find('li.active').removeClass('active');
        parent_li.addClass('active');
      });
    }
    if (checkElement.is(subMenuSelector)) {
      e.preventDefault();
    }
  });
}
$.sidebarMenu($('.sidebar-menu'))
let $nav = $('.page-sidebar');
let $header = $('.page-main-header');
let $toggle_nav_top = $('.sidebar-toggle');
$toggle_nav_top.click(function () {
  let $this = $(this);
  $nav = $('.page-sidebar');
  $nav.toggleClass('open');
  $header.toggleClass('open');
  // $(".page-body-wrapper .page-sidebar").toggleClass("active")

});
let $body_part_side = $('.body-part');
$body_part_side.click(function () {
  $nav.addClass('open');
  $header.addClass('open');
});

$(".sidebar-back").click(function () {
  $(".page-sidebar").addClass("open");
});

//    responsive sidebar
var $window = $(window);
var widthwindow = $window.width();
$(function () {
  "use strict";
  if (widthwindow <= 991) {
    $toggle_nav_top.addClass("open");
    $nav.addClass("open");
  }
});
$(window).resize(function () {
  var widthwindaw = $window.width();
  if (widthwindaw + 17 <= 991) {
    $toggle_nav_top.addClass("open");
    $nav.addClass("open");
  } else {
    $toggle_nav_top.removeClass("open");
    $nav.removeClass("open");
  }
});

$(".sidebar-menu>li").removeClass("active");
$(".sidebar-menu").find("a").removeClass("active");
$(".sidebar-menu").find("li a").removeClass("active");

var current = window.location.pathname
$(".sidebar-menu>li a").filter(function () {

  // console.log(window.location.pathname);
  // console.log($(this).attr("href"));

  var link = $(this).attr("href");
  if (link) {
    if (current.indexOf(link) != -1) {
      $(this).parents('li a').addClass('active');
      $(this).addClass('active');
      // console.log(link + " found");
    }
  }
});

// add active when dropdown links are active
// $(".sidebar-menu li").each(function (index) {
//   if ($(this).hasClass("active")) {
//     $(this).find(".sidebar-header").addClass("active")
//   }
// });
