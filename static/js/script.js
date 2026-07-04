document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const uploadArea = document.querySelector(".custom-file-upload");
    const uploadText = document.getElementById("uploadText");
    const imagePreviewContainer = document.getElementById("imagePreviewContainer");
    const imagePreview = document.getElementById("imagePreview");
    const fileNameDisplay = document.getElementById("fileNameDisplay");
    const predictBtn = document.getElementById("predictBtn");

    if (fileInput) {
        // Handle file selection
        fileInput.addEventListener("change", function (e) {
            handleFiles(this.files);
        });

        // Drag and drop events
        uploadArea.addEventListener("dragover", function (e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.add("dragover");
        });

        uploadArea.addEventListener("dragleave", function (e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.remove("dragover");
        });

        uploadArea.addEventListener("drop", function (e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.remove("dragover");
            
            let files = e.dataTransfer.files;
            fileInput.files = files; // Assign files to input
            handleFiles(files);
        });

        function handleFiles(files) {
            if (files && files[0]) {
                const file = files[0];
                const validExtensions = ["image/jpeg", "image/png", "image/jpg"];
                
                if (validExtensions.includes(file.type)) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        imagePreview.src = e.target.result;
                        fileNameDisplay.textContent = file.name;
                        
                        // Show preview, hide icon
                        uploadText.classList.add("d-none");
                        imagePreviewContainer.classList.remove("d-none");
                        
                        // Add glow effect on button
                        predictBtn.classList.add("shadow-lg");
                        predictBtn.classList.replace("btn-tea-green", "btn-tea-dark");
                    };
                    
                    reader.readAsDataURL(file);
                } else {
                    alert("Format file tidak didukung! Harap unggah PNG atau JPG/JPEG.");
                    fileInput.value = "";
                }
            }
        }
    }
});
