$(document).on('change', '.file-input', function () {
    var filesCount = $(this)[0].files.length;

    var textbox = $(this).prev();

    if (filesCount === 1) {
        var fileName = $(this).val().split('\\').pop();
        textbox.text(fileName);
    } else {
        textbox.text(filesCount + ' files selected');
    }
});


function submitForm() {
    // var fileInput = document.querySelector('.file-input');
    // var files = fileInput.files;
    var files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        document.getElementById('upload-message').innerText = 'Please upload file';
    } else {
        // Proceed with file upload or other actions
        document.getElementById('upload-message').innerText = '';

        $('#loadingModal').modal('show');

        var formData = new FormData();

        for (var i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response);

                $('#loadingModal').modal('hide');

                var image1 = document.getElementById('img1');
                image1.src = response.file1

                var image2 = document.getElementById('img2');
                image2.src = response.file2

                document.getElementById('form_input').style.display = 'none';
                document.getElementById('form_result').style.display = 'block';

                // alert('Files uploaded successfully');
            } else {
                alert('Error uploading files');
            }
        };
        xhr.send(formData);


    }


}

function tryAgain() {

    // document.getElementById('form_input').reset();
    document.getElementById('form_input').style.display = '';
    document.getElementById('form_result').style.display = 'none';
}