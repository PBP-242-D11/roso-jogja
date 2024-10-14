async function getRestaurants(page) {
  const response = await fetch(`api/restaurants/?page=${page}&page_size=8`);
  return await response.json();
}

async function refreshRestaurants(page) {
  const restaurants = await getRestaurants(page);
  const restaurantList = document.getElementById("restaurant-list");
  let htmlString = "";
  restaurantList.innerHTML = "";
  restaurants.results.forEach((restaurant) => {
    htmlString += `<div class="relative group h-full">
                <div class="flex flex-col items-center justify-between group rounded-md shadow-lg transition-transform group-hover:scale-105 overflow-hidden h-full">
                    <img src="/static/images/restaurant_placeholder.png"
                         alt="Plant placeholder"
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

  restaurantList.innerHTML = htmlString;

  const pageInfo = document.getElementById("page-info");
  pageInfo.innerHTML = `Page ${restaurants.current_page} of ${restaurants.num_pages}`;
}

refreshRestaurants(1);

let isLoading = false;

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
