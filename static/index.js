const BASE_URL = "http://localhost:5000/api/cupcakes";

const $body = $("body");

const $cupcakeList = $("#cupcake-list");

const $formSubmit = $("#cupcake-form").on("submit", cupcakeSubmitForm);

const $deleteCupcake = $cupcakeList.on("click", "li", deleteCupcake);

const $searchCupcakes = $("#search").on("submit", cupcakeSearch);

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
  let flavor = $("#Flavor").val();
  let size = $("#Size").val();
  let rating = $("#Rating").val();
  let image = $("#Image").val();

  let response = await axios({
    url: BASE_URL,
    method: "POST",
    data: {
      flavor,
      size,
      rating,
      image
    }
  });

  addCupcakesToDOM();
  evt.target.reset();
}

async function cupcakeSearch(evt) {
  evt.preventDefault();

  let searchTerm = $("#search-term").val();
  let response = await axios({
    url: `${BASE_URL}/search`,
    method: "GET",
    params: {searchTerm}
  });

  list = response.data.cupcakes;

  $cupcakeList.empty();

  for (cake of list) {
    $cupcakeList.append($(`<li class="list-group-item cupcakes" id="${cake.id}">${cake.flavor}</li>`));
  }

  evt.target.reset();
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