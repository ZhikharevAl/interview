const Utils = {
    formatText(text) {
        if (!text) return '';
        const tempDiv = document.createElement('div');
        tempDiv.textContent = text;
        let sanitizedText = tempDiv.innerHTML;

        sanitizedText = sanitizedText
            .replace(/```([\s\S]*?)```/g, (match, code) => {
                const encodedCode = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                return `<pre class="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto my-4 border border-blue-500 border-opacity-30 font-mono">${encodedCode.trim()}</pre>`;
            })
            .replace(/`([^`]+)`/g, '<code class="bg-blue-900 bg-opacity-50 text-blue-300 font-mono text-sm px-2 py-1 rounded-md">$1</code>')
            .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-blue-300">$1</strong>')
            .replace(/\n/g, '<br>');

        return `<div class="prose max-w-none text-gray-300">${sanitizedText}</div>`;
    },
    shuffleArray(array) {
        return [...array].sort(() => Math.random() - 0.5);
    },
};
