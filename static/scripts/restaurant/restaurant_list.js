const PAGE_WIDTH = 2;
let currentSearchTerm = "";

// Fetch CSRF token dari meta tag untuk digunakan dalam permintaan AJAX POST
const csrfToken = document
  .querySelector("meta[name='csrfmiddlewaretoken']")
  .getAttribute("content");

// Mendapatkan daftar ID restoran yang ada di wishlist pengguna
async function getWishlist() {
  try {
    const response = await fetch("/wishlist/wishlist/status/"); // Menggunakan endpoint yang ada
    const data = await response.json();
    return data; // Mengembalikan array ID restoran yang ada di wishlist
  } catch (error) {
    console.error("Error fetching wishlist status:", error);
    return []; // Default jika terjadi error
  }
}

async function getRestaurants(page, search = "") {
  const response = await fetch(
    `api/restaurants/?page=${page}&page_size=8&search=${search}`,
  );
  return await response.json();
}

function createRestaurantCard(restaurant, userRole, wishlistIds) {
  const isInWishlist = wishlistIds.includes(restaurant.id);
  return `
                  <div class="relative group h-full">
                <a href="/restaurant/${
                  restaurant.id
                }" class="flex flex-col items-center justify-between group rounded-xl shadow-lg transition-transform group-hover:scale-105 overflow-hidden h-full bg-red-100">
                <img src="/static/images/restaurant_placeholder_${
                  restaurant.placeholder_image
                }.png"
                         alt="Restaurant placeholder"
                         class="w-auto h-60 p-2" />
                      <div class="bg-white p-6 flex flex-col gap-2 w-full bg-[#F5F5F5]">
                          <h3 class="font-bold text-xl text-rj-orange tracking-wide line-clamp-1">${
                            restaurant.name
                          }</h3>
                          <p class="line-clamp-2 text-sm min-h-10">${
                            restaurant.address
                          }</p>
                      </div>
                      </a>
                      <button id="love-btn-${
                        restaurant.id
                      }" class="absolute right-3 top-3 bg-gray-300  rounded-full p-3 group-hover:scale-105 text-gray-500 hover:text-red-500 transition duration-300" onclick="toggleWishlist('${
                        restaurant.id
                      }')">
                          <svg id="heart-icon-${
                            restaurant.id
                          }" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="${
                            isInWishlist ? "red" : "none"
                          }" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 010 6.364L12 20.364l7.682-7.682a4.5 4.5 0 10-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                      </button>
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
    pageString += `<a href="?page=1&search=${currentSearchTerm}" class="${pageClass} text-white cursor_pointer hover:bg-orange-700 bg-rj-orange">1</a>`;
    pageString += `<span class="font-semibold text-rj-orange">...</span>`;
  }
  response.page_range.forEach((page) => {
    if (
      page < response.current_page - PAGE_WIDTH ||
      page > response.current_page + PAGE_WIDTH
    ) {
      return;
    }
    if (page === response.current_page) {
      pageString += `<span class="${pageClass} text-rj-orange">${page}</span>`;
    } else {
      pageString += `<a href="?page=${page}&search=${currentSearchTerm}" class="${pageClass} text-white cursor_pointer hover:bg-orange-700 bg-rj-orange">${page}</a>`;
    }
  });
  if (response.current_page < response.num_pages - PAGE_WIDTH) {
    pageString += `<span class="font-semibold text-rj-orange">...</span>`;
    pageString += `<a href="?page=${response.num_pages}&search=${currentSearchTerm}" class="${pageClass} text-white cursor_pointer hover:bg-orange-700 bg-rj-orange">${response.num_pages}</a>`;
  }

  pageInfo.innerHTML = pageString;

  if (response.has_previous) {
    prevBtn.href = `?page=${
      response.current_page - 1
    }&search=${currentSearchTerm}`;
  } else {
    prevBtn.classList.add("hidden");
  }

  if (response.has_next) {
    nextBtn.href = `?page=${
      response.current_page + 1
    }&search=${currentSearchTerm}`;
  } else {
    nextBtn.classList.add("hidden");
  }
}

async function toggleWishlist(restaurantId) {
  const heartIcon = document.getElementById(`heart-icon-${restaurantId}`);
  const isInWishlist = heartIcon.getAttribute("fill") === "red";

  if (isInWishlist) {
    await removeFromWishlist(restaurantId);
  } else {
    await addToWishlist(restaurantId);
  }
}

// Fungsi untuk mengatur navigasi halaman
function updatePagination(response) {
  const navBtnContainer = document.getElementById("nav-btn-container");
  navBtnContainer.className = "flex justify-center items-center gap-3 p-5";

  const pageInfo = document.getElementById("page-info");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const pageClass =
    "rounded-lg w-10 aspect-square flex justify-center items-center";

  let pageString = "";
  if (response.current_page > 1 + PAGE_WIDTH) {
    pageString += `<a href="?page=1" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">1</a>`;
    pageString += `<span class="font-semibold text-green-800">...</span>`;
  }

  response.page_range.forEach((page) => {
    if (
      page < response.current_page - PAGE_WIDTH ||
      page > response.current_page + PAGE_WIDTH
    )
      return;

    pageString +=
      page === response.current_page
        ? `<span class="${pageClass} text-green-800">${page}</span>`
        : `<a href="?page=${page}" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">${page}</a>`;
  });

  if (response.current_page < response.num_pages - PAGE_WIDTH) {
    pageString += `<span class="font-semibold text-green-800">...</span>`;
    pageString += `<a href="?page=${response.num_pages}" class="${pageClass} text-white cursor_pointer hover:bg-green-600 bg-green-800">${response.num_pages}</a>`;
  }

  pageInfo.innerHTML = pageString;
  prevBtn.classList.toggle("hidden", !response.has_previous);
  nextBtn.classList.toggle("hidden", !response.has_next);
  prevBtn.href = response.has_previous
    ? `?page=${response.current_page - 1}`
    : "#";
  nextBtn.href = response.has_next ? `?page=${response.current_page + 1}` : "#";
}

