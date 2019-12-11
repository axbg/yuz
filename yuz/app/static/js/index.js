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
};

function dragLeave(event) {
    event.preventDefault();
    dropZone.classList.remove("on-drag");
    dropMessage.textContent = "Drop your photo in the box";
};

function drop(event) {
    event.preventDefault();
    dropMessage.textContent = "Processing your image";
    const file = event.dataTransfer.files[0];

    base64encoder(file)
        .then(result => {
            const trimmedResult = result.split(",")[1];
            removeChildren(dropZone);
            dropZone.appendChild(createImage(trimmedResult, 250, 312, 10));
            fetch("/", {
                method: "POST",
                body: JSON.stringify({ original: trimmedResult }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(res => res.json())
                .then(res => {
                    removeChildren(dropZone);
                    res["cropped"].forEach(crop => {
                        dropZone.appendChild(createImage(crop, 250, 312, 10));
                    });

                    dropMessage.textContent = "There you go!";
                    dropZone.classList.remove("on-drag");
                    dropZone.classList.remove('drop-zone-background');
                });
        })
        .catch(() => {
            console.log("Error happened when encoding");
        })
};

function disableDrop(event) {
    event.preventDefault();
};

function disableDrag(event) {
    event.preventDefault();
};

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

function createImage(b64, width, height, margin) {
    const image = document.createElement("img");
    image.src = "data:image/png;base64," + b64;
    image.width = width;
    image.height = height;
    image.style.margin = margin;
    return image;
};

function removeChildren(container) {
    while (container.hasChildNodes()) {
        container.removeChild(container.childNodes[0]);
    }
};