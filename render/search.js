document.addEventListener('DOMContentLoaded', (event) => {
    const searchModal = document.getElementById('searchModal');
    const searchInput = document.getElementById('searchInput');
    const recentSearches = document.querySelector('.recent-searches');
    const scoreThresholdInput = document.getElementById('scoreThreshold');
    const scoreValueDisplay = document.getElementById('scoreValue'); // 获取显示分数的元素
    let scoreThreshold = 10; // 默认阈值设为 100

    // 更新滑动条上方的显示值
    scoreValueDisplay.textContent = scoreThreshold;

    if (!searchModal || !searchInput || !recentSearches || !scoreThresholdInput) {
        console.error('Search modal elements not found');
        return;
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'k' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            openSearchModal();
        } else if (event.key === 'Escape') {
            closeSearchModal();
        }
    });

    function openSearchModal() {
        searchModal.style.display = 'flex';
        searchInput.focus();
    }

    function closeSearchModal() {
        searchModal.style.display = 'none';
    }

    searchModal.addEventListener('click', (event) => {
        if (event.target === searchModal) {
            closeSearchModal();
        }
    });

    searchInput.addEventListener('input', debounce(performSearch, 300));

    // 当滑动条变化时，更新阈值和显示的值
    scoreThresholdInput.addEventListener('input', () => {
        scoreThreshold = parseInt(scoreThresholdInput.value);
        scoreValueDisplay.textContent = scoreThreshold; // 更新显示的分数值
        performSearch(); // 重新执行搜索
    });

    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();
        if (query.length < 2) {
            recentSearches.innerHTML = 'No recent searches';
            return;
        }

        const queryWords = query.split(/\s+/);
    
        const scoredResults = blogData.map(blog => {
            let score = 0;
            queryWords.forEach(word => {
                if (blog.title.toLowerCase().includes(word)) score += 20;
                if (blog.category.toLowerCase().includes(word)) score += 10;
                blog.keywords.forEach(keyword => {
                    if (keyword.toLowerCase().includes(word)) score += 1;
                });
            });
            return { ...blog, score };
        }).filter(blog => blog.score >= scoreThreshold)
          .sort((a, b) => b.score - a.score);
    
        displayResults(scoredResults);
    }

    function displayResults(results) {
        if (results.length === 0) {
            recentSearches.innerHTML = 'No results found';
            return;
        }

        const resultsHTML = results.map(blog => `
            <div class="search-result">
                <div class="search-result-content">
                    <a href="${blog.url}" class="${blog.type}">${blog.title}</a>
                    <span>(${blog.date}, ${blog.type}${blog.author ? ', @' + blog.author : ''})</span>
                    ${blog.note ? `<a href="${blog.note}" class="html">note</a>` : ''}
                </div>
                <div class="search-result-score">score: ${blog.score}</div>
            </div>
        `).join('');

        recentSearches.innerHTML = resultsHTML;
    }

    function debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    console.log('Advanced search modal script loaded');
});

