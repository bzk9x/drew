function applyClocNormalization() {
    const clockElement = document.getElementById('clock');
    if (clockElement) {
        clockElement.style.display = 'inline-block';
        clockElement.style.textAlign = 'center';
        clockElement.style.verticalAlign = 'baseline';
        clockElement.style.lineHeight = '1.2';
        clockElement.style.whiteSpace = 'nowrap';
    }
}

async function loadFonts() {
    try {
        const response = await fetch('../../fonts/fonts.json');
        const fonts = await response.json();
        
        const fontOptionsContainer = document.getElementById('font-options');
        
        fontOptionsContainer.innerHTML = '';
        
        fonts.forEach((font, index) => {
            const fontOption = document.createElement('div');
            fontOption.className = 'font-option';
            fontOption.setAttribute('data-font', font.name);
            
            const span = document.createElement('span');
            span.textContent = '07';
            
            span.style.fontFamily = `"${font.name}"`;
            span.style.display = 'inline-block';
            span.style.minWidth = '80px';
            span.style.minHeight = '60px'; 
            span.style.lineHeight = '1.2'; 
            span.style.textAlign = 'center';
            span.style.fontSize = '4em';
            span.style.verticalAlign = 'baseline';
            span.style.whiteSpace = 'nowrap';
            
            fontOption.appendChild(span);
            fontOptionsContainer.appendChild(fontOption);
            
            fontOption.addEventListener('click', function() {
                const clockElement = document.getElementById('clock');
                if (clockElement) {
                    clockElement.style.fontFamily = `"${font.name}"`;
                }
            });
        });
        applyClocNormalization();
        
        if (fonts.length > 0) {
            const clockElement = document.getElementById('clock');
            if (clockElement) {
                clockElement.style.fontFamily = `"${fonts[0].name}"`;
            }
        }
        
    } catch (error) {
        console.error('Error loading fonts:', error);
        
        const fontOptionsContainer = document.getElementById('font-options');
        fontOptionsContainer.innerHTML = '<div>Error loading fonts</div>';
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadFonts);
} else {
    loadFonts();
}