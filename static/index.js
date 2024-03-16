const canvas = document.getElementById('graph_canvas');
const context = canvas.getContext('2d');

var nodes = [];


function draw() {
    context.clearRect(0, 0, window.innerWidth, window.innerHeight);
    for (let i = 0; i < nodes.length; i++) {
        let node = nodes[i];
        context.beginPath();
        context.fillStyle = node.fillStyle;
        context.arc(node.x, node.y, node.radius, 0, Math.PI * 2, true);
        context.strokeStyle = node.strokeStyle;
        context.fill();
        context.stroke();
    }
}

var selection = undefined;

function within(x, y) {
    return nodes.find(n => {
        return x > (n.x - n.radius) && 
            y > (n.y - n.radius) &&
            x < (n.x + n.radius) &&
            y < (n.y + n.radius);
    });
}

/** remove the onclick code and update move and up code */
function move(e) {
    if (selection) {
        selection.x = e.x;
        selection.y = e.y;
        selection.moving = true;
        draw();
    }
    console.log(selection.x);
}

function down(e) {
    let target = within(e.x, e.y);
    if (target) {
        selection = target;
    }
}

function up(e) {
    if (!selection || !selection.moving) {
        let node = {
            x: e.x,
            y: e.y,
            radius: 10,
            fillStyle: '#22cccc',
            strokeStyle: '#009999',
            selectedFill: '#88aaaa'
        };
        nodes.push(node);
        draw();
        console.log("pushed",node);
    }
    if (selection) {
        delete selection.moving;
        delete selection.selected;
    }
    selection = undefined;
    draw();
}

window.onmousemove = move;
window.onmousedown = down;
window.onmouseup = up;
