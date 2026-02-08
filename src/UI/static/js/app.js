/**
 * StudyMate - Main Application JavaScript
 */

// ============== Navigation ==============

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initModals();
    initTabs();
    loadDashboardData();
    loadCoursesData();
    loadPlansData();
    setTodayDate();
});

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const viewId = item.dataset.view;

            // Update nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update views
            views.forEach(view => view.classList.remove('active'));
            document.getElementById(`${viewId}-view`).classList.add('active');
        });
    });
}

// ============== Modals ==============

function initModals() {
    const courseModal = document.getElementById('course-modal');
    const btnNewCourse = document.getElementById('btn-new-course');
    const modalCloseButtons = document.querySelectorAll('.modal-close');

    if (btnNewCourse) {
        btnNewCourse.addEventListener('click', () => {
            courseModal.classList.remove('hidden');
        });
    }

    modalCloseButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.classList.add('hidden');
            });
        });
    });

    // Close modal on backdrop click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    });
}

// ============== Tabs ==============

function initTabs() {
    const tabGroups = document.querySelectorAll('.tab-group');

    tabGroups.forEach(group => {
        const tabs = group.querySelectorAll('.tab');
        const parent = group.closest('.modal-body') || group.parentElement;
        const contents = parent.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.dataset.tab;

                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                contents.forEach(content => {
                    content.classList.remove('active');
                    if (content.id === `tab-${tabId}`) {
                        content.classList.add('active');
                    }
                });
            });
        });
    });
}

// ============== Dashboard ==============

function setTodayDate() {
    const dateEl = document.getElementById('today-date');
    if (dateEl) {
        const today = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateEl.textContent = today.toLocaleDateString('en-US', options);
    }
}

