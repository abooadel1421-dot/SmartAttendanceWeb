
document.addEventListener('DOMContentLoaded', function() {  
    console.log("Card Form JavaScript loaded!");  

    // 1. تفعيل Flatpickr (مكتبة Datepicker)  
    const issuedAtField = document.querySelector('.datepicker');  
    if (issuedAtField) {  
        flatpickr(issuedAtField, {  
            locale: "ar",
            altInput: true,
            altFormat: "F j, Y",
            dateFormat: "Y-m-d",
            maxDate: "today",
        });  
    }  

    // 2. تفعيل Bootstrap form validation  
    const form = document.querySelector('.needs-validation');  
    if (form) {  
        form.addEventListener('submit', function(event) {  
            if (!form.checkValidity()) {  
                event.preventDefault();  
                event.stopPropagation();  
            }  
            form.classList.add('was-validated');  
        }, false);  
    }  

    // ====================================================================  
    // 3. منطق قراءة البطاقة (Scan Card Logic) - محدث بـ Short Polling
    // ====================================================================  
    const scanCardBtn = document.getElementById('scanCardBtn');  
    const cancelScanBtn = document.getElementById('cancelScanBtn');  
    const cardUidField = document.getElementById('card_uid');  
    const scanStatusMessage = document.getElementById('scanStatusMessage');  
    const scanSpinner = document.getElementById('scanSpinner');  
    const cardUidGroup = document.getElementById('cardUidGroup');

    let scanPollingInterval = null; // لتكرار التحقق من البطاقة
    let scanStartTime = null; // وقت بدء المسح
    let currentScanSessionId = null; // معرف الجلسة الحالية
    const SCAN_TIMEOUT = 60000; // 60 ثانية timeout

    if (scanCardBtn && cancelScanBtn && cardUidField && scanStatusMessage && scanSpinner && cardUidGroup) {  

        // وظيفة لتوليد معرف جلسة فريد  
        function generateSessionId() {  
            return 'scan-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);  
        }  

        // وظيفة لعرض رسالة حالة  
        function showScanStatus(message, type = 'info') {  
            scanStatusMessage.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">  
                                            ${message}  
                                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>  
                                          </div>`;
            if (type !== 'danger') {  
                setTimeout(() => {  
                    const alertElement = scanStatusMessage.querySelector('.alert');  
                    if (alertElement) {  
                        const bsAlert = bootstrap.Alert.getInstance(alertElement) || new bootstrap.Alert(alertElement);  
                        bsAlert.close();  
                    }  
                }, 5000);  
            }  
        }  

        // وظيفة لتغيير حالة عناصر الواجهة أثناء المسح  
        function setScanningState(isScanning) {  
            if (isScanning) {  
                scanCardBtn.disabled = true;  
                cancelScanBtn.disabled = false;  
                cardUidField.readOnly = true;  
                scanSpinner.classList.remove('d-none');  
                scanStatusMessage.innerHTML = '';
                cardUidGroup.classList.add('scanning-active');
            } else {  
                scanCardBtn.disabled = false;  
                cancelScanBtn.disabled = true;  
                cardUidField.readOnly = false;  
                scanSpinner.classList.add('d-none');  
                cardUidGroup.classList.remove('scanning-active');  
            }  
        }

        // إيقاف المسح
        function stopScanning() {
            if (scanPollingInterval) {
                clearInterval(scanPollingInterval);
                scanPollingInterval = null;
            }
            setScanningState(false);
            scanStartTime = null;
        }

        // دالة التحقق المتكرر من الـ UID
        async function checkForScannedCard() {
            // فحص Timeout
            if (Date.now() - scanStartTime > SCAN_TIMEOUT) {
                stopScanning();
                showScanStatus('انتهت مهلة المسح. لم يتم الكشف عن بطاقة.', 'warning');
                currentScanSessionId = null;
                return;
            }

            try {
                const response = await fetch('/api/admin/check-scanned-uid', {
                    method: 'GET',
                    headers: {
                        'X-Session-ID': currentScanSessionId
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.success && data.card_uid) {
                        // وُجدت البطاقة!
                        console.log('✅ UID ممسوح:', data.card_uid);
                        cardUidField.value = data.card_uid;
                        showScanStatus(data.message, 'success');
                        stopScanning();
                        currentScanSessionId = null;
                    }
                }
                // إذا 404 = لا توجد بطاقة بعد، استمر في Polling

            } catch (error) {
                console.error('خطأ في التحقق:', error);
            }
        }

        // عند النقر على زر "قراءة بطاقة"  
        scanCardBtn.addEventListener('click', async function() {
            console.log('🔵 زر المسح تم الضغط عليه');
            
            setScanningState(true);  
            showScanStatus('يرجى تمرير البطاقة الآن...', 'info');  

            currentScanSessionId = generateSessionId();
            scanStartTime = Date.now();

            console.log('🆔 Session ID:', currentScanSessionId);

            // 1. بدء جلسة المسح
            try {  
                const response = await fetch('/api/admin/scan-card-for-form', {  
                    method: 'POST',
                    headers: {  
                        'X-Session-ID': currentScanSessionId,
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                console.log('📡 رد من الخادم:', data);
                
                if (!data.success) {
                    showScanStatus(data.message, 'danger');
                    stopScanning();
                    currentScanSessionId = null;
                    return;
                }

                console.log('✅ جلسة المسح نشطة');

                // 2. بدء Polling للتحقق من الـ UID كل 500ms
                scanPollingInterval = setInterval(checkForScannedCard, 500);

            } catch (error) {  
                console.error('❌ خطأ في بدء المسح:', error);  
                showScanStatus('فشل الاتصال بالخادم', 'danger');
                stopScanning();
                currentScanSessionId = null;
            }  
        });  

        // عند النقر على زر "إلغاء"  
        cancelScanBtn.addEventListener('click', async function() {
            console.log('🔴 زر الإلغاء تم الضغط عليه');
            
            stopScanning();
            
            if (!currentScanSessionId) {
                showScanStatus('لا توجد عملية مسح نشطة', 'info');
                return;
            }

            try {
                const response = await fetch('/api/admin/cancel-card-scan', {  
                    method: 'POST',  
                    headers: {  
                        'Content-Type': 'application/json',  
                        'X-Session-ID': currentScanSessionId
                    },  
                    body: JSON.stringify({})
                });
                
                const data = await response.json();
                
                if (data.success) {  
                    showScanStatus(data.message, 'info');  
                } else {  
                    showScanStatus(data.message, 'danger');  
                }
            } catch (error) {  
                console.error('❌ خطأ في الإلغاء:', error);  
                showScanStatus('حدث خطأ أثناء إلغاء عملية المسح.', 'danger');  
            } finally {
                currentScanSessionId = null;
            }
        });  

        // تهيئة الحالة الأولية للأزرار  
        setScanningState(false);  
    } else {
        console.error('❌ لم يتم العثور على عناصر واجهة المسح');
    }
});