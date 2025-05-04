async function getRecipe() {
    const ingredient = document.getElementById('ingredient').value;
    const response = await fetch('/generate-recipe', {  // Backend endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredient })
    });

    const data = await response.json();
    document.getElementById('recipe').innerText = data.recipe;  // Display recipe
}
