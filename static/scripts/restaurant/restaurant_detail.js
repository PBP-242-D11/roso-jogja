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
            ? `<div class="flex flex-row items-center justify-between gap-2"> 
                <a href="/restaurant/api/restaurants/${restaurant.id}/delete_food/${food.id}" class="bg-red-500 hover:bg-red-600 text-white rounded-lg p-2 transition duration-300 shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 sm:h-8 sm:w-8" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </a> 
                <a href="/restaurant/api/restaurants/${restaurant.id}/update_food/${food.id}" class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg p-2 transition duration-300 shadow-md">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 sm:h-8 sm:w-8" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>          
                </a>
              </div>`
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
            <button id="addToCardBtn-${food.id}" class="flex items-center justify-center bg-red-500 hover:bg-red-600 text-white rounded-lg p-2 transition duration-300 shadow-md" title="Add to Cart">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 512 512" fill="currentColor">
                <path d="M483.158,164.434H350.465l-60.034,58.974c-8.128,7.988-18.892,12.392-30.29,12.392c-11.684,0-22.647-4.602-30.839-12.942
                    c-15.834-16.13-16.41-41.595-1.94-58.424H28.843C12.91,164.434,0,177.342,0,193.276v9.622c0,15.695,12.556,28.448,28.178,28.793
                    l31.094,190.443c3.771,23.074,23.698,40.001,47.068,40.001h299.272c23.37,0,43.296-16.927,47.069-40.001L483.774,231.7
                    C499.42,231.371,512,218.609,512,202.898v-9.622C512,177.342,499.091,164.434,483.158,164.434z M319.98,351.696h-48.974v48.967
                    h-30.051v-48.967H191.98v-30.05h48.974v-48.982h30.051v48.982h48.974V351.696z"/>
                <path d="M277.62,210.36L397.493,92.598c9.828-9.655,9.968-25.449,0.312-35.276c-9.647-9.82-25.449-9.959-35.268-0.312
                    L242.655,174.778c-9.827,9.656-9.967,25.441-0.312,35.269C252.007,219.875,267.792,220.023,277.62,210.36z"/>
              </svg>
            </button> 
          </div>`
          : ""
        }
      </div>
    `;
  });
  fetchAndDisplayReviews(id, user_data)

  restaurantFoods.innerHTML = htmlString;

  foods.forEach((food) => {
    const addToCardBtn = document.getElementById(`addToCardBtn-${food.id}`);
    if (addToCardBtn) {
      addToCardBtn.addEventListener("click", async () => {
        await fetch(`/order/api/add_food_to_cart/${food.id}/`).then((response) => response.json());
      });
    }
  });

  if (user_data.role === "C") {
    const addReviewButton = document.createElement("button");
    addReviewButton.classList.add("bg-green-600", "text-white", "hover:bg-green-700", "px-4", "py-2", "rounded-md", "font-medium", "mt-6");
    addReviewButton.innerText = "Add Review";
    addReviewButton.addEventListener("click", showReviewModal);
  
    const reviewContainer = document.getElementById("reviews-container");
    reviewContainer.style.display = "flex";
    reviewContainer.style.flexDirection = "column";
    reviewContainer.style.alignItems = "center";
    reviewContainer.appendChild(addReviewButton);
  }
}

async function fetchAndDisplayReviews(id, user_data) {
  const response = await fetch(`/reviews/api/get_reviews/${id}/`);
  const data = await response.json();
  const reviewContainer = document.getElementById("reviews-container");

  // Hapus teks "no reviews" jika ada review yang ditampilkan
  const noReviewsText = document.getElementById("no-reviews-text");
  if (data.reviews.length > 0 && noReviewsText) {
    noReviewsText.remove();
  }

  if (data.reviews.length === 0) {
    return;
  } else {
    data.reviews.forEach(review => {
      const reviewElement = document.createElement("div");
      reviewElement.classList.add("bg-gray-100", "p-4", "rounded", "mt-4", "relative");
      // Format tampilan review dengan ikon bintang
      let starsHtml = `<span class="inline-flex items-center align-middle gap-x-0	">`; 
      for (let i = 1; i <= 5; i++) {
        starsHtml += `
          <svg class="w-5 h-5 ${i <= review.rating ? 'text-yellow-500' : 'text-gray-400'}" 
               style="vertical-align: middle;" 
               xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
            <path d="M11.049 2.927a1 1 0 011.902 0l1.885 3.82a1 1 0 00.756.545l4.2.61a1 1 0 01.564 1.706l-3.04 2.968a1 1 0 00-.287.885l.718 4.179a1 1 0 01-1.451 1.054L12 17.347l-3.755 1.973a1 1 0 01-1.451-1.054l.718-4.179a1 1 0 00-.287-.885l-3.04-2.968a1 1 0 01.564-1.706l4.2-.61a1 1 0 00.756-.545l1.885-3.82z" />
          </svg>`;
      }
      starsHtml += `</span>`;

      reviewElement.innerHTML = `
        <p><strong>${review.user}</strong> rated: ${starsHtml}</p>
        <p>${review.comment}</p>
        <p class="text-sm text-gray-500">${review.created_at}</p>
      `;

      // Tambahkan tombol delete jika user adalah admin
      if (user_data.role === "A") {
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("absolute", "top-0", "right-0", "bg-red-600", "hover:bg-red-700", "text-white", "w-6", "h-6", "flex", "items-center", "justify-center", "rounded", "shadow-lg");
        deleteButton.innerHTML = `<span class="text-lg font-semibold">X</span>`;
        deleteButton.onclick = () => deleteReview(review.id, reviewElement);
        reviewElement.appendChild(deleteButton);
      }
      reviewContainer.appendChild(reviewElement);
    });
  }
}


