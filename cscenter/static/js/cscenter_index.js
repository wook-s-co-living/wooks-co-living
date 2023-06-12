const categoryBtns = document.querySelectorAll('.cscenter--index--section--category--item')
const categoryContainer = document.querySelector('.cscenter--index--section--category--posts')
console.log(categoryBtns)
if (categoryBtns) {
  
  categoryBtns.forEach((btn) => {

    btn.addEventListener('click', async (event) => {
      categoryBtns.forEach((btn) => {
        if (btn.classList.contains('cscenter--index--section--category--btnhover')) {
          btn.classList.remove('cscenter--index--section--category--btnhover')
        }
      })

      const btnValue = btn.value
      btn.classList.add('cscenter--index--section--category--btnhover')

      try {
        const response = await fetch(
          `/cscenter/?category=${btnValue}`
        )

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const html = await response.text()
        const parser = new DOMParser()
        const doc = parser.parseFromString(html, 'text/html')
        const newContainer = doc.querySelector('.cscenter--index--section--category--posts')
        categoryContainer.innerHTML = newContainer.innerHTML
      } catch (error) {
        console.error(error)
      }
    })
  })
}