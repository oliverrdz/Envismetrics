let filesArray = [];

function updateFileList() {
    const fileListDisplay = document.getElementById('file-list');
    const fileCountDisplay = document.getElementById('file-message');

    fileListDisplay.innerHTML = '';
    filesArray.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.innerHTML = `
        <button onclick="removeFile(${index})"> ❌ </button>
        <span>${file.name}</span>
      `;
        fileListDisplay.appendChild(div);
    });
    fileCountDisplay.textContent = filesArray.length + ' file(s) selected';
}

function removeFile(index) {
    filesArray.splice(index, 1);
    updateFileList();
}

function handleFiles(files) {
    for (let file of files) {
        const alreadyAdded = filesArray.some(f => f.name === file.name && f.size === file.size);
        if (!alreadyAdded) {
            filesArray.push(file);
        }
    }
    updateFileList();
}

$(document).on('change', '.file-input', function (e) {
    // handleFiles($(this)[0].files);
    handleFiles(e.target.files);
});

$(document).on('dragover', '.file-input', function () {
    const dropArea = document.getElementById('file-drop-area');
    dropArea.classList.add('highlight');
});

$(document).on('dragleave', '.file-input', function () {
    const dropArea = document.getElementById('file-drop-area');
    dropArea.classList.remove('highlight');
});

$(document).on('drop', '.file-input', function () {
    const dropArea = document.getElementById('file-drop-area');
    dropArea.classList.remove('highlight');
    handleFiles($(this)[0].files)
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
        var input_cycle = document.getElementById("input_cycle").value;
        formData.append('module', 'CV');
        formData.append('sigma', input_sigma);
        formData.append('cycle', input_cycle);
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


function tryAgain() {

    // document.getElementById('form_input').reset();
    document.getElementById('form_input').style.display = '';
    document.getElementById('form_result').style.display = 'none';
}

function goBack() {
    window.history.back();
}