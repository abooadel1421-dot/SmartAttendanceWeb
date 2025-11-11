// static/js/attendance_realtime.js
// استخدام WebSocket للتحديث الفوري بدلاً من Polling

class AttendanceRealtime {
    constructor(options = {}) {
        this.tableId = options.tableId || 'dataTable';
        this.apiEndpoint = options.apiEndpoint || '/admin/api/attendance_logs';
        this.websocketUrl = options.websocketUrl || '/socket.io';
        this.maxRows = options.maxRows || 50;
        this.loadedIds = new Set();
        this.isRunning = false;
        this.socket = null;
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        console.log('🔄 بدء التحديث الفوري للحضور');
        
        // التحميل الأول
        this.loadInitialData();
        
        // الاتصال بـ WebSocket
        this.connectWebSocket();
    }

    stop() {
        if (this.socket) {
            this.socket.off('new_attendance_log');
            this.isRunning = false;
            console.log('⏹ توقف التحديث الفعلي');
        }
    }

    /**
     * الاتصال بـ WebSocket
     */
    connectWebSocket() {
        // استخدام socket.io الذي تم تهيئته مسبقاً
        if (typeof io !== 'undefined') {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('✅ تم الاتصال بـ WebSocket');
            });

            // استقبال السجلات الجديدة
            this.socket.on('new_attendance_log', (data) => {
                console.log('📥 سجل جديد:', data);
                this.handleNewLog(data);
            });

            this.socket.on('disconnect', () => {
                console.log('❌ تم قطع الاتصال بـ WebSocket');
            });

