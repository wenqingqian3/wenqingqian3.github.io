
function updateMediaQuery() {
	const rootStyle = getComputedStyle(document.documentElement);
	const hiddenSidebar = parseInt(rootStyle.getPropertyValue('--hidden-sidebar'));
	const maxwidthshow = parseInt(rootStyle.getPropertyValue('--max-width-show'));

	// 根据当前 CSS 变量值更新媒体查询
	if (window.innerWidth - maxwidthshow < 4 * hiddenSidebar) {
	document.querySelector('.toc-container').style.display = 'none';
	} else {
	document.querySelector('.toc-container').style.display = 'block';
	}
}

// 监听窗口大小变化
window.addEventListener('resize', updateMediaQuery);
    const addButton = document.getElementById('adjustWidth-add');
    const subButton = document.getElementById('adjustWidth-sub');
    addButton.addEventListener('click', () => {
    updateMediaQuery();
});

// 按下减少宽度的按钮
subButton.addEventListener('click', () => {
	updateMediaQuery();
});




window.addEventListener('scroll', function() {
	const toch1 = document.querySelectorAll('h1');
	const toch2 = document.querySelectorAll('h2');
	const toch3 = document.querySelectorAll('h3');
	
	let currentH1Id = '';
	let currentH2Id = '';
	let currentH3Id = '';

	const scrollPosition = window.scrollY;
	const viewportHeight = window.innerHeight / 2;
	const buffer = 150;  // 增加一个缓冲区

	// 遍历 h1
	toch1.forEach(h1 => {
		const h1Top = h1.offsetTop;
		const h1Height = h1.offsetHeight;

		// 在可见范围内并加入缓冲区
		if (scrollPosition + viewportHeight >= h1Top - buffer && scrollPosition < h1Top + h1Height) {
		currentH1Id = h1.getAttribute('id');
		}
	});

	// 遍历 h2
	toch2.forEach(h2 => {
		const h2Top = h2.offsetTop;
		const h2Height = h2.offsetHeight;

		// 在可见范围内并加入缓冲区
		if (scrollPosition + viewportHeight >= h2Top - buffer && scrollPosition < h2Top + h2Height) {
		currentH2Id = h2.getAttribute('id');
		}
	});

	// 遍历 h3
	toch3.forEach(h3 => {
		const h3Top = h3.offsetTop;
		const h3Height = h3.offsetHeight;

		// 在可见范围内并加入缓冲区
		if (scrollPosition + viewportHeight >= h3Top - buffer && scrollPosition < h3Top + h3Height) {
		currentH3Id = h3.getAttribute('id');
		}
	});
	// 给当前所在 section 对应的 TOC 链接加上 active 类
	if (currentH1Id) {
		// 移除之前所有的高亮状态
		document.querySelectorAll('.toc-sidebar a').forEach(link => {
			link.classList.remove('active');
		});
		document.querySelector(`.toc-sidebar a[href="#${currentH1Id}"]`).classList.add('active');

		activeLink = document.querySelector(`.toc-sidebar a[href="#${currentH1Id}"]`);
		scrollToActiveLink(activeLink);
	}
	if (currentH2Id) {
		// 移除之前所有的高亮状态
		document.querySelectorAll('.toc-sidebar a').forEach(link => {
			link.classList.remove('active');
		});
		document.querySelector(`.toc-sidebar a[href="#${currentH2Id}"]`).classList.add('active');
		document.querySelector(`.toc-sidebar a[href="#${toch2map[currentH2Id].h1}"]`).classList.add('active');
		
		activeLink = document.querySelector(`.toc-sidebar a[href="#${currentH2Id}"]`);
		scrollToActiveLink(activeLink);
	}
	if (currentH3Id) {
		// 移除之前所有的高亮状态
		document.querySelectorAll('.toc-sidebar a').forEach(link => {
			link.classList.remove('active');
		});
		document.querySelector(`.toc-sidebar a[href="#${currentH3Id}"]`).classList.add('active');
		document.querySelector(`.toc-sidebar a[href="#${toch3map[currentH3Id].h2}"]`).classList.add('active');
		document.querySelector(`.toc-sidebar a[href="#${toch3map[currentH3Id].h1}"]`).classList.add('active');

		activeLink = document.querySelector(`.toc-sidebar a[href="#${currentH3Id}"]`);
		scrollToActiveLink(activeLink);
	}
});


// 滚动 TOC 容器到高亮的 TOC 项
function scrollToActiveLink(activeLink) {
	const tocContainer = document.querySelector('.toc-container');

	// 如果高亮链接不在可见范围内，则滚动
	const linkOffsetTop = activeLink.offsetTop;
	const containerHeight = tocContainer.offsetHeight;
	tocContainer.scrollTop = linkOffsetTop - containerHeight / 2 + activeLink.offsetHeight / 2;
}