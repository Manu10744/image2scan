const fileInputElement = document.querySelector(".upload-container input[type='file']")
const uploadDragZone = document.querySelector(".upload-container .upload-dragzone")
const fileNameDisplay = document.querySelector(".upload-container .filename")

const uploadBtn = document.querySelector(".upload-container .upload-btn");
const resetBtn = document.querySelector(".upload-container .reset-btn");

const selectedFilesTable = document.querySelector(".selected-files-table");

uploadDragZone.addEventListener("dragenter", (e) => {
    e.preventDefault();

    if (e.target == uploadDragZone) {
        uploadDragZone.classList.remove("animated")
        uploadDragZone.classList.add("active")
    }
})

uploadDragZone.addEventListener("dragleave", (e) => {
    e.preventDefault();

    if (e.target == uploadDragZone) {
        uploadDragZone.classList.add("animated")
        uploadDragZone.classList.remove("active")
    }
})

uploadDragZone.addEventListener("dragover", (e) => {
    e.preventDefault()
})

uploadDragZone.addEventListener("drop", (e) => {
    e.preventDefault()

    files = e.dataTransfer.files
    if (files.length == 1) {
        fileNameDisplay.textContent = files[0].name
    } else {
        fileNameDisplay.textContent = "Multiple Files selected."
    }

    fileInputElement.files = e.dataTransfer.files
    updateSelectedFilesTable(files);
})

fileInputElement.addEventListener("change", (e) => {
    files = fileInputElement.files
    if (files.length == 1) {
        fileNameDisplay.textContent = files[0].name
    } else {
        fileNameDisplay.textContent = "Multiple Files selected."
    }

    updateSelectedFilesTable(files)
})

uploadBtn.addEventListener("click", () => {
    // TODO:
})

resetBtn.addEventListener("click", () => {
    fileNameDisplay.textContent = "No file uploaded, yet!"
    fileInputElement.value = null

    resetSelectedFilesTable();
})

function updateFileList(selectedFiles) {
    // TODO
}

function updateSelectedFilesTable(files) {
    resetSelectedFilesTable();

    fileList = [...files]
    fileList.forEach(file => {
        let newRow = document.createElement("tr")
        let fileNameField = document.createElement("td")
        let isUploadedField = document.createElement("td")

        fileNameField.textContent = file.name
        isUploadedField.textContent = "Yes"

        newRow.appendChild(fileNameField)
        newRow.appendChild(isUploadedField)
        
        selectedFilesTable.appendChild(newRow)
    })
}

function resetSelectedFilesTable() {
    let headingRow = selectedFilesTable.firstElementChild
    selectedFilesTable.innerHTML = ''
    selectedFilesTable.appendChild(headingRow)
}