async function getRestaurants(page) {
  const response = await fetch(`api/restaurants/?page=${page}&page_size=8`);
  return await response.json();
}

async function refreshRestaurants(page) {
  const response = await getRestaurants(page);
  const user_data = await fetch("/user/").then((response) => response.json());
  const restaurantList = document.getElementById("restaurant-list");
  let htmlString = "";
  if (response.results.length === 0) {
    return;
  }
  restaurantList.className =
    "grid gap-6 sm:grid-cols-2 xl:grid-cols-4 p-3 md:p-10";
  response.results.forEach((restaurant) => {
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
                ${
                  user_data.role === "R"
                    ? `<div class="absolute -top-2 right-2 md:-right-4 flex space-x-1 group-hover:scale-105 transition-transform">
                    <a href="/restaurant/delete/${restaurant.id}"
                       class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                        <svg xmlns="http://www.w3.org/2000/svg"
                             class="h-6 w-6 sm:h-8 sm:w-8"
                             viewBox="0 0 20 20"
                             fill="currentColor">
                            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    </a>
                </div>
                `
                    : ""
                }
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
  pageInfo.innerHTML = `Page ${response.current_page} of ${response.num_pages}`;
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
