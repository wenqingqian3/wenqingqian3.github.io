document.addEventListener('DOMContentLoaded', (event) => {
    const searchModal = document.getElementById('searchModal');
    const searchInput = document.getElementById('searchInput');
    const recentSearches = document.querySelector('.recent-searches');
    const scoreThresholdInput = document.getElementById('scoreThreshold');
    const scoreValueDisplay = document.getElementById('scoreValue');
    let scoreThreshold = 10;

    updateMediaQuery();
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

    
    scoreThresholdInput.addEventListener('input', () => {
        scoreThreshold = parseInt(scoreThresholdInput.value);
        scoreValueDisplay.textContent = scoreThreshold; 
        performSearch();
    });

    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();
        if (query.length < 2) {
            recentSearches.innerHTML = 'No recent searches';
            return;
        }
        console.log(query)
        const ALLWords = parseQuery(query)

        queryWords = ALLWords.regularWords
        mandatoryWords = ALLWords.mandatoryWords
        console.log("qwords: ", queryWords)
        console.log("mwords: ", mandatoryWords)
    
        const scoredResults = blogData.map(blog => {
            let score = 0;
            if (queryWords && Array.isArray(queryWords)){
                queryWords.forEach(word => {
                    if (blog.title.toLowerCase().includes(word)) score += 20;
                    if (blog.category.toLowerCase().includes(word)) score += 10;
                    blog.keywords.forEach(keyword => {
                        if (keyword.toLowerCase().includes(word)) score += 1 * blog.scale;
                    });
                });
            }

            _is_title_manda = true
            _is_categ_manda = true
            _is_contn_manda = true

            if (mandatoryWords && Array.isArray(mandatoryWords)){
                if(mandatoryWords.length > 0){
                    _is_title_manda = false
                    _is_categ_manda = false
                    _is_contn_manda = false
                }
                mandatoryWords.forEach(word => {
                    if (blog.title.toLowerCase().includes(word)) {
                        score += 20;
                        _is_title_manda = true
                    }
                    if (blog.category.toLowerCase().includes(word)){
                        score += 10;
                        _is_categ_manda = true
                    }
                    blog.keywords.forEach(keyword => {
                        if (keyword.toLowerCase().includes(word)){
                            score += 1 * blog.scale;
                            _is_contn_manda = true
                        }
                    });
                });
            }
            if (_is_categ_manda === false && _is_title_manda === false && _is_contn_manda === false){
                score = -1
            }

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

    function parseQuery(query) {
        const mandatoryWords = [];
        const regularWords = [];
        let inQuotes = false;
        let QuotesClosed = false;
        let currentWord = '';

        for (let i = 0; i < query.length; i++) {
            if(query[i] === ' '){
                if(QuotesClosed === true){
                    mandatoryWords.push(currentWord.toLowerCase());
                    QuotesClosed = false;
                    inQuotes = false;
                    currentWord = '';
                }
                if(inQuotes){
                    currentWord += ' ';
                }else{
                    if(currentWord){
                        regularWords.push(currentWord.toLowerCase());
                    }
                    currentWord = '';
                }
            }
            else if(query[i] === "'"){
                if(inQuotes){
                    QuotesClosed = true;
                }else{
                    QuotesClosed = false;
                    if(currentWord === ''){
                        inQuotes = true;
                    }else{
                        currentWord += "'";
                    }
                }
            }
            else{
                if(QuotesClosed) currentWord += "'"
                currentWord += query[i];
                QuotesClosed = false;
            }
        }

        if(currentWord){
            if(QuotesClosed){
                mandatoryWords.push(currentWord.toLowerCase());
            }else{
                regularWords.push(currentWord.toLowerCase());
            }
        }

        return { mandatoryWords, regularWords };
    }
    console.log('Advanced search modal script loaded');
});