// Fungsi untuk menampilkan modal review
function showReviewModal() {
  const modalContent = `
    <div class="relative p-6">
      <button onclick="hideModal()" 
              class="absolute top-0 right-0 -mt-4 -mr-4 bg-red-600 text-white w-8 h-8 flex items-center justify-center rounded shadow-lg">
        <span class="text-lg font-semibold">X</span>
      </button>

      <div class="flex flex-col gap-4 mt-4">
        <label class="flex items-center">Rating: <!-- Align teks dan bintang dalam satu baris -->
          <div id="star-rating" class="flex gap-x-0 ml-2"> <!-- Mengatur gap kecil dan inline -->
            ${[...Array(5)].map((_, i) => `
              <svg class="star w-5 h-5 cursor-pointer text-gray-400 inline-block align-middle" data-value="${i + 1}" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                <path d="M11.049 2.927a1 1 0 011.902 0l1.885 3.82a1 1 0 00.756.545l4.2.61a1 1 0 01.564 1.706l-3.04 2.968a1 1 0 00-.287.885l.718 4.179a1 1 0 01-1.451 1.054L12 17.347l-3.755 1.973a1 1 0 01-1.451-1.054l.718-4.179a1 1 0 00-.287-.885l-3.04-2.968a1 1 0 01.564-1.706l4.2-.61a1 1 0 00.756-.545l1.885-3.82z" />
              </svg>
            `).join('')}
          </div>
        </label>
        <input type="hidden" id="review-rating" value="0">
        <label>Comment: <textarea id="review-comment" class="border rounded px-2 py-1 w-full"></textarea></label>
        <div class="flex justify-end mt-4">
          <button class="bg-green-600 text-white px-4 py-2 rounded" onclick="submitReview()">Submit Review</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById("crudModalContent").innerHTML = modalContent;
  showModal();

  const stars = document.querySelectorAll("#star-rating .star");
  stars.forEach(star => {
    star.addEventListener("click", () => {
      const rating = star.getAttribute("data-value");
      document.getElementById("review-rating").value = rating;
      updateStarRating(rating);
    });
  });
}

// Fungsi untuk memperbarui tampilan bintang berdasarkan rating yang dipilih
function updateStarRating(rating) {
  const stars = document.querySelectorAll("#star-rating .star");
  stars.forEach(star => {
    const starValue = star.getAttribute("data-value");
    if (starValue <= rating) {
      star.classList.add("text-yellow-500");
      star.classList.remove("text-gray-400");
    } else {
      star.classList.add("text-gray-400");
      star.classList.remove("text-yellow-500");
    }
  });
}


// Fungsi untuk mengirim review melalui API
async function submitReview() {
  const rating = document.getElementById("review-rating").value;
  const comment = document.getElementById("review-comment").value;
  const csrfToken = document.getElementById("restaurant-reviews").getAttribute("data-csrf-token");
  const response = await fetch(`/reviews/api/add_review/${id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrfToken,
    },
    body: `rating=${rating}&comment=${comment}`
  });

  const data = await response.json();
  if (data.success) {
    hideModal();
    const noReviewsText = document.getElementById("no-reviews-text");
    if (noReviewsText) {
      noReviewsText.remove();
    }
    const reviewContainer = document.getElementById("reviews-container");
    const reviewElement = document.createElement("div");
    reviewElement.classList.add("bg-gray-100", "p-4", "rounded", "mt-4");

    let starsHtml = `<span class="inline-flex items-center align-middle gap-x-0">`; 
    for (let i = 1; i <= 5; i++) {
      starsHtml += `
        <svg class="w-5 h-5 ${i <= data.review.rating ? 'text-yellow-500' : 'text-gray-400'}" 
             style="vertical-align: middle;" 
             xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
          <path d="M11.049 2.927a1 1 0 011.902 0l1.885 3.82a1 1 0 00.756.545l4.2.61a1 1 0 01.564 1.706l-3.04 2.968a1 1 0 00-.287.885l.718 4.179a1 1 0 01-1.451 1.054L12 17.347l-3.755 1.973a1 1 0 01-1.451-1.054l.718-4.179a1 1 0 00-.287-.885l-3.04-2.968a1 1 0 01.564-1.706l4.2-.61a1 1 0 00.756-.545l1.885-3.82z" />
        </svg>`;
    }
    starsHtml += `</span>`;

    reviewElement.innerHTML = `
      <p><strong>${data.review.user}</strong> rated: ${starsHtml}</p>
      <p>${data.review.comment}</p>
      <p class="text-sm text-gray-500">${data.review.created_at}</p>
    `;
    reviewContainer.appendChild(reviewElement);
    fetchAndDisplayReviews(id)
  } else {
    alert(data.error || "Failed to add review. Please try again.");
  }
}

async function deleteReview(reviewId, reviewElement) {
  const response = await fetch(`/reviews/api/delete_review/${reviewId}/`, {
      method: "DELETE",
  });

  const data = await response.json();
  if (data.success) {
      reviewElement.remove();
      const reviewContainer = document.getElementById("reviews-container");
      if (reviewContainer.childElementCount === 0) {
          // Jika tidak ada, tambahkan kembali teks "There are no reviews yet!"
          const noReviewsElement = document.createElement("p");
          noReviewsElement.id = "no-reviews-text";
          noReviewsElement.classList.add("text-gray-500", "italic", "mt-4");
          noReviewsElement.innerText = "There are no reviews yet!";
          reviewContainer.appendChild(noReviewsElement);
      }
    } else {
      alert("Failed to delete review. Please try again.");
  }
}

const url = new URL(window.location.href);
const id = url.pathname.split("/")[2];

refreshRestaurantDetail(id);

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
