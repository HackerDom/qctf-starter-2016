var WIDTH, HEIGHT;
var R = 80, SPEED = 0.75, ROTATE_SPEED = 0.3;
var INTERVAL_DELAY = 5, INTERVAL;
var nucl_url_list = [
    '/dna_checker/static/A.png',
    '/dna_checker/static/C.png',
    '/dna_checker/static/G.png',
    '/dna_checker/static/T.png'
];
var balls = []


function Ball(x, y, angle) {
    this.rotate_angle = 0;
    this.rotate_angle_speed = 0;
	this.x = x;
	this.y = y;
	this.dx = Math.cos(angle) * SPEED;
	this.dy = Math.sin(angle) * SPEED;
	this.htmlElem = document.createElement('div');
	this.htmlElem.className = 'ball';
    var nucl_idx = Math.floor(Math.random() * 4);
    var nucl_url = nucl_url_list[nucl_idx];
    this.htmlElem.style.setProperty('background', 'url(' + nucl_url + ')');
	this.refreshHtmlElem = function () {
		this.htmlElem.style.setProperty('left', (this.x - R) + 'px');
		this.htmlElem.style.setProperty('top', (this.y - R) + 'px');
        this.htmlElem.style.setProperty('transform', 'rotate(' + this.rotate_angle + 'deg)');
	};

	this.isCollide = function (other) {
		var d = Math.sqrt((this.x - other.x)*(this.x - other.x) +
					(this.y - other.y)*(this.y - other.y));
		if(d >= 2*R)
			return false;
		var r1 = len(this.x - other.x, this.y - other.y),
			r2 = len(this.x + this.dx - other.x - other.dx,
				this.y + this.dy - other.y - other.dy);
		return r2 < r1;
	};
}


function refreshSize() {
	WIDTH = window.innerWidth;
	HEIGHT = window.innerHeight;
}


function dot(x1, y1, x2, y2) {
	return x1*x2 + y1*y2;
}


function len(x1, y1) {
	return Math.sqrt(x1*x1 + y1*y1);
}


function proj(x1, y1, x2, y2) {
	var d = dot(x1, y1, x2, y2) / len(x2, y2),
		k = len(x2, y2);
	return {x: x2 / k * d, y: y2 / k * d};
}


function tick() {
	for(var i = 0; i < balls.length; i++) {
		for(var j = i + 1; j < balls.length; j++) {
			var a = balls[i],
				b = balls[j];
			if(!(a.x >= R && a.x <= WIDTH - R && a.y >= R && a.y <= HEIGHT - R))
				continue;
			if(!(b.x >= R && b.x <= WIDTH - R && b.y >= R && b.y <= HEIGHT - R))
				continue;
			if(a.isCollide(b)) {
				var coll_vec = {x: a.x - b.x, y: a.y - b.y},
					tan_vec = {x: -coll_vec.y, y: coll_vec.x},
					a_coll = proj(a.dx, a.dy, coll_vec.x, coll_vec.y),
					b_coll = proj(b.dx, b.dy, coll_vec.x, coll_vec.y),
					a_tan = proj(a.dx, a.dy, tan_vec.x, tan_vec.y),
					b_tan = proj(b.dx, b.dy, tan_vec.x, tan_vec.y);
				a.dx = a_tan.x + b_coll.x;
				a.dy = a_tan.y + b_coll.y;
				b.dx = b_tan.x + a_coll.x;
				b.dy = b_tan.y + a_coll.y;
                a.rotate_angle_speed = Math.random() * 2.0 * ROTATE_SPEED - ROTATE_SPEED;
                b.rotate_angle_speed = Math.random() * 2.0 * ROTATE_SPEED - ROTATE_SPEED;
			}
		}
	}
	for(var i = 0; i < balls.length; i++) {
		balls[i].x += balls[i].dx;
		balls[i].y += balls[i].dy;
		if(balls[i].x < R) {
			balls[i].dx = Math.abs(balls[i].dx);
			balls[i].x = R;
		}
		if(balls[i].x > WIDTH - R) {
			balls[i].dx = -Math.abs(balls[i].dx);
			balls[i].x = WIDTH - R;
		}
		if(balls[i].y < R) {
			balls[i].dy = Math.abs(balls[i].dy);
			balls[i].y = R;
		}
		if(balls[i].y > HEIGHT - R) {
			balls[i].dy = -Math.abs(balls[i].dy);
			balls[i].y = HEIGHT - R;
		}
        balls[i].rotate_angle += balls[i].rotate_angle_speed;
		balls[i].refreshHtmlElem();
	}
}


function addRandomBall() {
	var x, y, angle;
	x = R + Math.floor(Math.random() * (WIDTH - 2*R));
	y = R + Math.floor(Math.random() * (HEIGHT - 2*R));
	angle = Math.random() * 2.0 * Math.PI;
	var ball = new Ball(x, y, angle);
	balls.push(ball);
	document.body.appendChild(ball.htmlElem);
}


function removeAllBalls() {
	for(var i = 0; i < balls.length; i++) {
		balls[i].htmlElem.remove();
	}
	balls = [];
}


function init(n) {
	refreshSize();
	for(var i = 0; i < n; i++) {
		addRandomBall();
	}
	INTERVAL = setInterval(tick, INTERVAL_DELAY);
}
