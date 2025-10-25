<script>
  window.addEventListener("scroll", function() {
    const nav = document.querySelector("nav");
    if (window.scrollY > 10) {
      nav.classList.add("shadow-md");
    } else {
      nav.classList.remove("shadow-md");
    }
  });
</script>