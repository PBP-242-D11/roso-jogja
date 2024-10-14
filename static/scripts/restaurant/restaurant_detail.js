async function getRestaurantDetail(id) {
  const response = await fetch(`/restaurant/api/restaurants/${id}/`);
  return response.json();
}

async function refreshRestaurantDetail(id) {
  const restaurant = await getRestaurantDetail(id);
  const restaurantMeta = document.getElementById("restaurant-meta");
  const restaurantFoods = document.getElementById("restaurant-foods");

  restaurantMeta.innerHTML = `
    <h1>${restaurant.name}</h1>
    <p>${restaurant.address}</p>
    <p>${restaurant.price_range}</p>
    <p>${restaurant.description}</p>
  `;

  let htmlString = "";
  restaurant.foods.forEach((food) => {
    htmlString += `
      <div class="flex flex-row items-center justify-between bg-green-100 min-h-16 rounded-lg p-5">
        <div class="flex flex-col">
          <h3 class="font-medium">${food.name}</h3>
          <p class="text-gray-700 text-sm">${food.description}</p>
        </div>
        <p>${food.price}</p>
      </div>
    `;
  });

  restaurantFoods.innerHTML = htmlString;
}

const url = new URL(window.location.href);
const id = url.pathname.split("/")[2];

refreshRestaurantDetail(id);
