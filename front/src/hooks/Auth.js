export function signOut() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/";
}
