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
    var fileInput = document.querySelector('.file-input');
    var files = fileInput.files;
    var must_upload = false
    if (files.length === 0 && must_upload === true) {
        document.getElementById('upload-message').innerText = 'Please upload file';
    } else {
        // Proceed with file upload or other actions
        document.getElementById('upload-message').innerText = '';

        $('#loadingModal').modal('show'); // 显示 Bootstrap 消息框

        // 随机暂停2至3秒后，消息框消失
        var delay = Math.floor(Math.random() * (3000 - 2000 + 1)) + 2000; // 生成2至3秒之间的随机延迟时间
        setTimeout(function () {
            $('#loadingModal').modal('hide'); // 隐藏 Bootstrap 消息框

            document.getElementById('form_input').style.display = 'none';
            document.getElementById('form_result').style.display = 'block';
        }, delay);
    }


}
function tryAgain() {

    // document.getElementById('form_input').reset();
    document.getElementById('form_input').style.display = '';
    document.getElementById('form_result').style.display = 'none';
}