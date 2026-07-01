const API = "/courses";

const els = {
  apiStatus: document.getElementById("api-status"),
  coursesBody: document.getElementById("courses-body"),
  detailContent: document.getElementById("detail-content"),
  search: document.getElementById("search"),
  addModal: document.getElementById("add-modal"),
  addForm: document.getElementById("add-form"),
  formError: document.getElementById("form-error"),
  toast: document.getElementById("toast"),
  statTotal: document.getElementById("stat-total"),
  statCapacity: document.getElementById("stat-capacity"),
  statEnrolled: document.getElementById("stat-enrolled"),
  statAvailable: document.getElementById("stat-available"),
};

let courses = [];
let selectedId = null;

function showToast(message) {
  els.toast.textContent = message;
  els.toast.hidden = false;
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => {
    els.toast.hidden = true;
  }, 2800);
}

function setApiStatus(state, text) {
  els.apiStatus.className = `badge badge--${state}`;
  els.apiStatus.textContent = text;
}

function statusFor(course) {
  const ratio = course.enrollment_count / course.capacity;
  if (ratio >= 1) return { label: "تکمیل ظرفیت", className: "status-pill--full" };
  if (ratio >= 0.75) return { label: "نزدیک به تکمیل", className: "status-pill--busy" };
  return { label: "قابل ثبت‌نام", className: "status-pill--open" };
}

function updateStats(list) {
  const totalCapacity = list.reduce((sum, c) => sum + c.capacity, 0);
  const totalEnrolled = list.reduce((sum, c) => sum + c.enrollment_count, 0);

  els.statTotal.textContent = list.length;
  els.statCapacity.textContent = totalCapacity;
  els.statEnrolled.textContent = totalEnrolled;
  els.statAvailable.textContent = Math.max(totalCapacity - totalEnrolled, 0);
}

function renderDetail(course) {
  if (!course) {
    els.detailContent.className = "detail detail--empty";
    els.detailContent.innerHTML = `
      <div class="detail__placeholder">
        <span>📋</span>
        <p>یک درس از جدول انتخاب کنید تا جزئیات نمایش داده شود.</p>
      </div>`;
    return;
  }

  const status = statusFor(course);
  const percent = Math.min((course.enrollment_count / course.capacity) * 100, 100);

  els.detailContent.className = "detail";
  els.detailContent.innerHTML = `
    <div class="detail-card">
      <h3>${course.title}</h3>
      <div class="detail-row"><strong>شناسه</strong><span>${course.id}</span></div>
      <div class="detail-row"><strong>کد درس</strong><span>${course.code}</span></div>
      <div class="detail-row"><strong>استاد</strong><span>${course.professor_id || "تعیین نشده"}</span></div>
      <div class="detail-row"><strong>ظرفیت</strong><span>${course.capacity} نفر</span></div>
      <div class="detail-row"><strong>ثبت‌نام‌شده</strong><span>${course.enrollment_count} نفر</span></div>
      <div class="detail-row"><strong>وضعیت</strong><span class="status-pill ${status.className}">${status.label}</span></div>
      <div>
        <strong>پر شدگی کلاس</strong>
        <div class="progress"><div class="progress__bar" style="width:${percent}%"></div></div>
      </div>
    </div>`;
}

function renderTable(list) {
  if (!list.length) {
    els.coursesBody.innerHTML = `<tr><td colspan="6" class="empty">هنوز درسی ثبت نشده است.</td></tr>`;
    renderDetail(null);
    return;
  }

  els.coursesBody.innerHTML = list
    .map((course) => {
      const status = statusFor(course);
      const selected = course.id === selectedId ? "is-selected" : "";
      return `
        <tr class="${selected}" data-id="${course.id}">
          <td><strong>${course.code}</strong></td>
          <td>${course.title}</td>
          <td>${course.capacity}</td>
          <td>${course.enrollment_count}</td>
          <td><span class="status-pill ${status.className}">${status.label}</span></td>
          <td><button class="link-btn" data-action="view" data-id="${course.id}">مشاهده</button></td>
        </tr>`;
    })
    .join("");

  const selected = list.find((c) => c.id === selectedId) || list[0];
  selectedId = selected.id;
  renderDetail(selected);
}

function applySearch() {
  const q = els.search.value.trim().toLowerCase();
  const filtered = courses.filter(
    (c) => c.code.toLowerCase().includes(q) || c.title.toLowerCase().includes(q)
  );
  renderTable(filtered);
  updateStats(filtered);
}

async function loadCourses() {
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error("خطا در دریافت لیست دروس");
    courses = await res.json();
    setApiStatus("ok", "API متصل است");
    applySearch();
  } catch (err) {
    setApiStatus("error", "خطا در اتصال API");
    els.coursesBody.innerHTML = `<tr><td colspan="6" class="empty">${err.message}</td></tr>`;
  }
}

async function selectCourse(courseId) {
  selectedId = courseId;
  try {
    const res = await fetch(`${API}/${courseId}`);
    if (!res.ok) throw new Error("درس پیدا نشد");
    const course = await res.json();
    renderDetail(course);
    document.querySelectorAll("#courses-body tr").forEach((row) => {
      row.classList.toggle("is-selected", row.dataset.id === courseId);
    });
  } catch (err) {
    showToast(err.message);
  }
}

async function addCourse(formData) {
  const payload = {
    id: formData.get("id").trim(),
    code: formData.get("code").trim(),
    title: formData.get("title").trim(),
    capacity: Number(formData.get("capacity")),
    professor_id: formData.get("professor_id").trim() || null,
  };

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "خطا در افزودن درس");
  }
  return data;
}

document.getElementById("btn-refresh").addEventListener("click", loadCourses);
document.getElementById("btn-add").addEventListener("click", () => els.addModal.showModal());
document.getElementById("btn-close-modal").addEventListener("click", () => els.addModal.close());
document.getElementById("btn-cancel").addEventListener("click", () => els.addModal.close());
els.search.addEventListener("input", applySearch);

els.coursesBody.addEventListener("click", (event) => {
  const row = event.target.closest("tr[data-id]");
  if (!row) return;
  selectCourse(row.dataset.id);
});

els.addForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  els.formError.hidden = true;

  try {
    const created = await addCourse(new FormData(els.addForm));
    els.addForm.reset();
    els.addModal.close();
    showToast(`درس «${created.title}» با موفقیت اضافه شد`);
    await loadCourses();
    selectedId = created.id;
    await selectCourse(created.id);
  } catch (err) {
    els.formError.textContent = err.message;
    els.formError.hidden = false;
  }
});

loadCourses();
