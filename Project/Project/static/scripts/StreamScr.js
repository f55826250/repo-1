// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#sender").addEventListener("click", () => {
        // submit the review
        let revBody = document.querySelector("#reviewText").value
        let rating = document.querySelector("#rating").value
        let pk = document.querySelector("#pk").value
        let csrftoken = getCookie('csrftoken');

        fetch("/submitreview", {
            method: "PUT",
            body: JSON.stringify({
                revBody:revBody,
                rating:rating,
                pk:pk,
            }),
            headers: { "X-CSRFToken": csrftoken },
        })
    })
    // add to favorites
    let fav = document.querySelector("#fav")
    fav.addEventListener("click", () => {
        let pk = document.querySelector("#pk").value
        let csrftoken = getCookie('csrftoken')
        if (fav.innerText  === "add to favorites") {
            fav.innerText  = "remove from favorites"
        } else if (fav.innerText  === "remove from favorites") {
            fav.innerText  = "add to favorites"
        }
        fetch("/favorite", {
            method: "PUT",
            body: JSON.stringify({
                pk:pk,
            }),
            headers: { "X-CSRFToken": csrftoken },
        })
    })

    
})