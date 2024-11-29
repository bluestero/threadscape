// Function to adjust textarea height dynamically
function autoResizeTextarea(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
}

// Attach event listeners after DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    // Attach auto-resize listener to textareas with class 'message-box'
    document.querySelector('.message-box').addEventListener('input', autoResizeTextarea);

});
