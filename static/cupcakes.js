const $cupcakeForm = document.querySelector('.cupcake-form');

/** Handle a cupcake form submission */
async function handleStart() {
    //evt.preventDefault();
    const cupcakes = await getCupcakes();
    displayCupcakes(cupcakes);
}

/** Fetch the data for all cupcakes */
async function getCupcakes() {
    const resp = await fetch('/api/cupcakes');
    const apiData = await resp.json();
    console.log(apiData);
    return apiData.cupcakes;
}

/** Populate the DOM with the cupcake data */

function displayCupcakes(cupcakes) {
    //for every cupcake in cupcakes list, create a li and add them all to $cupcakeList
    const $cupcakeList = document.querySelector('.cupcake-list');

    for (const cupcake in cupcakes) {
        const $cupcakeItem = document.createElement("li");
        console.log("cupcake", cupcake);
        $cupcakeItem.innerHTML = `
            ${cupcake.id},
            ${cupcake.flavor},
            ${cupcake.size},
            ${cupcake.rating}`;
        $cupcakeList.append($cupcakeItem);
    }
}

// function handleCupcakeForm() {

// }

function start() {
    handleStart();
    //$cupcakeForm.addEventListener("submit", handleCupcakeForm);
}

export { start };