async function loadDashboardData() {
    try {
        // Load stats
        const statsResponse = await fetch('/api/stats');
        const statsData = await statsResponse.json();

        document.getElementById('stat-plans').textContent = statsData.active_plans;



        // Render upcoming deadlines
        renderDeadlines(statsData.upcoming_deadlines);

        // Load agenda
        const agendaResponse = await fetch('/api/agenda');
        const agendaData = await agendaResponse.json();

        renderAgenda(agendaData.items);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function renderDeadlines(deadlines) {
    const deadlineList = document.getElementById('deadline-list');
    if (!deadlineList) return;

    deadlineList.innerHTML = deadlines.slice(0, 3).map(d => {
        const urgencyClass = d.days <= 7 ? 'urgent' : d.days <= 14 ? 'warning' : '';
        return `
            <div class="deadline-item ${urgencyClass}">
                <span class="deadline-course">${d.course}</span>
                <span class="deadline-hours">${d.hours_left}h</span>
                <span class="deadline-days">${d.days}d</span>
            </div>
        `;
    }).join('');
}

function renderAgenda(items) {
    const agendaList = document.getElementById('agenda-list');
    if (!agendaList) return;

    agendaList.innerHTML = items.map(item => {
        const escapedTitle = item.title.replace(/'/g, "\\'");
        return `
        <div class="agenda-item ${item.completed ? 'completed' : ''}" data-id="${item.id}">
            <div class="agenda-checkbox ${item.completed ? 'checked' : ''}" onclick="toggleAgendaItem(${item.id}, ${item.estimated_minutes}, '${escapedTitle}')"></div>
            <div class="agenda-info">
                <div class="agenda-title">${item.title}</div>
                <div class="agenda-course">${item.course}</div>
            </div>
            <div class="agenda-time">${item.estimated_minutes} min</div>
        </div>
    `}).join('');
}

function toggleAgendaItem(id, estimatedMinutes, title) {
    const item = document.querySelector(`.agenda-item[data-id="${id}"]`);
    const checkbox = item.querySelector('.agenda-checkbox');

    // If uncompleting, just toggle without modal
    if (item.classList.contains('completed')) {
        item.classList.remove('completed');
        checkbox.classList.remove('checked');
        return;
    }

    // Show time input modal
    showTimeModal(id, estimatedMinutes, title);
}

function showTimeModal(taskId, estimatedMinutes, title) {
    const modal = document.getElementById('time-modal');
    const taskLabel = document.getElementById('time-modal-task');
    const input = document.getElementById('actual-time-input');
    const display = document.getElementById('actual-time-display');
    const hint = document.getElementById('time-estimate-hint');

    // Round estimated to nearest 15 min (minimum 15)
    const rounded = Math.max(15, Math.round(estimatedMinutes / 15) * 15);

    taskLabel.textContent = title;
    hint.textContent = `Estimated: ${estimatedMinutes} minutes`;
    input.value = rounded;
    input.dataset.taskId = taskId;
    display.textContent = `${rounded} min`;

    modal.classList.remove('hidden');
}

function adjustTime(delta) {
    const input = document.getElementById('actual-time-input');
    const display = document.getElementById('actual-time-display');
    let value = parseInt(input.value) + delta;
    if (value < 15) value = 15;
    input.value = value;
    display.textContent = `${value} min`;
}

function saveActualTime() {
    const input = document.getElementById('actual-time-input');
    const taskId = input.dataset.taskId;
    const actualMinutes = parseInt(input.value) || 0;

    // Mark task as completed
    const item = document.querySelector(`.agenda-item[data-id="${taskId}"]`);
    const checkbox = item.querySelector('.agenda-checkbox');
    item.classList.add('completed');
    checkbox.classList.add('checked');

    // Update the displayed time to show actual
    const timeEl = item.querySelector('.agenda-time');
    timeEl.textContent = `${actualMinutes} min`;
    timeEl.classList.add('actual');

    // Close modal
    document.getElementById('time-modal').classList.add('hidden');

    // TODO: Send update to backend with actualMinutes
    console.log(`Task ${taskId} completed in ${actualMinutes} minutes`);
}

// Initialize time modal events
document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('btn-save-time');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveActualTime);
    }

    // Allow Enter key to save
    const timeInput = document.getElementById('actual-time-input');
    if (timeInput) {
        timeInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') saveActualTime();
        });
    }
});

// ============== Courses ==============

async function loadCoursesData() {
    try {
        const response = await fetch('/api/courses');
        const data = await response.json();

        renderCourses(data.courses);
    } catch (error) {
        console.error('Error loading courses:', error);
    }
}

function renderCourses(courses) {
    const courseList = document.getElementById('course-list');
    if (!courseList) return;

    courseList.innerHTML = courses.map(course => `
        <div class="course-card" data-id="${course.id}">
            <div class="course-name">${course.name}</div>
            <div class="course-meta">
                <span>📖 ${course.units} units</span>
                <span>📅 ${course.plans} plan${course.plans !== 1 ? 's' : ''}</span>
            </div>
        </div>
    `).join('');
}

// ============== Plans ==============

async function loadPlansData() {
    try {
        const response = await fetch('/api/plans');
        const data = await response.json();

        renderPlans(data.plans);
    } catch (error) {
        console.error('Error loading plans:', error);
    }
}

