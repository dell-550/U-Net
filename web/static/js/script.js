document.getElementById('imageInput').addEventListener('change', handleImageUpload);

// 将类别和对应的颜色信息格式化显示
function displayClassInfo() {
    const params = document.getElementById('params');
    // params.innerHTML = '';  // 清空现有内容

}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // 显示原始图片
            const originalImage = document.getElementById('originalImage');
            originalImage.src = e.target.result;
            originalImage.style.display = 'block';

            // 发送图片到后台并获取返回图片
            uploadImageToBackend(file);
        };
        reader.readAsDataURL(file);
    }
}

function uploadImageToBackend(file) {
    // 这里你可以使用Fetch API或XMLHttpRequest上传图片到后台
    const formData = new FormData();
    formData.append('image', file);
    document.getElementById("file-name").textContent = file.name;
    document.getElementById("file-size").textContent = file.size;
    document.getElementById("format").textContent = file.type;
    // 假设后台接口为 /api/upload
    fetch('/upload', {
        method: 'POST',
        body: formData

    })
    .then(response => response.json())
    .then(data => {
        // 假设返回的图片链接在返回数据的 `image_url` 字段
        const returnedImage = document.getElementById('returnedImage');
        returnedImage.src = data.data.path;  // 使用后台返回的图片URL
        returnedImage.style.display = 'block';

        document.getElementById("model-name").textContent = data.data.model_name;
        document.getElementById("inference-time").textContent = data.data.times;
        document.getElementById("classes").textContent =data.data.deal_type;
        document.getElementById("segmented-size").textContent =data.data.image_size;
        document.getElementById("save-path").textContent =data.data.path;
        document.getElementById("model-path").textContent =data.data.model_path;
        // // 显示返回的参数
        // const params = document.getElementById('params');
        // params.textContent = JSON.stringify(data.data, null, 2);  // 假设返回的参数在 `params` 字段

    })
    .catch(error => {
        console.error('上传图片失败:', error);
    });
}


window.onload = function() {
    displayClassInfo();
};