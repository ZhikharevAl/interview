// Create geometric background shapes
function createGeometricShapes() {
    const bg = document.querySelector('.geometric-bg');
    const shapes = ['circle', 'square', 'triangle'];
    const colors = ['var(--red)', 'var(--blue)', 'var(--yellow)', 'var(--black)'];

    for (let i = 0; i < CONFIG.geometricShapesCount; i++) {
        const shape = document.createElement('div');
        const shapeType = shapes[Math.floor(Math.random() * shapes.length)];
        shape.className = `geometric-shape ${shapeType}`;

        if (shapeType !== 'triangle') {
            shape.style.width = `${20 + Math.random() * 40}px`;
            shape.style.height = shape.style.width;
            shape.style.background = colors[Math.floor(Math.random() * colors.length)];
        }

        shape.style.left = `${Math.random() * 100}%`;
        shape.style.top = `${Math.random() * 100}vh`;
        shape.style.animationDelay = `${Math.random() * 20}s`;
        shape.style.animationDuration = `${20 + Math.random() * 20}s`;

        bg.appendChild(shape);
    }
}

// Format answer with code highlighting
function formatAnswer(text) {
    // Replace code blocks
    text = text.replace(/```([\s\S]*?)```/g, '<div class="code-block">$1</div>');
    // Replace inline code
    text = text.replace(/`([^`]+)`/g, '<span class="inline-code">$1</span>');
    // Replace line breaks
    text = text.replace(/\n/g, '<br>');
    // Bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    return text;
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, CONFIG.notificationDuration);
}

// Shuffle array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
