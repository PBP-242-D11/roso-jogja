const PAGE_WIDTH = 2;
let currentSearchTerm = "";

async function getRestaurants(page, search = "") {
  const response = await fetch(
    `api/restaurants/?page=${page}&page_size=8&search=${search}`,
  );
  return await response.json();
}

function createRestaurantCard(restaurant, userRole) {
  return `
                  <div class="relative group h-full">
                <a href="/restaurant/${restaurant.id}" class="flex flex-col items-center justify-between group rounded-xl shadow-lg transition-transform group-hover:scale-105 overflow-hidden h-full bg-red-100">
                <img src="/static/images/restaurant_placeholder_${restaurant.placeholder_image}.png"
                         alt="Restaurant placeholder"
                         class="w-auto h-60 p-2" />
                      <div class="bg-white p-6 flex flex-col gap-2 w-full bg-[#F5F5F5]">
                          <h3 class="font-bold text-xl text-rj-orange tracking-wide line-clamp-1">${restaurant.name}</h3>
                          <p class="line-clamp-2 text-sm min-h-10">${restaurant.address}</p>
                      </div>
                </a>
                ${
                  userRole === "R"
                    ? `<div class="absolute -top-2 right-2 md:-right-4 flex space-x-1 group-hover:scale-105 transition-transform">
                    <a href="/restaurant/update/${restaurant.id}"
                       class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                        <svg xmlns="http://www.w3.org/2000/svg"
                             class="h-6 w-6 sm:h-8 sm:w-8"
                             viewBox="0 0 20 20"
                             fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                    </a>
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
}

function updatePagination(response) {
  const navBtnContainer = document.getElementById("nav-btn-container");
  const pageInfo = document.getElementById("page-info");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const pageClass =
    "rounded-lg w-10 aspect-square flex justify-center items-center";

  navBtnContainer.className = "flex justify-center items-center gap-3 p-5";

  pageString = "";
  if (response.current_page > 1 + PAGE_WIDTH) {
    pageString += `<a href="?page=1" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">1</a>`;
    pageString += `<span class="font-semibold text-green-800">...</span>`;
  }
  response.page_range.forEach((page) => {
    if (
      page < response.current_page - PAGE_WIDTH ||
      page > response.current_page + PAGE_WIDTH
    ) {
      return;
    }
    if (page === response.current_page) {
      pageString += `<span class="${pageClass} text-green-800">${page}</span>`;
    } else {
      pageString += `<a href="?page=${page}" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">${page}</a>`;
    }
  });
  if (response.current_page < response.num_pages - PAGE_WIDTH) {
    pageString += `<span class="font-semibold text-green-800">...</span>`;
    pageString += `<a href="?page=${response.num_pages}" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">${response.num_pages}</a>`;
  }

  pageInfo.innerHTML = pageString;

  if (response.has_previous) {
    prevBtn.href = `?page=${response.current_page - 1}`;
  } else {
    prevBtn.classList.add("hidden");
  }

  if (response.has_next) {
    nextBtn.href = `?page=${response.current_page + 1}`;
  } else {
    nextBtn.classList.add("hidden");
  }
}

async function refreshRestaurants(page) {
  const response = await getRestaurants(page, currentSearchTerm);
  if (response.current_page != page) {
    window.location.href = `?page=${response.current_page}&search=${currentSearchTerm}`;
  }

  const user_data = await fetch("/user/").then((response) => response.json());

  const restaurantList = document.getElementById("restaurant-list");
  let htmlString = "";

  updatePagination(response);
  if (response.results.length === 0) {
    restaurantList.className = "flex justify-center items-center h-96";
    restaurantList.innerHTML = `<h1 class="text-2xl text-gray-500">No restaurants found</h1>`;
    return;
  }

  restaurantList.className =
    "grid gap-6 sm:grid-cols-2 xl:grid-cols-4 p-3 md:p-10";

  htmlString = response.results
    .map((restaurant) => createRestaurantCard(restaurant, user_data.role))
    .join("");

  restaurantList.innerHTML = htmlString;
}

const url = new URL(window.location.href);
const page = url.searchParams.get("page") || 1;

refreshRestaurants(page);

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

// Debounce function to limit API calls during search
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Search functionality
const searchInput = document.getElementById("searchInput");
const debouncedSearch = debounce((value) => {
  currentSearchTerm = value;
  refreshRestaurants(1);
}, 300);

searchInput.addEventListener("input", (e) => {
  debouncedSearch(e.target.value);
});
