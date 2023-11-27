const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');
const menuIcons = document.querySelectorAll('.navbar__icons')
const navLogo = document.querySelector('#navbar__logo');
const nav = document.querySelector('.navbar');


// Display Mobile Menu
const mobileMenu = () => {
  menu.classList.toggle('is-active');
  nav.classList.add('active');
  menuLinks.classList.toggle('active');
};

const navbarblack = () => {
  if (mobileMenu){
    nav.classList.add('active');
  } else {
    nav.classList.remove('active');
  }
};

menu.addEventListener('click', mobileMenu, navbarblack);

//  Close mobile Menu when clicking on a menu item
const hideMobileMenu = () => {
  const menuBars = document.querySelector('.is-active');
  if (window.innerWidth <= 768 && menuBars) {
    menu.classList.toggle('is-active');
    menuLinks.classList.remove('active');
  }
};

function makeinvisible(navbar){
  var element=document.getElementsByClassName('navbar')
  if (menuBars)
   try { 
     element.classList.remove(".navbar");
     } catch (ex){}
     element.classList.add(".navbar.active");
};

// Hides navbar when scrolling down and makes it reappear when scrolling up
var prev = window.pageYOffset;
window.onscroll = function() {
    var current = window.pageYOffset;
    if (prev > current){
        document.getElementById("nav").style.top = "0";
    } else {
        document.getElementById("nav").style.top = "-80px";
    }
    prev = current
};

function validerForm() {
  const form = document.forms["iform"]
  let nomJeu = form["nomJeu"].value;
  console.log("nomJeu : "+nomJeu)
  let description = form["description"].value;
  console.log("description : "+description)
  let prix = form["prix"].value;
  console.log("prix : "+prix)
  let uScore = form["uScore"].value;
  console.log("uScore : "+uScore)
  let date = form["date"].value;
  console.log("date : "+date)
  let image = form["image"].value;
  console.log("image : "+image)
  let achievements = form["achievements"].value;
  console.log("achievements : "+achievements)
  let nomDev = form["nomDev"].value;
  console.log("nomDev : "+nomDev)
  let nomEditeur = form["nomEditeur"].value;
  console.log("nomEditeur : "+nomEditeur)
  let win = form["win"].checked;
  let mac = form["mac"].checked;
  let lnx = form["lnx"].checked;
  console.log("win : "+win)
  console.log("mac : "+mac)
  console.log("lnx : "+lnx)
  let bien = true
  if (nomJeu === "") {
    alert("Insérer un titre pour le jeu");
    document.getElementById("nomJeu").style.backgroundColor = "#FFE1DA"
    if (bien === true) {bien = false}
  }
  if (description === "") {
      alert("Insérer une description pour le jeu");
      document.getElementById("description").style.backgroundColor = "#FFE1DA"
      if (bien === true) {bien = false}
  }
  if (prix === '' || Number.isNaN(Number(prix))) {
      alert("Insérer le prix du jeu");
      document.getElementById("prix").style.backgroundColor = "#FFE1DA"
      if (bien === true) {bien = false}
  }
  if (uScore === '' || Number.isNaN(Number(uScore)) || Number(uScore)<0 || Number(uScore)>100) {
      alert("Insérer le score du jeu, il doit être entre 0 et 100");
      document.getElementById("uScore").style.backgroundColor = "#FFE1DA"
      if (bien === true) {bien = false}
  }
  if (date === "") {
      alert("Insérer la date de sortie du jeu");
      document.getElementById("date").style.backgroundColor = "#FFE1DA"
      if (bien === true) {bien = false}
  }
  if (image === "") {
    alert("Insérer le lien vers l'image du jeu");
    document.getElementById("image").style.backgroundColor = "#FFE1DA"
    if (bien === true) {bien = false}
  }
  if (achievements === '') {
    alert("Insérer le nombre de succès");
    document.getElementById("achievements").style.backgroundColor = "#FFE1DA"
    if (bien === true) {bien = false}
  }
  if (nomDev === "") {
    alert("Insérer le nom du développeur");
    document.getElementById("nomDev").style.backgroundColor = "#FFE1DA"
    if (bien === true) {bien = false}
  }
  if (win === false && mac === false && lnx === false) {
    alert("Sélectionner les platformes");
    if (bien === true) {bien = false}
  }
  if (bien) {
    console.log("Bravo le formulaire est bien rempli")
  }

  fetch("/insertion", {
    method: "POST",
    body: JSON.stringify({
      "nomJeu": nomJeu,
      "description": description,
      "prix": Number(prix),
      "uScore": Number(uScore),
      "date": date,
      "image": image,
      "achievements": Number(achievements),
      "nomDev": nomDev,
      "nomEditeur": nomEditeur,
      "win": win,
      "mac": mac,
      "lnx": lnx
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then(response => response.text()).then(id => {window.location.href = "/jeu/"+id})
}
