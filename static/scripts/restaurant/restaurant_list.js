async function getRestaurants(page) {
  const response = await fetch(`api/restaurants/?page=${page}&page_size=8`);
  return await response.json();
}

async function refreshRestaurants(page) {
  const restaurants = await getRestaurants(page);
  const restaurantList = document.getElementById("restaurant-list");
  let htmlString = "";
  if (restaurants.results.length === 0) {
    return;
  }
  restaurantList.className =
    "grid gap-6 sm:grid-cols-2 xl:grid-cols-4 p-3 md:p-10";
  restaurants.results.forEach((restaurant) => {
    htmlString += `<div class="relative group h-full">
                <div class="flex flex-col items-center justify-between group rounded-md shadow-lg transition-transform group-hover:scale-105 overflow-hidden h-full">
                    <img src="/static/images/restaurant_placeholder.png"
                         alt="Restaurant placeholder"
                         class="w-auto h-60 p-2" />
                    <a href="/restaurant/${restaurant.id}" class="block w-full">
                      <div class="bg-white p-4 flex flex-col gap-2 w-full">
                          <div class="flex flex-col">
                              <h3 class="font-semibold text-lg text-green-800 tracking-wide">${restaurant.name}</h3>
                              <p class="text-green-600">${restaurant.price_range}</p>
                          </div>
                          <p class="text-green-600">${restaurant.description}</p>
                      </div>
                    </a>
                </div>
            </div>`;
  });

  const navBtnContainer = document.getElementById("nav-btn-container");
  navBtnContainer.className = "flex justify-center items-center gap-3 p-5";
  restaurantList.innerHTML = htmlString;

  document.getElementById("prev-btn").addEventListener("click", async () => {
    if (isLoading) return;
    isLoading = true;
    const currentPage = parseInt(
      document.getElementById("page-info").innerText.split(" ")[1],
    );
    if (currentPage === 1) return;
    await refreshRestaurants(currentPage - 1);
    isLoading = false;
  });

  document.getElementById("next-btn").addEventListener("click", async () => {
    if (isLoading) return;
    isLoading = true;
    const currentPage = parseInt(
      document.getElementById("page-info").innerText.split(" ")[1],
    );
    const numPages = parseInt(
      document.getElementById("page-info").innerText.split(" ")[3],
    );
    if (currentPage === numPages) return;
    await refreshRestaurants(currentPage + 1);
    isLoading = false;
  });

  const pageInfo = document.getElementById("page-info");
  pageInfo.innerHTML = `Page ${restaurants.current_page} of ${restaurants.num_pages}`;
}

refreshRestaurants(1);

let isLoading = false;

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
  const response = await fetch("api/restaurants/create/", {
    method: "POST",
    body: new FormData(document.querySelector("#createRestaurantForm")),
  });

  if (response.ok) {
    document.getElementById("createRestaurantForm").reset();
    document.getElementById("formErrorMessage").classList.add("hidden");
    hideModal();
    refreshRestaurants(1);
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

document
  .getElementById("createRestaurantForm")
  .addEventListener("submit", (e) => {
    e.preventDefault();
    createRestaurant();
  });
