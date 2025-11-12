<script>
  document.addEventListener("DOMContentLoaded", function () {
    const nav = document.querySelector("nav");
    if (!nav) return;

    window.addEventListener("scroll", () => {
      nav.classList.toggle("shadow-md", window.scrollY > 10);
    });
  });
</script>