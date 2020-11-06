let imgFile = document.getElementById("imagepost");
let buttonUp = document.getElementById("imagepostbutton");

buttonUp.addEventListener("click", () => {
  const image = new FormData();
  image.append("file", imgFile.files[0]);
  imageHandler(image);
});

function imageHandler(image) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/uploads", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      var res = JSON.parse(this.responseText);
      if (res.status) {
        addToEditor(res.imageLink);
      } else {
        alert(res.message);
      }
    }
  };
  xhr.send(image);
}
const renderHtml = () => {
  preview.innerHTML = md.render(body.value);
};
let md = new markdownit();
let preview = document.querySelector(".preview");
// var result = md.render("# markdown-it rulezz!");
let body = document.getElementById("body");
body.addEventListener("input", renderHtml);

renderHtml();

function addToEditor(msg) {
  let p = document.querySelector("#urlpost");
  msg = msg.replace(/\\/g, "/");
  body.value += `![Image alt text](${msg})`;
  renderHtml();
}
