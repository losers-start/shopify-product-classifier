async function approveResult(id) {
  const r = await fetch(`/api/classifications/${id}/approve/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ reviewer: "interviewer" }),
  });
  if (r.ok) location.reload();
  else alert("Approval failed");
}
function getCookie(n) {
  const v = `; ${document.cookie}`;
  const p = v.split(`; ${n}=`);
  return p.length === 2 ? p.pop().split(";").shift() : "";
}
