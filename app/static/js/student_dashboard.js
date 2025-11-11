// static/js/student_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

/**
 * تهيئة لوحة تحكم الطالب
 */
function initializeDashboard() {
    addAnimations();
    setupCardInteractions();
    setupTableEnhancements();
    loadAttendanceStats();
    initializeTooltips();
}

/**
 * إضافة التأثيرات والحركات
 */
function addAnimations() {
    const cards = document.querySelectorAll('.card');
    const header = document.querySelector('.student-dashboard-header');
    
    // تأثير الظهور للرأس
    if (header) {
        header.style.animation = 'slideDown 0.5s ease';
    }
    
    // تأثير الظهور للبطاقات
    cards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease ${index * 0.1}s both`;
    });
    
    // تأثير التمرير على البطاقات
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 15px 40px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.15)';
        });
    });
}

/**
 * إعداد تفاعلات البطاقات
 */
function setupCardInteractions() {
    const cardHeaders = document.querySelectorAll('.card-header');
    
    cardHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        
        header.addEventListener('click', function() {
            const card = this.closest('.card');
            const body = card.querySelector('.card-body');
            
            // تأثير التوسع والطي (اختياري)
            if (body.style.maxHeight) {
                body.style.maxHeight = null;
            } else {
                body.style.maxHeight = body.scrollHeight + 'px';
            }
        });
    });
}

/**
 * تحسينات الجداول
 */
function setupTableEnhancements() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach((row, index) => {
            row.style.transition = 'all 0.3s ease';
            
            // تأثير التمرير
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f9fafb';
                this.style.transform = 'scale(1.002)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
                this.style.transform = 'scale(1)';
            });
        });
    });
}

/**
 * تحميل إحصائيات الحضور
 */
function loadAttendanceStats() {
    const table = document.querySelector('.table');
    
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    if (rows.length > 0) {
        let enterCount = 0;
        let exitCount = 0;
        
        rows.forEach(row => {
            const badge = row.querySelector('.badge');
            if (badge) {
                if (badge.textContent.includes('دخول')) {
                    enterCount++;
                } else if (badge.textContent.includes('خروج')) {
                    exitCount++;
                }
            }
        });
        
        // يمكن إضافة عرض الإحصائيات هنا
        console.log('إحصائيات الحضور:', {
            دخول: enterCount,
            خروج: exitCount,
            الإجمالي: rows.length
        });
    }
}

/**
 * تهيئة التلميحات (Tooltips)
 */
function initializeTooltips() {
    const badges = document.querySelectorAll('.badge');
    
    badges.forEach(badge => {
        badge.addEventListener('mouseover', function() {
            this.style.opacity = '0.9';
        });
        
        badge.addEventListener('mouseout', function() {
            this.style.opacity = '1';
        });
    });
}

/**
 * تحديث سجلات الحضور (يمكن استدعاؤها دورياً)
 */
function refreshAttendanceLogs() {
    fetch('/student/api/attendance-records')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateAttendanceTable(data.logs);
                console.log('تم تحديث سجلات الحضور');
            }
        })
        .catch(error => console.error('خطأ في تحديث السجلات:', error));
}

/**
 * تحديث جدول الحضور
 */
function updateAttendanceTable(logs) {
    const tbody = document.querySelector('.table tbody');
    
    if (!tbody) return;
    
    // مسح الصفوف القديمة
    tbody.innerHTML = '';
    
    if (logs.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-4">
                    <i class="bi bi-inbox"></i> لا توجد سجلات حضور
                </td>
            </tr>
        `;
        return;
    }
    
    // إضافة الصفوف الجديدة
    logs.forEach((log, index) => {
        const row = document.createElement('tr');
        const statusBadge = log.status === 'ENTER' 
            ? '<span class="badge bg-success"><i class="bi bi-arrow-right-short"></i>دخول</span>'
            : '<span class="badge bg-danger"><i class="bi bi-arrow-left-short"></i>خروج</span>';
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${log.timestamp}</td>
            <td>${statusBadge}</td>
            <td>${log.device_name || 'غير معروف'}</td>
        `;
        
        tbody.appendChild(row);
    });
}

/**
 * عرض رسالة تنبيه
 */
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        <strong>${type === 'success' ? 'نجح!' : 'تحذير!'}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container.mt-4');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // إزالة تلقائية بعد 5 ثواني
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * تحميل بيانات الملف الشخصي
 */
function loadProfileData() {
    const profileImage = document.querySelector('.profile-image-container img');
    
    if (profileImage) {
        profileImage.addEventListener('load', function() {
            console.log('تم تحميل صورة الملف الشخصي');
        });
        
        profileImage.addEventListener('error', function() {
            console.log('فشل تحميل الصورة، استخدام الصورة الافتراضية');
        });
    }
}

/**
 * حفظ تفضيلات الطالب (اختياري)
 */
function savePreferences() {
    const preferences = {
        lastVisit: new Date().toISOString(),
        theme: 'light'
    };
    
    // يمكن حفظها في sessionStorage إذا لزم الأمر
    sessionStorage.setItem('studentPreferences', JSON.stringify(preferences));
}

/**
 * تحميل التفضيلات المحفوظة
 */
function loadPreferences() {
    const saved = sessionStorage.getItem('studentPreferences');
    
    if (saved) {
        const preferences = JSON.parse(saved);
        console.log('التفضيلات المحفوظة:', preferences);
    }
}

/**
 * تصدير السجلات (اختياري)
 */
function exportRecords() {
    const table = document.querySelector('.table');
    
    if (!table) {
        showAlert('warning', 'لا توجد بيانات لتصديرها');
        return;
    }
    
    let csv = [];
    const headers = [];
    
    // جمع الرؤوس
    table.querySelectorAll('thead th').forEach(header => {
        headers.push(header.textContent.trim());
    });
    csv.push(headers.join(','));
    
    // جمع البيانات
    table.querySelectorAll('tbody tr').forEach(row => {
        const cells = [];
        row.querySelectorAll('td').forEach(cell => {
            cells.push('"' + cell.textContent.trim() + '"');
        });
        csv.push(cells.join(','));
    });
    
    // إنشاء ملف وتحميله
    const csvContent = csv.join('\n');
    downloadFile(csvContent, 'attendance_records.csv', 'text/csv');
    
    showAlert('success', 'تم تصدير السجلات بنجاح');
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
 * تحديث دوري للسجلات (كل 30 ثانية)
 */
function startAutoRefresh(interval = 30000) {
    setInterval(() => {
        refreshAttendanceLogs();
    }, interval);
}

// تهيئة البيانات عند التحميل
loadProfileData();
loadPreferences();