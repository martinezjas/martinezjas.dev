(function() {
  // Constants
  const DEBOUNCE_DELAY_MS = 300; // Delay before triggering search
  const MIN_QUERY_LENGTH = 1; // Minimum characters to trigger search

  const numberInput = document.getElementById('numberInput');
  const dropdown = document.getElementById('autocompleteDropdown');
  const form = document.getElementById('himnarioForm');
  let debounceTimer;
  let selectedIndex = -1;
  let results = [];

  // Debounced search function
  function performSearch(query) {
    if (!query || query.length < MIN_QUERY_LENGTH) {
      hideDropdown();
      return;
    }

    fetch(`/api/search/autocomplete?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        results = data;
        displayResults(data);
      })
      .catch(error => {
        console.error('Search error:', error);
        hideDropdown();
      });
  }

  // Display autocomplete results
  function displayResults(data) {
    if (!data || data.length === 0) {
      hideDropdown();
      return;
    }

    dropdown.innerHTML = '';
    selectedIndex = -1;

    data.forEach((item, index) => {
      const div = document.createElement('div');
      div.className = 'autocomplete-item';
      div.innerHTML = `
        <div class="autocomplete-number">Himno ${item.number}</div>
        <div class="autocomplete-title">${item.title}</div>
      `;
      div.dataset.number = item.number;
      div.dataset.index = index;

      div.addEventListener('click', () => selectHymn(item.number));
      dropdown.appendChild(div);
    });

    dropdown.style.display = 'block';
  }

  // Hide dropdown
  function hideDropdown() {
    dropdown.style.display = 'none';
    selectedIndex = -1;
  }

  // Select hymn and set value
  function selectHymn(number) {
    numberInput.value = number;
    hideDropdown();
  }

  // Keyboard navigation
  function handleKeydown(e) {
    const items = dropdown.querySelectorAll('.autocomplete-item');

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (selectedIndex < items.length - 1) {
        selectedIndex++;
        updateSelection(items);
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (selectedIndex > 0) {
        selectedIndex--;
        updateSelection(items);
      }
    } else if (e.key === 'Enter') {
      if (selectedIndex >= 0 && items[selectedIndex]) {
        e.preventDefault();
        const number = items[selectedIndex].dataset.number;
        selectHymn(number);
      }
    } else if (e.key === 'Escape') {
      hideDropdown();
    }
  }

  // Update visual selection
  function updateSelection(items) {
    items.forEach((item, index) => {
      if (index === selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  // Event listeners
  numberInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      performSearch(e.target.value);
    }, DEBOUNCE_DELAY_MS);
  });

  numberInput.addEventListener('keydown', handleKeydown);

  // Click outside to close
  document.addEventListener('click', (e) => {
    if (!numberInput.contains(e.target) && !dropdown.contains(e.target)) {
      hideDropdown();
    }
  });
})();
