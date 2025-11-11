// static/js/attendance_logs.js

/**
 * تهيئة الصفحة عند تحميل DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeAttendanceLogs();
});

/**
 * تهيئة جميع وظائف صفحة سجلات الحضور
 */
function initializeAttendanceLogs() {
    updateStats();
    addEventListeners();
    setupTableEnhancements();
    addDataLabelsForMobile();
}

/**
 * تحديث الإحصائيات
 */
function updateStats() {
    const table = document.getElementById('dataTable');
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');
    let totalAccess = 0;
    let totalDenied = 0;
    let totalRecords = rows.length;

    // تجاهل صف "لا توجد بيانات"
    if (totalRecords === 1 && rows[0].querySelector('td[colspan]')) {
        totalRecords = 0;
    } else {
        rows.forEach(row => {
            if (row.getAttribute('data-status') === 'granted') {
                totalAccess++;
            } else if (row.getAttribute('data-status') === 'denied') {
                totalDenied++;
            }
        });
    }

    // تحديث عناصر الإحصائيات
    document.getElementById('totalAccess').textContent = totalAccess;
    document.getElementById('totalDenied').textContent = totalDenied;
    document.getElementById('totalRecords').textContent = totalRecords;
    document.getElementById('recordCount').textContent = `${totalRecords} سجل`;
}

/**
 * إضافة مستمعات الأحداث
 */
function addEventListeners() {
    // مستمعات البحث والتصفية
    const filterStudent = document.getElementById('filterStudent');
    const filterStatus = document.getElementById('filterStatus');
    const filterDate = document.getElementById('filterDate');
    const filterDevice = document.getElementById('filterDevice');

    if (filterStudent) {
        filterStudent.addEventListener('keyup', debounce(applyFilters, 300));
    }

    if (filterStatus) {
        filterStatus.addEventListener('change', applyFilters);
    }

    if (filterDate) {
        filterDate.addEventListener('change', applyFilters);
    }

    if (filterDevice) {
        filterDevice.addEventListener('keyup', debounce(applyFilters, 300));
    }

    // إغلاق التنبيهات تلقائياً
    setupAlertDismiss();
}

/**
 * دالة debounce للحد من عدد استدعاءات الدالة
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * تطبيق التصفية
 */
function applyFilters() {
    const studentFilter = (document.getElementById('filterStudent')?.value || '').toLowerCase();
    const statusFilter = document.getElementById('filterStatus')?.value || '';
    const dateFilter = document.getElementById('filterDate')?.value || '';
    const deviceFilter = (document.getElementById('filterDevice')?.value || '').toLowerCase();

    const table = document.getElementById('dataTable');
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');
    let visibleCount = 0;

    rows.forEach(row => {
        // تجاهل صف "لا توجد بيانات"
        if (row.querySelector('td[colspan]')) {
            row.style.display = 'none';
            return;
        }

        const isVisible = shouldShowRow(row, studentFilter, statusFilter, dateFilter, deviceFilter);
        row.style.display = isVisible ? '' : 'none';
        row.style.animation = isVisible ? 'fadeIn 0.3s ease' : 'none';

        if (isVisible) visibleCount++;
    });

    // عرض رسالة عند عدم وجود نتائج
    showNoResultsMessage(table, visibleCount);
}

/**
 * التحقق من ظهور الصف بناءً على التصفية
 */
function shouldShowRow(row, studentFilter, statusFilter, dateFilter, deviceFilter) {
    // تصفية الطالب
    if (studentFilter) {
        const studentName = row.getAttribute('data-student')?.toLowerCase() || '';
        const studentId = row.querySelector('td:nth-child(3)')?.textContent.toLowerCase() || '';
        if (!studentName.includes(studentFilter) && !studentId.includes(studentFilter)) {
            return false;
        }
    }

    // تصفية الحالة
    if (statusFilter) {
        const rowStatus = row.getAttribute('data-status') || '';
        if (rowStatus !== statusFilter) {
            return false;
        }
    }

    // تصفية التاريخ
// تصفية التاريخ
if (dateFilter) {
    const timestamp = row.querySelector('td:nth-child(6)')?.textContent || '';
    const rowDate = timestamp.split(' ')[0]; // يفترض أن التاريخ هو أول جزء
    if (rowDate !== dateFilter) {
        return false;
    }
}

    // تصفية الجهاز
    if (deviceFilter) {
        const deviceName = row.getAttribute('data-device')?.toLowerCase() || '';
        if (!deviceName.includes(deviceFilter)) {
            return false;
        }
    }

    return true;
}

/**
 * عرض رسالة عند عدم وجود نتائج
 */
