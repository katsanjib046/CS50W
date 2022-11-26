document.addEventListener('DOMContentLoaded', function() {

    // Like button
    document.querySelectorAll('.like').forEach(function(button) {
        button.onclick = function() 
        {
            const id = this.dataset.id;
            like_post(id);
        }
    });
    
    // Dislike button
    document.querySelectorAll('.dislike').forEach(function(button) {
        button.onclick = function() 
        {
            const id = this.dataset.id;
            dislike_post(id);
        }
    });

    // Edit button
    document.querySelectorAll('.edit').forEach(function(button) {
        button.onclick = function() 
        {
            const id = this.dataset.id;
            edit_post(id);
        }
    });

    // // Edit submit button
    // document.querySelectorAll('.submitEditedPost').forEach(function(button) {
    //     button.onclick = function() 
    //     {
    //         const id = this.dataset.id;
    //         edit_post(id);
    //     }
    // });
});


function like_post(id) {
    fetch(`/likes/${id}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#like-${id}`).innerHTML = result.likesCount;
        // console.log(result);
        // window.location.reload();
    });
}

function dislike_post(id) {
    fetch(`/dislikes/${id}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#dislike-${id}`).innerHTML = result.dislikesCount;
        // console.log(result);
        // window.location.reload();
    });
}

function edit_post(id) {
    // make a test area first
    let oldContent = document.querySelector(`#content-${id}`).innerHTML;
    document.querySelector(`#content-${id}`).innerHTML = `<textarea id="edit-${id}" cols="30" rows="5"></textarea>
    <button id="submitEditedPost-${id}" data-id="${id}">Submit</button>`;
    // fill the text area with the old content
    document.querySelector(`#edit-${id}`).value = oldContent;
    // add event listener to the submit button
    document.querySelector(`#submitEditedPost-${id}`).addEventListener('click', function() {

    fetch(`/edit/${id}`, {
        method: 'PUT',
        body : JSON.stringify({
            postContent: document.querySelector(`#edit-${id}`).value
    })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        // window.location.reload();
        document.querySelector(`#content-${id}`).innerHTML = result.postContent;
    });
});
}


// function edit_text(id) {
//     document.querySelector(`#content-${id}`).innerHTML = `<textarea id="edit-${id}" cols="30" rows="5"></textarea>
//     <button class="submitEditedPost" data-id="${id}">Submit</button>`;
// }