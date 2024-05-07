const $cupcakeForm = document.querySelector('.cupcake-form');
console.log($cupcakeForm);

/** Handle a cupcake form submission */
async function handleStart() {
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

    for (const cupcake of cupcakes) {
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

async function handleCupcakeForm(evt) {
    debugger;
    evt.preventDefault();
    const cupcake = parseFormData();
    await addCupcake(cupcake);
    location.reload();
}

$cupcakeForm.addEventListener("submit", handleCupcakeForm);

async function addCupcake(cupcake) {
    console.log("addCupcake");
    const resp = await fetch('/api/cupcakes', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(cupcake)
    }
    );
    const apiData = await resp.json();

    console.log({ apiData });

}

function parseFormData() {
    const flavor = document.querySelector('#flavor').value;
    const size = document.querySelector('#size').value;
    const rating = document.querySelector('#rating').value;
    const image_url = document.querySelector('#image_url').value;

    return { flavor, size, rating, image_url };
}

function start() {
    handleStart();
}

export { start };