// static/js/advanced_search.js - نظام البحث المتقدم الكامل

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const dateFromFilter = document.getElementById('dateFromFilter');
    const dateToFilter = document.getElementById('dateToFilter');
    const applyFiltersBtn = document.getElementById('applyFiltersBtn');
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    const toggleSearchBtn = document.getElementById('toggleSearchBtn');
    const searchFilters = document.getElementById('searchFilters');
    const resultsCount = document.getElementById('resultsCount');
    const table = document.getElementById('cardsDataTable');

    if (!table) {
        console.error('جدول البطاقات غير موجود!');
        return;
    }

    // تبديل إظهار/إخفاء البحث المتقدم
    if (toggleSearchBtn) {
        toggleSearchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            searchFilters.classList.toggle('collapsed');
            const icon = toggleSearchBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-chevron-down');
                icon.classList.toggle('fa-chevron-up');
            }
        });
    }

    // البحث الفوري (Real-time Search)
    if (searchInput) {
        searchInput.addEventListener('keyup', applyFilters);
    }
    if (statusFilter) {
        statusFilter.addEventListener('change', applyFilters);
    }
    if (dateFromFilter) {
        dateFromFilter.addEventListener('change', applyFilters);
    }
    if (dateToFilter) {
        dateToFilter.addEventListener('change', applyFilters);
    }

    // الأزرار
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            applyFilters();
        });
    }
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            resetFilters();
        });
    }

    // دالة تطبيق الفلاتر
    function applyFilters() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const status = statusFilter ? statusFilter.value : '';
        const dateFrom = dateFromFilter ? dateFromFilter.value : '';
        const dateTo = dateToFilter ? dateToFilter.value : '';

        const rows = table.querySelectorAll('tbody tr');
        let visibleCount = 0;
        let totalCount = 0;

        rows.forEach(row => {
            // تخطي صفوف الرسائل الفارغة
            if (row.querySelector('td[colspan]')) {
                row.style.display = 'none';
                return;
            }

            totalCount++;
            let isVisible = true;

            // فحص البحث العام (الاسم أو رقم البطاقة)
            if (searchTerm) {
                const cardUidCell = row.querySelector('td:nth-child(2)');
                const studentCell = row.querySelector('td:nth-child(3)');
                
                const cardUid = cardUidCell ? cardUidCell.textContent.toLowerCase() : '';
                const studentText = studentCell ? studentCell.textContent.toLowerCase() : '';
                
                isVisible = cardUid.includes(searchTerm) || studentText.includes(searchTerm);
            }

            // فحص الحالة
            if (isVisible && status) {
                const rowStatus = row.getAttribute('data-status');
                isVisible = rowStatus === status;
            }

            // فحص نطاق التواريخ
            if (isVisible && (dateFrom || dateTo)) {
                const rowDate = row.getAttribute('data-issued-date');
                
                if (dateFrom && rowDate && rowDate < dateFrom) {
                    isVisible = false;
                }
                if (dateTo && rowDate && rowDate > dateTo) {
                    isVisible = false;
                }
            }

            // عرض أو إخفاء الصف
            row.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCount++;
        });

        // تحديث عدد النتائج
        updateResultsCount(visibleCount, totalCount);
    }

    // دالة إعادة تعيين الفلاتر
    function resetFilters() {
        if (searchInput) searchInput.value = '';
        if (statusFilter) statusFilter.value = '';
        if (dateFromFilter) dateFromFilter.value = '';
        if (dateToFilter) dateToFilter.value = '';
        
        // إظهار جميع الصفوف
        const rows = table.querySelectorAll('tbody tr');
        let count = 0;
        rows.forEach(row => {
            if (!row.querySelector('td[colspan]')) {
                row.style.display = '';
                count++;
            }
        });

        updateResultsCount(count, count);
    }

    // دالة تحديث عدد النتائج
    function updateResultsCount(visible, total) {
        if (!resultsCount) return;
        
        if (visible === 0 && visible !== total) {
            resultsCount.textContent = '❌ لا توجد نتائج';
            resultsCount.style.color = '#dc3545';
        } else if (visible === total) {
            resultsCount.textContent = `📊 ${total} نتائج`;
            resultsCount.style.color = '#6c757d';
        } else {
            resultsCount.textContent = `🔍 ${visible} من ${total} نتائج`;
            resultsCount.style.color = '#17a2b8';
        }
    }

    // تهيئة عدد النتائج عند التحميل
    setTimeout(function() {
        const rows = table.querySelectorAll('tbody tr');
        let count = 0;
        rows.forEach(row => {
            if (!row.querySelector('td[colspan]')) {
                count++;
            }
        });
        updateResultsCount(count, count);
    }, 500);
});