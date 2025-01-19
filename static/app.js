let audio = document.getElementsByClassName("recommend")
let url = document.getElementsByTagName("source")

// function to empty the music modal after closing it
function empty_modal(modal){
  modal.innerHTML = ""
}

// function to show recommendations based on the song you chose
function show_recommendations(original_song, recommended_songs, labels){

  let user_recommended_songs = Object.keys(recommended_songs)
  let recommendation_modal = document.getElementsByClassName("show_recommend")
  let close = [...document.getElementsByClassName("close")]

  empty_modal(recommendation_modal[0])
  
  close.map((val) => {
    val.addEventListener("click" , (e) => {
      empty_modal(recommendation_modal[0])
    })
  })
  // placing each recommended song inside an audio tag, inside the music modal
  recommendation_modal[0].innerHTML = `
           <h5 class = "mb-3">Song you chose</h5>
           <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[original_song]}/${original_song}" type="audio/mpeg">
            </audio>
            <h5 class = "mb-3">Recommendations</h5>
            <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[user_recommended_songs[0]]}/${user_recommended_songs[0]}" type="audio/mpeg">
            </audio>
            <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[user_recommended_songs[1]]}/${user_recommended_songs[1]}" type="audio/mpeg">
            </audio>
            <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[user_recommended_songs[2]]}/${user_recommended_songs[2]}" type="audio/mpeg">
            </audio>
            <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[user_recommended_songs[3]]}/${user_recommended_songs[3]}" type="audio/mpeg">
            </audio>
            <audio controls>
                <source src="static/dataset/Data/genres_original/${labels[user_recommended_songs[4]]}/${user_recommended_songs[4]}" type="audio/mpeg">
            </audio>
  `
}

let audio_section_arr = [...audio[0].children[0].children]
let audio_arr = []
for(let i = 0; i < audio_section_arr.length; i++){
  audio_section_arr[i].classList = "mt-3 me-3 p-3 card col"
  audio_arr.push(...audio_section_arr[i].children)
}

// changing the normal behaviour of boostrap modals
// to show a modal by clicking on a div
audio_arr.map((val) => {
  val.classList.value = "mt-3 lh-base p-3 col card text-start add_hover"
  val.dataset.bsToggle = "modal"
  val.dataset.bsTarget = "#musicModal"
  let h4 = document.createElement("h4")
  h4.classList.value = "label ms-3 mt-2"
  val.appendChild(h4)
})

let url_arr = [...url]

// fetching labels of audio files with their names
async function fetchAudioLabels() {
  const response = await fetch("/get_data")
  const data = await response.json()
  const labels = data.list
  return labels
}

fetchAudioLabels().then((labels) => {
  let audio_labels = []

  audio_labels.push(...url_arr.map(function(val) {
    let filename = val.src.split("/").slice(-1)[0]
    return [labels[filename], filename]
  }))

  let h4_labels = document.getElementsByClassName("label")

  // putting labels and names in an h4 tag for display
  for (let i = 0; i < audio_labels.length; i++){
    h4_labels[i].setAttribute('style', 'white-space: pre;');
    h4_labels[i].textContent = `${audio_labels[i][0]}\r\n${audio_labels[i][1]}`
  }

  // sending the selected audio file to recommender.py file for finding similarities
  audio_arr.map((val) => {
    val.addEventListener("click", (e, filename) => {
      let src = e.currentTarget.children[0].children[0].src

      filename = src.split("/").slice(-1)[0]
      let payload = { data: filename};
      // using post request for submitting data
      fetch("/submit_file", {
        method: "post",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      })
      .then(response => response.json())
      .then(data => {
        // console.log("Response from FastAPI:", data);
        show_recommendations(filename ,data, labels)
      })
    })
  })
  
})


let ul = document.getElementsByClassName("music-dropdown")[0]

for (let i = 0; i < ul.children.length; i++){
  ul.children[i].addEventListener("click", (e) => {
    ul.previousElementSibling.textContent = e.target.textContent
    audio[0].style.display = "block"
  })
}
