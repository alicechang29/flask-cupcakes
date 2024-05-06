$cupcakeForm = document.querySelector('.cupcake-form')

/** Handle a cupcake form submission */
async function handleCupcakeForm(evt) {
    evt.preventDefault();
    cupcakes = await getCupcakes();
}

/** Fetch the data for all cupcakes */
async function getCupcakes() {
    resp = await fetch('/api/cupcakes');
    apiData = await resp.json();

    return apiData.cupcakes;
}

/** Populate the DOM with the cupcake data */

function start() {
    $cupcakeForm.addEventListener("submit", handleCupcakeForm);
}

export { start }