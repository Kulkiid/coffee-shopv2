const navLinks = document.querySelectorAll(".nav-menu .nav-link");
const menuOpenButton = document.querySelector("#menu-open-button");
const menuCloseButton = document.querySelector("#menu-close-button");


menuOpenButton.addEventListener("click", () => {
    
    document.body.classList.toggle("show-mobile-menu");
})

menuCloseButton.addEventListener("click", () => {
    document.body.classList.remove("show-mobile-menu");
});

navLinks.forEach(link => {
    link.addEventListener("click", () => menuOpenButton.click());
})

const coffeeChoices = document.querySelectorAll('input[name="coffee"]');
const coffeeChoiceIcon = document.querySelector("#coffee-choice-icon");
const selectedOrderList = document.querySelector("#selected-order-list");
const orderTotalAmount = document.querySelector("#order-total-amount");

if (coffeeChoices.length) {
  const categoryIcons = {
    hot_beverages: "fa-mug-hot",
    cold_beverages: "fa-glass-water",
    refreshments: "fa-lemon",
    special_combo: "fa-utensils",
    desserts: "fa-cake-candles",
    burger_and_fries: "fa-burger",
  };

  const renderSelectedOrders = () => {
    const selectedChoices = [...coffeeChoices].filter(choice => choice.checked);
    let total = 0;

    if (selectedOrderList) {
      selectedOrderList.replaceChildren();
      if (!selectedChoices.length) {
        const emptyMessage = document.createElement("li");
        emptyMessage.className = "order-list-empty";
        emptyMessage.textContent = "No menu items selected yet.";
        selectedOrderList.append(emptyMessage);
      }

      selectedChoices.forEach(choice => {
        const option = choice.closest(".order-menu-option");
        const label = option.querySelector("span").textContent;
        const priceMatch = label.match(/From \$([0-9.]+)/);
        const itemPrice = priceMatch ? Number(priceMatch[1]) : 0;
        total += itemPrice;

        const orderItem = document.createElement("li");
        const itemName = document.createElement("span");
        const removeButton = document.createElement("button");
        itemName.textContent = label.replace(/ - From \$[0-9.]+$/, "");
        removeButton.type = "button";
        removeButton.className = "remove-order-item";
        removeButton.dataset.removeValue = choice.value;
        removeButton.setAttribute("aria-label", `Remove ${itemName.textContent}`);
        removeButton.innerHTML = '<i class="fa-solid fa-xmark" aria-hidden="true"></i>';
        orderItem.append(itemName, removeButton);
        selectedOrderList.append(orderItem);
      });
    } else {
      total = selectedChoices.reduce((sum, choice) => {
        const label = choice.closest(".order-menu-option").querySelector("span").textContent;
        const priceMatch = label.match(/From \$([0-9.]+)/);
        return sum + (priceMatch ? Number(priceMatch[1]) : 0);
      }, 0);
    }

    if (orderTotalAmount) {
      orderTotalAmount.textContent = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(total);
    }

    if (coffeeChoiceIcon && selectedChoices.length === 1) {
      coffeeChoiceIcon.className = `fa-solid ${categoryIcons[selectedChoices[0].value] || "fa-mug-hot"}`;
    } else if (coffeeChoiceIcon) {
      coffeeChoiceIcon.className = "fa-solid fa-basket-shopping";
    }
  };

  coffeeChoices.forEach(choice => choice.addEventListener("change", renderSelectedOrders));

  selectedOrderList?.addEventListener("click", event => {
    const removeButton = event.target.closest("[data-remove-value]");
    if (!removeButton) return;

    const choice = [...coffeeChoices].find(item => item.value === removeButton.dataset.removeValue);
    if (choice) {
      choice.checked = false;
      renderSelectedOrders();
    }
  });

  renderSelectedOrders();
}

const swiper = new Swiper('.slider-wrapper', {
    loop: true,
    grabCursor: true,
    spaceBetween: 25,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    dynamicBullets: true,
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },


  // Responsive breakpoints
  breakpoints: {
    0: {
        slidesPerView: 1
    },
    768: {
        slidesPerView: 2
    },
    1024: {
        slidesPerView: 3
    }
  }
});