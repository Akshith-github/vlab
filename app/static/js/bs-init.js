if(document.querySelectorAll('[data-bss-chart]')){document.addEventListener('DOMContentLoaded', function() {

	var charts = document.querySelectorAll('[data-bss-chart]');

	for (var chart of charts) {
		if(chart.chart){
		chart.chart = new Chart(chart, JSON.parse(chart.dataset.bssChart));}
	}
}, false);}