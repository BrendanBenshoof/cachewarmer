$(document).ready(function() {
	init();
	//$('.bg_canvas').css('display', 'none');
});

var rad = 250;	//minimal radius
var trad = 550;	//maximal radius
var pts = [];	//points array
var c;			//canvas
var $$;			//context

var cww = window.innerWidth;
var cwh = window.innerHeight;

var offsetX = cww / 2;	//x offset
var offsetY = cwh / 2;	//y offset
var max = 65;			//max object parts

function init() {
	c = document.getElementById('bg_canvas');
	//c.height = window.innerHeight;

	$$ = c.getContext('2d');
	var angle = 0;
	var speed = 0;
	var dist = 0;
	for (var i = 0; i < 120; ++i) {
		angle = Math.random() * Math.PI * 2;
		speed = Math.random() * 2;
		dist = Math.random() * rad;
		pts.push({
			x:Math.sin(angle) * dist,
			y:Math.cos(angle) * dist,
			incx:Math.sin(angle) * speed,
			incy:Math.cos(angle) * speed,
			speed:speed
		});
	}
	draw();
}

function In() {
	trad = 160;
}

function Out() {
	trad = 300;
}

function draw() {
	rad += (trad - rad) * .01;

	var i = 0;
	var j = 0;
	var l = pts.length;
	var part = null;
	var part2 = null;
	var dx = 0;
	var dy = 0;
	//canvasWidth = window.innerWidth;
	//canvasHeight = window.innerHeight;
	
	var canvasWidth = 1920;
	var canvasHeight = 1080;

	$$.fillStyle = "rgba(255, 255, 255, 1)";
	$$.fillRect(0, 0, canvasHeight * 2, canvasWidth * 3);
	$$.strokeStyle = 'rgba(15, 91, 214, 1)';

	for (i = 0; i < l; ++i) {
		part = pts[i];
		for (j = i + 1; j < l; ++j) {
			part2 = pts[j];
			dx = part.x - part2.x;
			dy = part.y - part2.y;
			var dif = Math.sqrt(dx * dx + dy * dy);
			if (dif < max) {
				$$.lineWidth = (max - dif) * 0.05;
				$$.beginPath();
				$$.moveTo(offsetX + part.x * 2, offsetY + part.y * 2);
				$$.lineTo(offsetX + part2.x * 2, offsetY + part2.y * 2);
				$$.stroke();
			}
		}

		// move current obj
		part.x += part.incx;
		part.y += part.incy;

		var ptDist = Math.sqrt((part.x * part.x) + (part.y * part.y))
		if (ptDist > rad) {
			var mp = ( 1 / ptDist ) * 100;
			part.x = -part.x * mp;
			part.y = -part.y * mp;
			part.incx = (Math.random() - 0.5) * part.speed;
			part.incy = (Math.random() - 0.5) * part.speed;
		}
	}
	requestAnimFrame(draw);
}

window.requestAnimFrame = (function() {
	return	window.requestAnimationFrame ||
			window.webkitRequestAnimationFrame ||
			window.mozRequestAnimationFrame ||
			window.oRequestAnimationFrame ||
			window.msRequestAnimationFrame ||
	function(callback,  element) {
		window.setTimeout(callback, 2000 / 60);
	};
})();
