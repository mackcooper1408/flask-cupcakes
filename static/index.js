const BASE_URL = "http://localhost:5000/api/cupcakes"

const $body = $("body");

const $cupcakeList = $("#cupcake-list");

const $formSubmit = $("form").on("submit", cupcakeSubmitForm);

const $deleteCupcake = $cupcakeList.on("click", "li", deleteCupcake);

async function getCupcakeList() {
    const resp = await axios({
        url: BASE_URL,
        method: "GET"
    })
    list = resp.data.cupcakes;

    return list;
}

async function addCupcakesToDOM() {
    
    let list = await getCupcakeList();

    $cupcakeList.empty();

    for (cake of list) {
        $cupcakeList.append($(`<li class="list-group-item cupcakes" id="${cake.id}">${cake.flavor}</li>`));
    }
}


async function cupcakeSubmitForm(evt) {
        evt.preventDefault();
        let flavor = $("#cupcake-flavor").val()
        let size = $("#cupcake-size").val()
        let rating = $("#cupcake-rating").val()
        let image = $("#img-url").val()

        let response = await axios({
            url: BASE_URL,
            method: "POST",
            data: {
                "flavor": flavor,
                "size": size,
                "rating": rating,
                "image": image
            }
        })

        let newCupcake = response.data.cupcake
        // console.log(response)
        showNewCupcake(newCupcake);
        evt.target.reset()
}

function showNewCupcake(newCupcake) {
    $cupcakeList.append($(`<li class="list-group-item" id="${newCupcake.id}">${newCupcake.flavor}</li>`));
}

async function deleteCupcake(evt) {
    let cupcakeId = this.id;

    let response = await axios({
        url: `${BASE_URL}/${cupcakeId}`,
        method: "DELETE"
    })

    addCupcakesToDOM();
}

addCupcakesToDOM();