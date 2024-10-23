
// now only support system-mode
document.addEventListener('DOMContentLoaded', () => {
	const isDarkMode = localStorage.getItem('dark-mode') === 'true';
	if (isDarkMode) {
		document.body.classList.add('dark-mode');
	}
	var element = document.getElementById("color_mode_button");
	if (isDarkMode) {
		element.innerHTML = "dark";
	}else{
		element.innerHTML = "light";
	}
	
	
});

function toggleDarkMode() {
	var element = document.getElementById("color_mode_button");
	if (element.innerHTML === "light"){
		element.innerHTML = "dark";
	}else{
		element.innerHTML = "light";
	}
	document.body.classList.toggle('dark-mode');
	localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode'));

}

window.onload = function() {
	const root = document.documentElement;
	const savedMaxWidth = localStorage.getItem('max-width-show');

	if (savedMaxWidth) {
		root.style.setProperty('--max-width-show', savedMaxWidth);
	}
};

// adjust max-width
function adjustMaxWidthAdd() {
	const root = document.documentElement;
	const currentMaxWidth = getComputedStyle(root).getPropertyValue('--max-width-show').trim();
	let newMaxWidth;

	if (currentMaxWidth === '400px') {
		newMaxWidth = '500px';
	} else if (currentMaxWidth === '500px') {
		newMaxWidth = '600px';
	} else if (currentMaxWidth === '600px') {
		newMaxWidth = '700px';
	} else if (currentMaxWidth === '700px') {
		newMaxWidth = '800px';
	} else if (currentMaxWidth === '800px') {
		newMaxWidth = '900px'
	} else if (currentMaxWidth === '900px') {
		newMaxWidth = '1000px'
	} else if (currentMaxWidth === '1000px') {
		newMaxWidth = '1100px'
	} else if (currentMaxWidth === '1100px') {
		newMaxWidth = '1200px'
	} else {
		newMaxWidth = '1200px'
	}

	root.style.setProperty('--max-width-show', newMaxWidth);
	localStorage.setItem('max-width-show', newMaxWidth);
}

function adjustMaxWidthSub() {
	const root = document.documentElement;
	const currentMaxWidth = getComputedStyle(root).getPropertyValue('--max-width-show').trim();
	let newMaxWidth;

	if (currentMaxWidth === '1200px') {
		newMaxWidth = '1100px';
	} else if (currentMaxWidth === '1100px') {
		newMaxWidth = '1000px';
	} else if (currentMaxWidth === '1000px') {
		newMaxWidth = '900px';
	} else if (currentMaxWidth === '900px') {
		newMaxWidth = '800px';
	} else if (currentMaxWidth === '800px') {
		newMaxWidth = '700px';
	} else if (currentMaxWidth === '700px') {
		newMaxWidth = '600px';
	} else if (currentMaxWidth === '600px') {
		newMaxWidth = '500px';
	} else if (currentMaxWidth === '500px') {
		newMaxWidth = '400px';
	} else {
		newMaxWidth = '400px';
	}

	root.style.setProperty('--max-width-show', newMaxWidth);
	localStorage.setItem('max-width-show', newMaxWidth);
}


document.getElementById('adjustWidth-add').onclick = adjustMaxWidthAdd;
document.getElementById('adjustWidth-sub').onclick = adjustMaxWidthSub;


// img
mediumZoom('[data-zoomable]', {
    margin: 24,
    background: 'rgba(0,0,0,0.9)',
    scrollOffset: 0,
});