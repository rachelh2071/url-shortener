document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("url-form");
    const longUrlInput = document.getElementById("long-url");
    const shortenButton = document.getElementById("shorten-button");
    const shortUrlElement = document.getElementById("short-url");
    const errorElement = document.getElementById("error-message");
    const errorText = document.getElementById("error-text");

    shortenButton.addEventListener("click", async () => {
        const longUrl = longUrlInput.value;
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ longUrl })
        });

        if (response.status === 200) {
            const data = await response.json();
            shortUrlElement.href = data.shortUrl;
            shortUrlElement.textContent = data.shortUrl;
            
            errorElement.classList.add("hidden");
        } else {
            const data = await response.json();
            errorText.textContent = data.error;
            errorElement.classList.remove("hidden");
        }
    });
});
