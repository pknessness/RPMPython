
const ctx = document.getElementById('graph_canvas');

const data = {
  datasets: [{
    label: 'Gravity',
    data: [],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};

const config = {
  type: 'line',
  data: data,
  responsive: true,
  maintainAspectRatio: false,
  options: {
        scales: {
            y: {
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, ticks) {
                        return `${value}G`;
                    }
                }
            },
            x: {
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, ticks) {
                        return `${value}ms`;
                    }
                }
            }
        }
    }
};

var myChart = new Chart(ctx, config);

function updateChart(){
	var textIn = document.getElementById("input_profile");
	var lines = textIn.value.replaceAll(" ","").split("\n");
	myChart.data.datasets[0].data = []
	for(var i = 0; i < lines.length; i ++){
		console.log(`lines ${lines[i]}`);
		var split = lines[i].split(",");
		console.log(split);
		if(!split[0].endsWith("MS") | !split[1].endsWith("G")) break;
		var ms = split[0].split("MS")[0];
		var g = split[1].split("G")[0];
		myChart.data.datasets[0].data.push({x: ms, y: g});
	}
	myChart.update()
}

console.log(myChart);
updateChart();
