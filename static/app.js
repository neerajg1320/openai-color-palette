const form = document.querySelector('#form');
form.addEventListener('submit', function (e) {
  e.preventDefault();

  getColors();
});

function getColors() {
  // Get the value of the query entered by user
  const query = form.elements.query.value;
  console.log(`submit: ${query}`);

  // We could have send this in json format
  // But we are sending it in form-data format
  fetch('/palette', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      query: query,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      createColorDivs(data.colors, document.querySelector('.container'));
    })
}

function createColorDivs(colors, container) {
  container.innerHTML = '';
  for (const color of colors) {
    // For each color create and append a div child to container
    const div = document.createElement('div');
    div.classList.add('color');
    div.style.backgroundColor = color;
    div.style.width = `calc(100%/${colors.length})`;

    // onClick: copy color to clipboard
    div.addEventListener('click', function () {
      navigator.clipboard.writeText(color);
    });

    // Append a span child to the div
    const span = document.createElement('span');
    span.innerText = color;
    div.appendChild(span);

    container.appendChild(div);
  }
}