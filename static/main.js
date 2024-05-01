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
        document.getElementById('upload-message').innerText = 'Please upload files';
    } else {
        // Proceed with file upload or other actions
        document.getElementById('upload-message').innerText = '';

        $('#loadingModal').modal('show');

        var formData = new FormData();

        for (var i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }
        formData.append('module', 'HDV');

        var input_sigma = document.getElementById("input_sigma").value;
        formData.append('sigma', input_sigma);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response);

                $('#loadingModal').modal('hide');

                if (response.status === true) {
                    // var image1 = document.getElementById('img1');
                    // image1.src = response.file1
                    //
                    // var image2 = document.getElementById('img2');
                    // image2.src = response.file2
                    //
                    // document.getElementById('form_input').style.display = 'none';
                    // document.getElementById('form_result').style.display = 'block';

                    // 指定要跳转的 URL
                    var targetURL = "/hyd_elec/" + response.version + '?step=2';
                    window.location.href = targetURL;
                } else {
                    alert(response.message);
                }
                // alert('Files uploaded successfully');
            } else {
                alert('Error uploading files');
            }
        };
        xhr.send(formData);
    }
}


function submitFormCV1() {
    // var fileInput = document.querySelector('.file-input');
    // var files = fileInput.files;
    var files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        document.getElementById('upload-message').innerText = 'Please upload files';
    } else {
        // Proceed with file upload or other actions
        document.getElementById('upload-message').innerText = '';

        $('#loadingModal').modal('show');

        var formData = new FormData();

        for (var i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }

        var input_sigma = document.getElementById("input_sigma").value;
        formData.append('module', 'CV');
        formData.append('sigma', input_sigma);
        formData.append('step', '1');

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response);

                $('#loadingModal').modal('hide');

                if (response.status === true) {
                    // var image1 = document.getElementById('form2_img1');
                    // image1.src = response.file1
                    //
                    // var image2 = document.getElementById('form2_img2');
                    // image2.src = response.file2
                    // var sigma = document.getElementById('form2_sigma');
                    // sigma.textContent = input_sigma
                    //
                    // var version = document.getElementById('version');
                    // version.value = response.version
                    //
                    //
                    // document.getElementById('form1').style.display = 'none';
                    // document.getElementById('form2').style.display = 'block';
                    // document.getElementById('form3').style.display = 'none';

                    // 指定要跳转的 URL
                    var targetURL = "/cv/" + response.version + '?step=2';
                    window.location.href = targetURL;
                } else {
                    alert(response.message);
                }
                // alert('Files uploaded successfully');
            } else {
                alert('Error uploading files');
            }
        };
        xhr.send(formData);
    }
}



function submitFormCV2() {
    var formData = new FormData();

    var input_sigma = document.getElementById("sigma").value;
    var form2_range1 = document.getElementById("form2_range1").value;
    var form2_range2 = document.getElementById("form2_range2").value;
    var version = document.getElementById("version").value;
    formData.append('module', 'CV');
    formData.append('step', '2');
    formData.append('sigma', input_sigma);
    formData.append('version', version);

    formData.append('peak_range_top', form2_range1);
    formData.append('peak_range_bottom', form2_range2);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);

            $('#loadingModal').modal('hide');

            if (response.status === true) {
                // var image1 = document.getElementById('form3_img1');
                // image1.src = response.img1
                //
                // var form3_link = document.getElementById('form3_link');
                // form3_link.href = response.file1
                //
                // document.getElementById('form1').style.display = 'none';
                // document.getElementById('form2').style.display = 'none';
                // document.getElementById('form3').style.display = 'block';
                var targetURL = "/cv/" + response.version + '?step=3';
                window.location.href = targetURL;
            } else {
                alert(response.message);
            }
            // alert('Files uploaded successfully');
        } else {
            alert('Error uploading files');
        }
    };
    xhr.send(formData);
}

function tryAgain() {

    // document.getElementById('form_input').reset();
    document.getElementById('form_input').style.display = '';
    document.getElementById('form_result').style.display = 'none';
}