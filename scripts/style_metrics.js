console.log('Style Metric Script loaded');

function styleMetrics() {
    // console.log('styleMetrics function called');
    const root = window.parent.document.documentElement;
    const computedStyle = getComputedStyle(root);
    const expectedColor = computedStyle.getPropertyValue('--expected-colour').trim();
    const unexpectedColor = computedStyle.getPropertyValue('--unexpected-colour').trim();

    // Try to access parent window metrics
    const parentMetrics = window.parent.document.getElementsByClassName('stMetric');
    console.log('Found metrics in parent:', parentMetrics.length);

    Array.from(parentMetrics).forEach((metric, index) => {
        // Find the label text
        const label = metric.querySelector('[data-testid="stMarkdownContainer"] p');
        // Metric styling
        if (label) {
            const text = label.textContent;
            // console.log(label.textContent)
            if (text.includes('Expected Patterns')) {
                // console.log('Applying Expected Patterns styling');
                metric.style.backgroundColor = expectedColor;
                metric.style.padding = '10px';
                metric.style.borderRadius = '5px';
            } else if (text.includes('Unexpected Patterns')) {
                // console.log('Applying Unexpected Patterns styling');
                metric.style.backgroundColor = unexpectedColor;
                metric.style.padding = '10px';
                metric.style.borderRadius = '5px';
            } else if (text.includes('Total People')) {
                // console.log('Applying Unexpected Patterns styling');
                metric.style.padding = '10px';
                metric.style.borderRadius = '5px';
            }
            else {
                // console.log('Clear styling to avoid previous style cache')
                metric.style.backgroundColor = '';
                metric.style.padding = '';
                metric.style.borderRadius = '';
            }
        } else {
            console.log('No label found for this metric');
        }
    });
}

// Run immediately and after a delay
styleMetrics();

setTimeout(() => {
    // console.log('Running delayed styling');
    styleMetrics();
}, 1000);

// Set up observer on parent document
const observer = new MutationObserver((mutations) => {
    // console.log('Mutation observed');
    styleMetrics();
});

observer.observe(window.parent.document.body, {
    childList: true,
    subtree: true
});