            this.socket.on('error', (error) => {
                console.error('⚠️ خطأ في WebSocket:', error);
            });
        } else {
            console.warn('⚠️ socket.io غير محمل، استخدام Polling بدلاً منه');
            // البديل: استخدام Polling كل 2 ثانية
            this.intervalId = setInterval(() => this.fetchLatestLogs(), 2000);
        }
    }

    /**
     * التعامل مع السجل الجديد
     */
    handleNewLog(logData) {
        const tbody = document.querySelector(`#${this.tableId} tbody`);
        if (!tbody) return;

        // تحقق أن السجل جديد
        if (this.loadedIds.has(logData.id)) return;

        // إنشاء صف جديد
        const newRow = this.createTableRow(logData);
        tbody.insertBefore(newRow, tbody.firstChild);
        this.loadedIds.add(logData.id);
        this.highlightNewRow(newRow);
        
        console.log(`✅ سجل جديد: ${logData.student_name} - ${logData.status}`);

        // حذف الصفوف الزائدة
        this.trimExcessRows();
        
        // تحديث الإحصائيات
        this.updateStatisticsForNewLog(logData);
    }

    /**
     * تحميل البيانات الأولية
     */
    loadInitialData() {
        fetch(this.apiEndpoint)
            .then(response => response.json())
            .then(data => {
                if (data.logs) {
                    this.renderAllLogs(data.logs);
                }
            })
            .catch(error => console.error('❌ خطأ في التحميل الأول:', error));
    }

    /**
     * جلب السجلات الجديدة (للـ Polling فقط)
     */
    fetchLatestLogs() {
        fetch(this.apiEndpoint)
            .then(response => response.json())
            .then(data => {
                if (data.logs) {
                    this.addNewLogsOnly(data.logs);
                }
            })
            .catch(error => console.error('❌ خطأ في التحديث:', error));
    }

    /**
     * عرض جميع السجلات في التحميل الأول
     */
    renderAllLogs(logs) {
        const tbody = document.querySelector(`#${this.tableId} tbody`);
        if (!tbody) return;

        tbody.innerHTML = '';
        this.loadedIds.clear();

        const sortedLogs = [...logs].sort((a, b) => b.id - a.id);

        sortedLogs.forEach((log, index) => {
            const row = this.createTableRow(log, index + 1);
            tbody.appendChild(row);
            this.loadedIds.add(log.id);
        });

        this.updateStatistics(logs);
    }

    /**
     * إضافة السجلات الجديدة فقط
     */
    addNewLogsOnly(logs) {
        const tbody = document.querySelector(`#${this.tableId} tbody`);
        if (!tbody) return;

        const newLogs = logs.filter(log => !this.loadedIds.has(log.id));

        if (newLogs.length === 0) return;

        const sortedNewLogs = [...newLogs].sort((a, b) => b.id - a.id);

        sortedNewLogs.forEach((log) => {
            const newRow = this.createTableRow(log);
            tbody.insertBefore(newRow, tbody.firstChild);
            this.loadedIds.add(log.id);
            this.highlightNewRow(newRow);
        });

        this.trimExcessRows();
        this.updateStatistics(logs);
    }

    /**
     * حذف الصفوف الزائدة
     */
    trimExcessRows() {
        const tbody = document.querySelector(`#${this.tableId} tbody`);
        if (!tbody) return;

        const rows = Array.from(tbody.querySelectorAll('tr[data-log-id]'));
        
        while (rows.length > this.maxRows) {
            const lastRow = rows.pop();
            const logId = parseInt(lastRow.getAttribute('data-log-id'));
            this.loadedIds.delete(logId);
            lastRow.remove();
        }
    }

    /**
     * إنشاء صف جدول جديد
     */
    createTableRow(log, index) {
        const row = document.createElement('tr');
        row.setAttribute('data-log-id', log.id);
        
        const statusBadge = log.status === 'ENTER' 
            ? `<span class="badge bg-success"><i class="fas fa-check-circle me-1"></i>دخول</span>`
            : `<span class="badge bg-warning"><i class="fas fa-times-circle me-1"></i>خروج</span>`;

        const rowNumber = index || this.getNextRowNumber();

        row.innerHTML = `
            <td class="text-center row-number">${rowNumber}</td>
            <td>
                <i class="fas fa-user-circle me-2 text-primary"></i>
                ${log.student_name || 'غير معروف'}
            </td>
            <td class="text-center">
                <span class="badge bg-light text-dark">${log.student_id_number || 'N/A'}</span>
            </td>
            <td>
                <i class="fas fa-microchip me-2 text-info"></i>
                ${log.device_name || 'غير معروف'}
            </td>
            <td>
                <i class="fas fa-map-marker-alt me-2 text-danger"></i>
                ${log.device_location || 'غير متوفر'}
            </td>
            <td class="text-center">
                <span class="timestamp-badge">${this.formatTime(log.timestamp)}</span>
            </td>
            <td class="text-center">${statusBadge}</td>
        `;

        return row;
    }

    /**
     * الحصول على رقم الصف التالي
     */
    getNextRowNumber() {
        const tbody = document.querySelector(`#${this.tableId} tbody`);
        if (!tbody) return 1;
        
        const rows = tbody.querySelectorAll('tr[data-log-id]');
        return rows.length + 1;
    }

    /**
     * تأثير بصري للصفوف الجديدة
     */
    highlightNewRow(row) {
        row.style.backgroundColor = '#d4edda';
        row.style.transition = 'background-color 0.5s ease';
        
        setTimeout(() => {
            row.style.backgroundColor = '';
        }, 2000);
    }

    /**
     * تحديث الإحصائيات للسجل الجديد
     */
    updateStatisticsForNewLog(log) {
        const accessEl = document.getElementById('totalAccess');
        const deniedEl = document.getElementById('totalDenied');

        if (log.status === 'ENTER' && accessEl) {
            accessEl.textContent = parseInt(accessEl.textContent) + 1;
        } else if (log.status === 'EXIT' && deniedEl) {
            deniedEl.textContent = parseInt(deniedEl.textContent) + 1;
        }

        const recordsEl = document.getElementById('totalRecords');
        const recordCountEl = document.getElementById('recordCount');
        if (recordsEl) recordsEl.textContent = parseInt(recordsEl.textContent) + 1;
        if (recordCountEl) recordCountEl.textContent = `${recordsEl.textContent} سجل`;
    }

    /**
     * تحديث الإحصائيات الكاملة
     */
    updateStatistics(logs) {
        const totalAccess = logs.filter(l => l.status === 'ENTER').length;
        const totalDenied = logs.filter(l => l.status === 'EXIT').length;

        const accessEl = document.getElementById('totalAccess');
        const deniedEl = document.getElementById('totalDenied');
        const recordsEl = document.getElementById('totalRecords');
        const recordCountEl = document.getElementById('recordCount');

        if (accessEl) accessEl.textContent = totalAccess;
        if (deniedEl) deniedEl.textContent = totalDenied;
        if (recordsEl) recordsEl.textContent = logs.length;
        if (recordCountEl) recordCountEl.textContent = `${logs.length} سجل`;
    }

    /**
     * تنسيق التاريخ والوقت
     */
/**
     * تنسيق التاريخ والوقت
     */
formatTime(timestamp) {
    if (!timestamp) return 'N/A';
    
    const date = new Date(timestamp);
    let hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');

    // ✅ تحويل إلى 12 ساعة مع AM/PM
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // الساعة 0 تصبح 12
    hours = String(hours).padStart(2, '0');

    // ✅ صيغة: HH:MM:SS AM/PM DD/MM
    return `${hours}:${minutes}:${seconds} ${ampm} ${day}/${month}`;
}
}

// تهيئة النظام
document.addEventListener('DOMContentLoaded', function() {
    const realtime = new AttendanceRealtime({
        tableId: 'dataTable',
        apiEndpoint: '/admin/api/attendance_logs',
        maxRows: 50
    });

    realtime.start();

    window.addEventListener('beforeunload', function() {
        realtime.stop();
    });

    window.attendanceRealtime = realtime;
});