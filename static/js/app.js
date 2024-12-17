document.addEventListener("DOMContentLoaded", async () => {
    const resultsContainer = document.getElementById("results");
    const totalWatchedContainer = document.getElementById("total-watched");

    try {
        // Fetch dramas
        const dramasResponse = await fetch("/dramas/");
        if (!dramasResponse.ok) throw new Error("Failed to fetch dramas");

        const dramas = await dramasResponse.json();
        resultsContainer.innerHTML = "";

        dramas.forEach(drama => {
            const dramaElement = document.createElement("div");
            dramaElement.className = "drama-card";
            dramaElement.innerHTML = `
                <h3>${drama.name}</h3>
                <p><strong>Genre:</strong> ${drama.genre}</p>
                <p><strong>Country:</strong> ${drama.country}</p>
                <p><strong>Status:</strong> ${drama.status}</p>
                <p><strong>Streaming Platform:</strong> ${drama.streaming_platform}</p>
            `;
            resultsContainer.appendChild(dramaElement);
        });

        // Fetch total watched
        const totalResponse = await fetch("/dramas/total-watched");
        if (!totalResponse.ok) throw new Error("Failed to fetch total dramas");

        const { total } = await totalResponse.json();
        totalWatchedContainer.textContent = total;

    } catch (error) {
        resultsContainer.innerHTML = `Error: ${error.message}`;
        totalWatchedContainer.textContent = "Error";
    }
});