function renderPlans(plans) {
    const plansList = document.getElementById('plans-list');
    if (!plansList) return;

    plansList.innerHTML = plans.map(plan => `
        <div class="plan-card" data-id="${plan.id}">
            <div class="plan-info">
                <div class="plan-name">${plan.course}</div>
                <div class="plan-due">Due: ${formatDate(plan.due_date)}</div>
            </div>
            <div class="plan-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${plan.progress}%"></div>
                </div>
                <div class="progress-text">${plan.progress}% complete</div>
            </div>
            <span class="plan-status ${plan.status}">${formatStatus(plan.status)}</span>
        </div>
    `).join('');
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatStatus(status) {
    const labels = {
        'on_track': 'On Track',
        'ahead': 'Ahead',
        'behind': 'Behind'
    };
    return labels[status] || status;
}

// ============== Calendar Week Navigation ==============

let currentWeekStart = getMonday(new Date());
let selectedDate = new Date();
selectedDate.setHours(0, 0, 0, 0);

// Mock detailed tasks data (with id, title, course, estimated_minutes, completed)
const allTasksData = {};

function generateMockTasks(date) {
    const key = date.toISOString().split('T')[0];
    if (allTasksData[key]) return allTasksData[key];

    const dayOfWeek = date.getDay();
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

    if (isWeekend) {
        allTasksData[key] = [];
        return [];
    }

    // Generate 1-3 random tasks for weekdays
    const taskCount = Math.floor(Math.random() * 3) + 1;
    const courses = ['Mathematics', 'Biology 101', 'Physics', 'History'];
    const titles = ['Chapter Review', 'Practice Problems', 'Quiz Prep', 'Reading Assignment', 'Lab Report'];

    const tasks = [];
    for (let i = 0; i < taskCount; i++) {
        tasks.push({
            id: `${key}-${i}`,
            title: titles[Math.floor(Math.random() * titles.length)] + ` ${Math.floor(Math.random() * 10) + 1}`,
            course: courses[Math.floor(Math.random() * courses.length)],
            estimated_minutes: [30, 45, 60, 90][Math.floor(Math.random() * 4)],
            completed: false
        });
    }
    allTasksData[key] = tasks;
    return tasks;
}

function getMonday(d) {
    const date = new Date(d);
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(date.setDate(diff));
}

function changeWeek(delta) {
    currentWeekStart.setDate(currentWeekStart.getDate() + (delta * 7));
    renderCalendar();
}

function selectDay(dateStr) {
    selectedDate = new Date(dateStr);
    selectedDate.setHours(0, 0, 0, 0);

    // Update selected state in calendar
    document.querySelectorAll('.calendar-day').forEach(el => {
        el.classList.remove('selected');
    });
    document.querySelector(`.calendar-day[data-date="${dateStr}"]`)?.classList.add('selected');

    renderDayAgenda();
}

function renderDayAgenda() {
    const panel = document.getElementById('day-agenda-panel');
    const titleEl = document.getElementById('day-agenda-title');
    const dateEl = document.getElementById('day-agenda-date');
    const listEl = document.getElementById('day-agenda-list');
    if (!panel || !listEl) return;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const isToday = selectedDate.getTime() === today.getTime();
    titleEl.textContent = isToday ? "Today's Tasks" : selectedDate.toLocaleDateString('en-US', { weekday: 'long' }) + "'s Tasks";
    dateEl.textContent = selectedDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    const tasks = generateMockTasks(selectedDate);

    if (tasks.length === 0) {
        listEl.innerHTML = '<div class="no-tasks">No tasks scheduled</div>';
        return;
    }


    const isPast = selectedDate.getTime() < today.getTime();

    listEl.innerHTML = tasks.map(task => {
        const escapedTitle = task.title.replace(/'/g, "\\'");
        const checkboxClick = isPast ? '' : `onclick="toggleDayTask('${task.id}', ${task.estimated_minutes}, '${escapedTitle}')"`;
        const disabledClass = isPast ? 'disabled' : '';
        return `
            <div class="agenda-item ${task.completed ? 'completed' : ''} ${disabledClass}" data-id="${task.id}">
                <div class="agenda-checkbox ${task.completed ? 'checked' : ''} ${disabledClass}" 
                     ${checkboxClick}></div>
                <div class="agenda-info">
                    <div class="agenda-title">${task.title}</div>
                    <div class="agenda-course">${task.course}</div>
                </div>
                <div class="agenda-time ${task.completed ? 'actual' : ''}">${task.estimated_minutes} min</div>
            </div>
        `;
    }).join('');
}

function toggleDayTask(taskId, estimatedMinutes, title) {
    const dateKey = selectedDate.toISOString().split('T')[0];
    const tasks = allTasksData[dateKey] || [];
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    const item = document.querySelector(`.day-agenda-panel .agenda-item[data-id="${taskId}"]`);
    const checkbox = item?.querySelector('.agenda-checkbox');

    if (task.completed) {
        // Uncomplete
        task.completed = false;
        item?.classList.remove('completed');
        checkbox?.classList.remove('checked');
        const timeEl = item?.querySelector('.agenda-time');
        if (timeEl) {
            timeEl.textContent = `${task.estimated_minutes} min`;
            timeEl.classList.remove('actual');
        }
    } else {
        // Show time modal
        showTimeModalForDay(taskId, estimatedMinutes, title);
    }

    // Re-render calendar to update mini-task counts
    renderCalendar();
}

function showTimeModalForDay(taskId, estimatedMinutes, title) {
    const modal = document.getElementById('time-modal');
    const taskLabel = document.getElementById('time-modal-task');
    const input = document.getElementById('actual-time-input');
    const display = document.getElementById('actual-time-display');
    const hint = document.getElementById('time-estimate-hint');

    const rounded = Math.max(15, Math.round(estimatedMinutes / 15) * 15);

    taskLabel.textContent = title;
    hint.textContent = `Estimated: ${estimatedMinutes} minutes`;
    input.value = rounded;
    input.dataset.taskId = taskId;
    input.dataset.source = 'dayAgenda';
    display.textContent = `${rounded} min`;

    modal.classList.remove('hidden');
}

// Override saveActualTime to handle both dashboard and day agenda
const originalSaveActualTime = typeof saveActualTime !== 'undefined' ? saveActualTime : null;

function saveActualTime() {
    const input = document.getElementById('actual-time-input');
    const taskId = input.dataset.taskId;
    const actualMinutes = parseInt(input.value) || 0;
    const source = input.dataset.source;

    if (source === 'dayAgenda') {
        // Day agenda mode
        const dateKey = selectedDate.toISOString().split('T')[0];
        const tasks = allTasksData[dateKey] || [];
        const task = tasks.find(t => t.id === taskId);
        if (task) {
            task.completed = true;
            task.actual_minutes = actualMinutes;
        }

        const item = document.querySelector(`.day-agenda-panel .agenda-item[data-id="${taskId}"]`);
        if (item) {
            item.classList.add('completed');
            item.querySelector('.agenda-checkbox')?.classList.add('checked');
            const timeEl = item.querySelector('.agenda-time');
            if (timeEl) {
                timeEl.textContent = `${actualMinutes} min`;
                timeEl.classList.add('actual');
            }
        }

        renderCalendar();
    } else {
        // Dashboard mode
        const item = document.querySelector(`.agenda-item[data-id="${taskId}"]`);
        const checkbox = item?.querySelector('.agenda-checkbox');
        item?.classList.add('completed');
        checkbox?.classList.add('checked');

        const timeEl = item?.querySelector('.agenda-time');
        if (timeEl) {
            timeEl.textContent = `${actualMinutes} min`;
            timeEl.classList.add('actual');
        }
    }

    document.getElementById('time-modal').classList.add('hidden');
    console.log(`Task ${taskId} completed in ${actualMinutes} minutes`);
}

function renderCalendar() {
    const grid = document.getElementById('calendar-grid');
    const rangeEl = document.getElementById('week-range');
    if (!grid) return;

    const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let html = '';
    for (let i = 0; i < 7; i++) {
        const day = new Date(currentWeekStart);
        day.setDate(day.getDate() + i);
        day.setHours(0, 0, 0, 0);
        const dateStr = day.toISOString().split('T')[0];

        const isToday = day.getTime() === today.getTime();
        const isSelected = day.getTime() === selectedDate.getTime();
        const isRest = i >= 5;

        let classes = 'calendar-day';
        if (isToday) classes += ' today';
        if (isSelected) classes += ' selected';
        if (isRest) classes += ' rest';

        const tasks = generateMockTasks(day);
        const incompleteTasks = tasks.filter(t => !t.completed);
        const tasksHtml = isRest && tasks.length === 0
            ? '<div class="rest-label">Rest Day</div>'
            : incompleteTasks.map(t => `<div class="mini-task">${t.title.split(' ')[0]}</div>`).join('');

        html += `
            <div class="${classes}" data-date="${dateStr}" onclick="selectDay('${dateStr}')">
                <span class="day-name">${dayNames[i]}</span>
                <span class="day-date">${day.getDate()}</span>
                <div class="day-tasks">${tasksHtml}</div>
            </div>
        `;
    }

    grid.innerHTML = html;

    // Update week range display
    const endDate = new Date(currentWeekStart);
    endDate.setDate(endDate.getDate() + 6);
    const opts = { month: 'short', day: 'numeric' };
    const yearOpts = { month: 'short', day: 'numeric', year: 'numeric' };
    if (rangeEl) {
        rangeEl.textContent = `${currentWeekStart.toLocaleDateString('en-US', opts)} - ${endDate.toLocaleDateString('en-US', yearOpts)}`;
    }
}

// Swipe support for calendar
function initCalendarSwipe() {
    const wrapper = document.getElementById('calendar-wrapper');
    if (!wrapper) return;

    let startX = 0;
    let startY = 0;

    wrapper.addEventListener('touchstart', e => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });

    wrapper.addEventListener('touchend', e => {
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;
        const diffX = endX - startX;
        const diffY = endY - startY;

        // Horizontal swipe detected (more horizontal than vertical)
        if (Math.abs(diffX) > 50 && Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX > 0) {
                changeWeek(-1); // Swipe right = previous week
            } else {
                changeWeek(1);  // Swipe left = next week
            }
        }
    });
}

