document.addEventListener('DOMContentLoaded', function () {

    // Getting the message-box.
    const messageBox = document.querySelector('.message-box');

    // Make it adjust the box heigh according to the input lines.
    messageBox.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
