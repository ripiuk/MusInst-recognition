document.getElementById("image_path").onchange = function () {
    file_name = document.getElementById("uploadFile").value
    file_name = file_name.replace(/^.*[\\\/]/, '')
    document.getElementById("display_path").innerHTML = file_name;
};

function CloseNotification(){
    getElementById('notification').style.display = 'none';
};