function showNoResultsMessage(table, visibleCount) {
    let noDataRow = table.querySelector('tr.no-data-row');

    if (visibleCount === 0) {
        if (!noDataRow) {
            noDataRow = document.createElement('tr');
            noDataRow.className = 'no-data-row';
            noDataRow.innerHTML = `
                <td colspan="7" class="text-center py-5">
                    <div class="no-data-message">
                        <i class="fas fa-search fa-3x text-muted mb-3"></i>
                        <p class="text-muted fs-6">لا توجد نتائج مطابقة للبحث</p>
                    </div>
                </td>
            `;
            table.querySelector('tbody').appendChild(noDataRow);
        }
        noDataRow.style.display = '';
    } else {
        if (noDataRow) {
            noDataRow.style.display = 'none';
        }
    }
}

/**
 * إعادة تعيين جميع التصفية
 */
function resetFilters() {
    document.getElementById('filterStudent').value = '';
    document.getElementById('filterStatus').value = '';
    document.getElementById('filterDate').value = '';
    document.getElementById('filterDevice').value = '';

    // إزالة صف عدم وجود نتائج
    const noDataRow = document.querySelector('tbody .no-data-row');
    if (noDataRow) {
        noDataRow.remove();
    }

    // إظهار جميع الصفوف
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        if (!row.querySelector('td[colspan]')) {
            row.style.display = '';
        }
    });

    updateStats();
}

/**
 * إعداد إغلاق التنبيهات تلقائياً
 */
function setupAlertDismiss() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            });
        }

        // إغلاق تلقائي بعد 5 ثواني
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
}

/**
 * تحسينات الجدول
 */
function setupTableEnhancements() {
    const table = document.getElementById('dataTable');
    if (!table) return;

    // إضافة رقم الصف الديناميكي
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
        if (!row.querySelector('td[colspan]')) {
            row.querySelector('td:first-child').textContent = index + 1;
        }
    });

    // إضافة تأثيرات التمرير
    addRowHoverEffects();
}

/**
 * إضافة تأثيرات التمرير على الصفوف
 */
function addRowHoverEffects() {
    const rows = document.querySelectorAll('.attendance-row');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
        });

        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

/**
 * تحميل البيانات كـ CSV أو PDF
 */
function exportTable() {
    const format = confirm('هل تريد تحميل البيانات كـ PDF؟\nاختر "إلغاء" لتحميل CSV');

    if (format) {
        exportToPDF();
    } else {
        exportToCSV();
    }
}

/**
 * تحميل الجدول كـ CSV
 */
function exportToCSV() {
    const table = document.getElementById('dataTable');
    if (!table) return;

    let csv = [];
    const headers = [];

    // الحصول على رؤوس الجدول
    table.querySelectorAll('thead th').forEach(header => {
        headers.push('"' + header.textContent.trim() + '"');
    });
    csv.push(headers.join(','));

    // الحصول على بيانات الصفوف
    table.querySelectorAll('tbody tr').forEach(row => {
        if (!row.querySelector('td[colspan]')) {
            const cells = [];
            row.querySelectorAll('td').forEach(cell => {
                cells.push('"' + cell.textContent.trim() + '"');
            });
            csv.push(cells.join(','));
        }
    });

    // إنشاء ملف وتحميله
    const csvContent = csv.join('\n');
    downloadFile(csvContent, 'attendance-logs.csv', 'text/csv');
}

/**
 * تحميل الجدول كـ PDF
 */
function exportToPDF() {
    const element = document.getElementById('dataTable');
    if (!element) return;

    const opt = {
        margin: 10,
        filename: 'attendance-logs.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'landscape', unit: 'mm', format: 'a4' }
    };

    // استخدام html2pdf إذا كانت المكتبة محملة
    if (typeof html2pdf !== 'undefined') {
        html2pdf().set(opt).from(element).save();
    } else {
        alert('خطأ: مكتبة html2pdf غير محملة');
    }
}

/**
 * تحميل ملف
 */
function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * إضافة تسميات البيانات للجوال
 */
function addDataLabelsForMobile() {
    const table = document.getElementById('dataTable');
    if (!table) return;

    const headers = [];
    table.querySelectorAll('thead th').forEach(header => {
        headers.push(header.textContent.trim());
    });

    table.querySelectorAll('tbody td').forEach((cell, index) => {
        if (index < headers.length) {
            cell.setAttribute('data-label', headers[index % headers.length]);
        }
    });
}

/**
 * رسوم متحركة مخصصة
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }

    @keyframes slideIn {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .table tbody tr {
        animation: fadeIn 0.3s ease;
    }
`;
document.head.appendChild(style);