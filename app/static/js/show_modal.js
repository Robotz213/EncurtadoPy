$(document).ready(function () {
    $('#modalMessage').modal('show');
});

document.getElementById('copyText').addEventListener('click', function() {
    navigator.clipboard.writeText(this.innerText)
        .then(() => {
            alert('Texto copiado para a área de transferência!');
        })
        .catch(err => {
            console.error('Erro ao copiar o texto: ', err);
        });
});
