async function getRestaurantDetail(id) {
  const response = await fetch(`/restaurant/api/restaurants/${id}/`);
  return response.json();
}

async function refreshRestaurantDetail(id) {
  const restaurant = await getRestaurantDetail(id);
  const user_data = await fetch("/user/").then((response) => response.json());

  const restaurantMeta = document.getElementById("restaurant-meta");
  const restaurantFoods = document.getElementById("restaurant-foods");

  restaurantMeta.innerHTML = `
    <h1>${restaurant.name}</h1>
    <p>${restaurant.address}</p>
    <p>${restaurant.price_range}</p>
    <p>${restaurant.description}</p>
  `;

  const foods = restaurant.foods;

  if (foods.length === 0) {
    return;
  }

  let htmlString = "";
  foods.forEach((food) => {
    htmlString += `
      <div class="flex flex-row items-center justify-between bg-green-100 min-h-16 rounded-lg p-5 gap-3">
        ${
          user_data.role === "R"
            ? `
<div class="flex flex-row items-center justify-between gap-2"> 
          <a href="/restaurant/api/restaurants/${restaurant.id}/delete_food/${food.id}"
             class="bg-red-500 hover:bg-red-600 text-white rounded-lg p-2 transition duration-300 shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg"
                   class="h-6 w-6 sm:h-8 sm:w-8"
                   viewBox="0 0 20 20"
                   fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
          </a> 
          <a href="/restaurant/api/restaurants/${restaurant.id}/update_food/${food.id}"
             class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg p-2 transition duration-300 shadow-md">
            <svg xmlns="http://www.w3.org/2000/svg"
                 class="h-6 w-6 sm:h-8 sm:w-8"
                 viewBox="0 0 20 20"
                 fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>          
          </a>
        </div>

`
            : ""
        }
        <div class="flex flex-row items-center justify-between w-full gap-10">
          <div class="flex flex-col">
            <h3 class="font-medium">${food.name}</h3>
            <p class="text-gray-700 text-sm">${food.description}</p>
          </div>
          <p>${food.price}</p>
        </div>
        ${
          user_data.role === "C"
          ? `
          <div class="flex flex-row items-center justify-between gap-2"> 
            <a href="/order/api/add_food_to_cart/${food.id}/"
              class="bg-red-500 hover:bg-red-600 text-white rounded-lg p-2 transition duration-300 shadow-md">
              Add To Cart
            </a> 
          </div>
          `
          :""
        }
      </div>
    `;
  });

  restaurantFoods.innerHTML = htmlString;
}

const url = new URL(window.location.href);
const id = url.pathname.split("/")[2];

refreshRestaurantDetail(id);

const modal = document.getElementById("crudModal");
const modalContent = document.getElementById("crudModalContent");

function showModal() {
  const modal = document.getElementById("crudModal");
  const modalContent = document.getElementById("crudModalContent");

  modal.classList.remove("hidden");
  setTimeout(() => {
    modalContent.classList.remove("opacity-0", "scale-95");
    modalContent.classList.add("opacity-100", "scale-100");
  }, 50);
}

function hideModal() {
  const modal = document.getElementById("crudModal");
  const modalContent = document.getElementById("crudModalContent");

  modalContent.classList.remove("opacity-100", "scale-100");
  modalContent.classList.add("opacity-0", "scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
  }, 150);
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalBtn").addEventListener("click", hideModal);

async function createRestaurant() {
  const response = await fetch(
    `/restaurant/api/restaurants/${id}/create_food/`,
    {
      method: "POST",
      body: new FormData(document.querySelector("#createFoodForm")),
    },
  );

  if (response.ok) {
    document.getElementById("createFoodForm").reset();
    document.getElementById("formErrorMessage").classList.add("hidden");
    hideModal();
    refreshRestaurantDetail(id);
  } else {
    document.getElementById("formErrorMessage").classList.remove("hidden");
    document.getElementById("formErrorMessage").scrollIntoView({
      behavior: "smooth", // Optional, adds a smooth scroll effect
      block: "center", // Optional, aligns the element to the center of the view
      inline: "nearest", // Optional, aligns the element within the nearest scrolling container
    });
  }

  return false;
}

document.getElementById("createFoodForm").addEventListener("submit", (e) => {
  e.preventDefault();
  createRestaurant();
});
