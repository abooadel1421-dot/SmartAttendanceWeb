// static/js/reports_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    setupReportButtons();
    setupExportOptions();
    addAnimations();
}

/**
 * إعداد أزرار التقارير
 */
function setupReportButtons() {
    const reportButtons = document.querySelectorAll('.btn-report');
    reportButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href) {
                showLoadingIndicator();
                setTimeout(() => {
                    window.location.href = href;
                }, 500);
            }
        });
    });
}

/**
 * إعداد خيارات التصدير
 */
function setupExportOptions() {
    // بحث عن أزرار التصدير
    const exportButtons = document.querySelectorAll('[data-export-type]');
    
    exportButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const exportType = this.getAttribute('data-export-type');
            exportAttendanceReport(exportType);
        });
    });
}

/**
 * استخراج تقرير الحضور (Excel أو CSV أو PDF)
 */
function exportAttendanceReport(format) {
    showLoadingIndicator();
    
    const data = {
        format: format,
        date_from: document.getElementById('dateFrom')?.value || '',
        date_to: document.getElementById('dateTo')?.value || '',
        student_id: document.getElementById('studentFilter')?.value || '',
        device_id: document.getElementById('deviceFilter')?.value || ''
    };

    // إنشاء form مخفي للتصدير
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/admin/api/export-attendance-report';
    form.style.display = 'none';

    Object.keys(data).forEach(key => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = data[key];
        form.appendChild(input);
    });

    document.body.appendChild(form);
    
    // إضافة token CSRF إن وجد
    const csrfToken = document.querySelector('[name="csrf_token"]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrf_token';
        csrfInput.value = csrfToken.value;
        form.appendChild(csrfInput);
    }

    form.submit();
    document.body.removeChild(form);

    setTimeout(() => {
        hideLoadingIndicator();
        showAlert('success', 'تم استخراج التقرير بنجاح!');
    }, 1000);
}

/**
 * استخراج إلى Excel
 */
function exportToExcel() {
    exportAttendanceReport('excel');
}

/**
 * استخراج إلى CSV
 */
function exportToCSV() {
    exportAttendanceReport('csv');
}

/**
 * استخراج إلى PDF
 */
function exportToPDF() {
    exportAttendanceReport('pdf');
}

/**
 * عرض مؤشر التحميل
 */
function showLoadingIndicator() {
    let loader = document.getElementById('loadingIndicator');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loadingIndicator';
        loader.className = 'loading-spinner active';
        loader.innerHTML = '<div class="spinner"></div><p class="mt-3">جاري التحميل...</p>';
        document.body.appendChild(loader);
    } else {
        loader.classList.add('active');
    }
}

/**
 * إخفاء مؤشر التحميل
 */
function hideLoadingIndicator() {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.classList.remove('active');
    }
}

/**
 * عرض رسالة تنبيه
 */
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
    alertDiv.role = 'alert';
    
    const iconMap = {
        'success': 'fas fa-check-circle',
        'danger': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    };

    alertDiv.innerHTML = `
        <i class="${iconMap[type]}"></i>
        <span>${message}</span>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    document.body.insertBefore(alertDiv, document.body.firstChild);

    // إزالة تلقائية بعد 5 ثواني
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * إضافة تأثيرات الحركة
 */
function addAnimations() {
    const cards = document.querySelectorAll('.report-card');
    
    cards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease ${index * 0.1}s both`;
    });

    // تأثير عند تحريك الماوس
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * فتح مودال التقارير المتقدمة
 */
function openAdvancedReports() {
    const modal = new bootstrap.Modal(document.getElementById('advancedReportsModal'));
    modal.show();
}

/**
 * إنشاء تقرير مخصص
 */
function generateCustomReport() {
    const dateFrom = document.getElementById('dateFrom')?.value;
    const dateTo = document.getElementById('dateTo')?.value;
    const studentId = document.getElementById('studentFilter')?.value;
    const deviceId = document.getElementById('deviceFilter')?.value;

    if (!dateFrom || !dateTo) {
        showAlert('warning', 'يرجى تحديد فترة زمنية!');
        return;
    }

    showLoadingIndicator();

    fetch('/admin/api/generate-custom-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            date_from: dateFrom,
            date_to: dateTo,
            student_id: studentId,
            device_id: deviceId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingIndicator();
        if (data.success) {
            showAlert('success', 'تم إنشاء التقرير بنجاح!');
            // يمكنك إضافة عرض التقرير هنا
        } else {
            showAlert('danger', data.message || 'حدث خطأ في إنشاء التقرير');
        }
    })
    .catch(error => {
        hideLoadingIndicator();
        showAlert('danger', 'خطأ في الاتصال بالخادم');
        console.error('Error:', error);
    });
}

/**
 * تحميل إحصائيات اليوم
 */
function loadTodayStatistics() {
    fetch('/admin/api/today-statistics')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // تحديث الإحصائيات على الصفحة
                const statsContainer = document.getElementById('todayStats');
                if (statsContainer) {
                    statsContainer.innerHTML = `
                        <p><strong>إجمالي الطلاب الحاضرين:</strong> ${data.present_count}</p>
                        <p><strong>إجمالي الطلاب الغائبين:</strong> ${data.absent_count}</p>
                        <p><strong>إجمالي السجلات:</strong> ${data.total_logs}</p>
                    `;
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

// تحميل الإحصائيات عند فتح الصفحة
loadTodayStatistics();