async function updateWishlistCount() {
  try {
    const response = await fetch("/wishlist/wishlist/status/count/"); // Endpoint baru untuk menghitung jumlah wishlist
    if (response.ok) {
      const data = await response.json();
      const countElement = document.getElementById("wishlist-count");

      if (data.count > 0) {
        countElement.textContent = data.count;
        countElement.classList.remove("hidden"); // Tampilkan badge jika ada item
      } else {
        countElement.classList.add("hidden"); // Sembunyikan badge jika tidak ada item
      }
    } else {
      console.error("Failed to fetch wishlist count");
    }
  } catch (error) {
    console.error("Error fetching wishlist count:", error);
  }
}

// Panggil fungsi ini saat halaman dimuat
document.addEventListener("DOMContentLoaded", () => {
  updateWishlistCount();
});

// Fungsi untuk menambahkan item ke wishlist menggunakan AJAX
async function addToWishlist(restaurantId) {
  try {
    const response = await fetch(`/wishlist/add/${restaurantId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });

    if (response.ok) {
      const data = await response.json();
      if (data.created) {
        document
          .getElementById(`heart-icon-${restaurantId}`)
          .setAttribute("fill", "red");
        showNotification(
          `${data.restaurant_name} added to your wishlist!`,
          "success",
        );
        updateWishlistCount(); // Perbarui jumlah wishlist
      } else {
        showNotification(
          `${data.restaurant_name} is already in your wishlist.`,
          "error",
        );
      }
    } else {
      throw new Error("Failed to add to wishlist");
    }
  } catch (error) {
    console.error("Error:", error);
    showNotification("Something went wrong. Please try again.", "error");
  }
}

// Fungsi untuk menghapus dari wishlist
async function removeFromWishlist(restaurantId) {
  try {
    const response = await fetch(`/wishlist/remove/${restaurantId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });

    if (response.ok) {
      const data = await response.json();
      if (data.deleted) {
        document
          .getElementById(`heart-icon-${restaurantId}`)
          .setAttribute("fill", "none");
        showNotification("Removed from your wishlist.", "error");
        updateWishlistCount(); // Perbarui jumlah wishlist
      } else {
        showNotification("Failed to remove from wishlist.", "error");
      }
    } else {
      throw new Error("Failed to remove from wishlist");
    }
  } catch (error) {
    console.error("Error:", error);
    showNotification("Something went wrong. Please try again.", "error");
  }
}

const url = new URL(window.location.href);
const page = url.searchParams.get("page") || 1;
currentSearchTerm = url.searchParams.get("search") || "";
const searchInput = document.getElementById("searchInput");

async function refreshRestaurants(page) {
  searchInput.value = currentSearchTerm;
  const response = await getRestaurants(page, currentSearchTerm);
  if (response.current_page != page) {
    window.location.href = `?page=${response.current_page}&search=${currentSearchTerm}`;
  }

  const user_data = await fetch("/user/").then((response) => response.json());
  const wishlistIds = await getWishlist(); // Dapatkan ID wishlist
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
    .map((restaurant) =>
      createRestaurantCard(restaurant, user_data.role, wishlistIds),
    )
    .join("");

  restaurantList.innerHTML = htmlString;
}

refreshRestaurants(page);

// Modal Handlers
const modal = document.getElementById("crudModal");
const modalContent = document.getElementById("crudModalContent");

function showModal() {
  modal.classList.remove("hidden");
  setTimeout(() => {
    modalContent.classList.remove("opacity-0", "scale-95");
    modalContent.classList.add("opacity-100", "scale-100");
  }, 50);
}

function hideModal() {
  modalContent.classList.remove("opacity-100", "scale-100");
  modalContent.classList.add("opacity-0", "scale-95");
  setTimeout(() => {
    modal.classList.add("hidden");
  }, 150);
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalBtn").addEventListener("click", hideModal);

// Fungsi untuk membuat restoran baru
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
      behavior: "smooth",
      block: "center",
      inline: "nearest",
    });
  }
}

function showNotification(message, type) {
  const notification = document.getElementById("notification");
  notification.textContent = message;

  // Reset kelas Tailwind untuk menghindari kelas sebelumnya tertinggal
  notification.className =
    "fixed bottom-4 right-4 p-4 rounded-lg text-white text-sm font-semibold shadow-lg transition-all duration-500 ease-out opacity-0";

  // Tambahkan kelas warna berdasarkan tipe
  if (type === "success") {
    notification.classList.add("bg-green-500"); // Hijau untuk success
  } else if (type === "error") {
    notification.classList.add("bg-red-500"); // Merah untuk error
  }

  // Tampilkan notifikasi dengan animasi smooth
  setTimeout(() => {
    notification.classList.remove("opacity-0");
    notification.classList.add("opacity-100");
  }, 100); // Delay kecil agar animasi smooth saat muncul

  // Hapus notifikasi setelah beberapa detik dengan fade-out yang lebih lama
  setTimeout(() => {
    notification.classList.remove("opacity-100");
    notification.classList.add("opacity-0");
    setTimeout(() => notification.classList.add("hidden"), 600); // Tambahkan hidden setelah animasi selesai
  }, 4000); // Menghilang setelah 4 detik
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
const debouncedSearch = debounce((value) => {
  currentSearchTerm = value;
  refreshRestaurants(1);
}, 300);

searchInput.addEventListener("input", (e) => {
  debouncedSearch(e.target.value);
});