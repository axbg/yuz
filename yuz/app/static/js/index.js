const dropZone = document.getElementsByClassName("drop-zone")[0];
const dropMessage = document.getElementsByClassName("drop-message")[0];
const form = document.getElementById("image-form");
const photoInput = document.getElementById("id_photo");

function dragOver(event) {
    event.preventDefault();
    if (!dropZone.classList.contains("on-drag")) {
        dropZone.classList.add("on-drag");
        dropMessage.textContent = "Yes, yes, there";
    }
}

function dragLeave(event) {
    event.preventDefault();
    dropZone.classList.remove("on-drag");
    dropMessage.textContent = "Drop your photo in the box";
}

function drop(event) {
    event.preventDefault();
    dropZone.classList.remove("on-drag");
    dropMessage.textContent = "Processing your image";
    const file = event.dataTransfer.files[0];
    base64encoder(file)
        .then(result => {
            const trimmedResult = result.split(",")[1];
            fetch("/", {
                method: "POST",
                body: JSON.stringify({ original: trimmedResult })
            })
                .then(res => res.json())
                .then(res => {
                    res["cropped"].forEach(crop => {

                        console.log(crop);
                    })
                    dropMessage.textContent = "??? profit";
                })
        })
        .catch(() => {
            console.log("Error happened when encoding");
        })
}

function disableDrop(event) {
    event.preventDefault();
}

function disableDrag(event) {
    event.preventDefault();
}

function base64encoder(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            resolve(reader.result);
        };
        reader.onerror = () => {
            reject();
        };
    });
};