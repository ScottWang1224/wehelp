const burgerMenu = document.querySelector(".burger-menu");
const mobileMenu = document.querySelector(".mobile-menu");
const closeMenu = document.querySelector(".close-menu");

burgerMenu.addEventListener("click", function () {
  mobileMenu.classList.add("active");
});

closeMenu.addEventListener("click", function () {
  mobileMenu.classList.remove("active");
});

const url1 = "https://cwpeng.github.io/test/assignment-3-1";
const url2 = "https://cwpeng.github.io/test/assignment-3-2";

Promise.all([
  fetch(url1).then(response => response.json()),
  fetch(url2).then(response => response.json())
]).then(function(results) {
  const data1 = results[0];
  const data2 = results[1];

  const attractions = data1.rows;
  const pictures = data2.rows;
  const bars = document.querySelector(".bars");

  const barClasses = [
    "bar bar-large",
    "bar bar-wide",
    "bar bar-small"
  ];

  for (let i = 0; i < 3; i++) {
    const attraction = attractions[i];

    const pictureData = pictures.find(function(item) {
      return item.serial === attraction.serial;
    });

    const imageUrl =
      "https://cwpeng.github.io/test" +
      pictureData.pics.split(".jpg")[0] + ".jpg";

    const bar = document.createElement("div");
    bar.className = barClasses[i];

    const img = document.createElement("img");
    img.src = imageUrl;

    const span = document.createElement("span");
    span.textContent = attraction.sname;

    bar.appendChild(img);
    bar.appendChild(span);
    bars.appendChild(bar);
  }

  const cards = document.querySelector(".cards");

  function renderCards(startIndex, count) {
    for (let i = startIndex; 
      i < startIndex + count && i < attractions.length; 
      i++
    ) {
      const attraction = attractions[i];

      const pictureData = pictures.find(function(item) {
        return item.serial === attraction.serial;
      });

      const imageUrl =
        "https://cwpeng.github.io/test" +
        pictureData.pics.split(".jpg")[0] +
        ".jpg";

      const card = document.createElement("div");
      card.className = "card";

      const bgImg = document.createElement("img");
      bgImg.className = "card-bg";
      bgImg.src = imageUrl;
      bgImg.alt = "Scenery";

      const star = document.createElement("img");
      star.className = "star";
      star.src = "star.png";
      star.alt = "Star";

      const title = document.createElement("div");
      title.className = "card-title";
      title.textContent = attraction.sname;

      card.appendChild(bgImg);
      card.appendChild(star);
      card.appendChild(title);
      cards.appendChild(card);
    }
  }

  renderCards(3, 10);
  let currentIndex = 13;
  const loadMoreButton = document.querySelector("#load-more");

  if (currentIndex >= attractions.length) {
    loadMoreButton.style.display = "none";
  }

  loadMoreButton.addEventListener("click", function() {
    renderCards(currentIndex, 10);
    currentIndex += 10;

    if (currentIndex >= attractions.length) {
      loadMoreButton.style.display = "none";
    }
  });
});
