const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

document.getElementById('copyText').addEventListener('click', function() {
    navigator.clipboard.writeText(this.innerText)
        .then(() => {
            // Change the tooltip text to show success message
            $(this).attr('data-original-title', 'Text copied!')
                   .tooltip('show');

            // Restore the original tooltip text after 2 seconds
            setTimeout(() => {
                $(this).attr('data-original-title', 'Click to copy');
            }, 2000);
        })
        .catch(err => {
            console.error('Erro ao copiar o texto: ', err);
        });
});

$(document).ready(function () {
    $('#modalMessage').modal('show');
});

