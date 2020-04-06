const dropZone = document.getElementsByClassName("drop-zone")[0];
const dropMessage = document.getElementsByClassName("drop-message")[0];
const form = document.getElementById("image-form");

function dragOver(event) {
    if (event) {
        event.preventDefault();
    }

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
    let files;

    if (event.dataTransfer) {
        event.preventDefault();
        files = event.dataTransfer.files;
    } else {
        files = event;
        dragOver();
    }

    dropMessage.textContent = "Processing your image";
    dropZone.background = "transparent";

    toggleDynamicBackground(files.length);

    let images = new FormData();
    for (let i = 0; i < files.length; i++) {
        images.append("image_" + i, files[i]);
    }

    fetch("/", {
        method: "POST",
        body: images,
    })
        .then(res => res.json())
        .then(res => {
            toggleDynamicBackground();
            if (res["cropped"].length === 0) {
                dropZone.appendChild(createText("No faces detected 😢", "black"));
            } else {
                res["cropped"].forEach(crop => {
                    dropZone.appendChild(createImage(crop, 250, 312, 10));
                });
            }
        });
}

function triggerClickUpload() {
    document.getElementById("hidden-upload").click();
}

function clickUpload(event) {
    drop(event.target.files);
}

function disableDrop(event) {
    event.preventDefault();
}

function disableDrag(event) {
    event.preventDefault();
}

function toggleDynamicBackground(elements) {
    if (elements) {
        removeChildren(dropZone);
        const text = elements === 1 ? "Processing your image" : "Processing " + elements + " images";
        dropZone.appendChild(createSpinner());
        dropZone.appendChild(createText(text, "white"));
        dropZone.style.backgroundImage = "none";
    } else {
        removeChildren(dropZone);
        document.getElementById("download-btn").style.display = "block";
        dropMessage.textContent = "There you go!";
        dropZone.classList.remove("on-drag");
        dropZone.classList.remove('drop-zone-background');
    }
}

function createSpinner() {
    const spinner = document.createElement("div");
    spinner.classList.add("spinner");
    spinner.classList.add("dynamic");
    return spinner;
}

function createText(text, color) {
    const content = document.createElement("h4");
    content.textContent = text;
    content.style.color = color;

    const contentContainer = document.createElement("div");
    contentContainer.classList.add("processing-text-container");
    contentContainer.classList.add("dynamic");
    contentContainer.appendChild(content);

    return contentContainer;
}

function createImage(b64, width, height, margin) {
    const image = document.createElement("img");
    image.src = "data:image/png;base64," + b64;
    image.width = width;
    image.height = height;
    image.style.margin = margin;

    const a = document.createElement("a");
    a.href = image.src;
    a.classList.add("downloadable");
    a.download = "yuz_result.png";
    a.appendChild(image);

    return a;
}

function downloadAll() {
    const images = document.querySelectorAll(".downloadable");
    repeatableDownload(images, 0, 0);
}

function repeatableDownload(images, i, timeout) {
    setTimeout(() => {
        if (i < images.length) {
            images[i].click();
            repeatableDownload(images, ++i, 750);
        }
    }, timeout);
}

function removeChildren(container) {
    while (container.hasChildNodes()) {
        container.removeChild(container.childNodes[0]);
    }
}