// Initialize calendar on page load
document.addEventListener('DOMContentLoaded', () => {
    renderCalendar();
    renderDayAgenda(); // Show today's agenda by default
    initCalendarSwipe();
});

// ============== Settings ==============

// Weekly availability stored as {h: hours, m: minutes}
const weeklyTime = {
    mon: { h: 2, m: 0 }, tue: { h: 2, m: 0 }, wed: { h: 2, m: 0 },
    thu: { h: 2, m: 0 }, fri: { h: 1, m: 30 }, sat: { h: 0, m: 0 }, sun: { h: 0, m: 0 }
};

function adjustDial(day, type, delta) {
    const time = weeklyTime[day];

    if (type === 'h') {
        // Adjust hours directly
        time.h += delta;
        if (time.h < 0) time.h = 0;
        if (time.h > 12) time.h = 12;
    } else {
        // Adjust minutes with rollover to hours
        time.m += delta;
        if (time.m >= 60) {
            time.m = 0;
            time.h++;
            if (time.h > 12) time.h = 12;
        } else if (time.m < 0) {
            if (time.h > 0) {
                time.m = 45;
                time.h--;
            } else {
                time.m = 0;
            }
        }
    }

    // Update displays
    document.getElementById(`${day}-h`).textContent = time.h;
    document.getElementById(`${day}-m`).textContent = time.m.toString().padStart(2, '0');

    updateTotalHours();
}

function updateTotalHours() {
    let totalMinutes = 0;
    for (const day in weeklyTime) {
        totalMinutes += weeklyTime[day].h * 60 + weeklyTime[day].m;
    }
    const h = Math.floor(totalMinutes / 60);
    const m = totalMinutes % 60;
    document.getElementById('total-hours').textContent = `${h}:${m.toString().padStart(2, '0')}`;
}

// Rating buttons
document.querySelectorAll('.rating-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const group = e.target.closest('.rating-group');
        group.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});
