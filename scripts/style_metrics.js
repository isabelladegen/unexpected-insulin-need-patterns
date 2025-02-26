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
        // Expected and Unexpected Metric styling
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
            } else if (text.includes('Some days')){
                metric.style.backgroundColor = hexToRgba('#7CBDDA', 0.5);
                metric.style.padding = '10px';
                metric.style.borderRadius = '5px';
                metric.style.border = '2px solid #7CBDDA';
            } else if (text.includes('Most days')){
                metric.style.backgroundColor = hexToRgba('#0A6C95', 0.5);
                metric.style.padding = '10px';
                metric.style.borderRadius = '5px';
                metric.style.border = '2px solid #0A6C95';
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

function hexToRgba(hex, alpha = 1) {
    // Remove the hash if it exists
    hex = hex.replace(/^#/, '');

    // Parse the hex values
    let r, g, b;

    // Check if it's a 3-digit hex
    if (hex.length === 3) {
        r = parseInt(hex[0] + hex[0], 16);
        g = parseInt(hex[1] + hex[1], 16);
        b = parseInt(hex[2] + hex[2], 16);
    }
    // Or a 6-digit hex
    else if (hex.length === 6) {
        r = parseInt(hex.substring(0, 2), 16);
        g = parseInt(hex.substring(2, 4), 16);
        b = parseInt(hex.substring(4, 6), 16);
    } else {
        throw new Error('Invalid hex color format');
    }

    // Return the rgba string
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
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