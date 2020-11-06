async function DeleteComment(commentID) {
  const res = await fetch("http://localhost:5000/post/comment/" + commentID, {
    method: "DELETE",
  });
  const res2 = await res.json();
  return res2;
}
let box = document.querySelector(".commentbox");

if (box) {
  box.addEventListener("click", (e) => {
    if (e.target.classList.contains("deleteComment")) {
      const commentID = e.target.dataset.comment;
      DeleteComment(commentID)
        .then((data) => {
          console.log(data.message);
          window.location.reload();
        })
        .catch((err) => console.log(err));
    }
  });
}
