async function DeletePost(idPost) {
  const res = await fetch("http://localhost:5000/post/" + idPost, {
    method: "DELETE",
  });
  const res2 = await res.json();
  return res2;
}
async function ArchivePost(idPost) {
  const res = await fetch("http://localhost:5000/archive/" + idPost, {
    method: "PUT",
  });
  const res2 = await res.json();
  return res2;
}
async function UnArchivePost(idPost) {
  const res = await fetch("http://localhost:5000/unarchive/" + idPost, {
    method: "PUT",
  });
  const res2 = await res.json();
  return res2;
}

let box = document.querySelector(".postbox");

if (box) {
  box.addEventListener("click", (e) => {
    if (e.target.classList.contains("deletePost")) {
      const postId = e.target.dataset.post;
      DeletePost(postId)
        .then((data) => {
          showAlert(data.message);
        })
        .catch((err) => console.log(err));
    } else if (e.target.classList.contains("archivePost")) {
      const postId = e.target.dataset.post;
      ArchivePost(postId)
        .then((data) => showAlert(data.message))
        .catch((err) => console.log(err));
    } else if (e.target.classList.contains("unarchivePost")) {
      const postId = e.target.dataset.post;
      UnArchivePost(postId)
        .then((data) => showAlert(data.message))
        .catch((err) => console.log(err));
    }
  });
}

function showAlert(msg) {
  Swal.fire({
    position: "top-end",
    icon: "success",
    title: msg,
    fontSize: 10,
    showConfirmButton: false,
    timer: 1700,
  });
  setTimeout(() => {
    window.location.reload();
  }, 1000);
}
