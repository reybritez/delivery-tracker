/* Copyright (c) 2016 THE ULTRASOFT (http://theultrasoft.com)
 * Licensed under the MIT License (LICENSE.txt).
 *
 * Project: Parallaxie
 * Version: 0.5
 *
 * Requires: jQuery 1.9+
 */
(function(a){a.fn.parallaxie=function(c){c=a.extend({speed:0.2,repeat:"no-repeat",size:"cover",pos_x:"center",offset:0,},c);this.each(function(){var d=a(this);var f=d.data("parallaxie");if(typeof f!=="object"){f={}}f=a.extend({},c,f);var e=d.data("image");if(typeof e==="undefined"){e=d.css("background-image");if(!e){return}var g=f.offset+(d.offset().top-a(window).scrollTop())*(1-f.speed);d.css({"background-image":e,"background-size":f.size,"background-repeat":f.repeat,"background-attachment":"fixed","background-position":f.pos_x+" "+g+"px",});b(d,f);a(window).scroll(function(){b(d,f)})}});return this};function b(c,d){var e=d.offset+(c.offset().top-a(window).scrollTop())*(1-d.speed);c.data("pos_y",e);c.css("background-position",d.pos_x+" "+e+"px")}}(jQuery));