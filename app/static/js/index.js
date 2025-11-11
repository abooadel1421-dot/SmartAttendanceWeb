// static/js/admin_dashboard.js  

document.addEventListener('DOMContentLoaded', function() {  
    console.log("Admin Dashboard scripts loaded!");  

    // 1. إضافة تأثير بسيط عند النقر على بطاقات الإحصائيات  
    const statsCards = document.querySelectorAll('.stats-card');  
    statsCards.forEach(card => {  
        card.addEventListener('click', function() {  
            // يمكن إضافة تأثير بصري لحظي أو إعادة توجيه  
            this.style.transform = 'translateY(-2px) scale(1.01)';  
            this.style.boxShadow = '0 6px 15px rgba(0,0,0,0.1)';  
            setTimeout(() => {  
                this.style.transform = '';  
                this.style.boxShadow = '';  
            }, 200); // إزالة التأثير بعد 200 مللي ثانية  
            
            // مثال: يمكن أن يوجه إلى صفحة التفاصيل  
            // console.log("Card clicked: " + this.querySelector('h6').textContent);  
            // window.location.href = '/admin/some_detail_page';   
        });  

        // إضافة مؤشر للماوس  
        card.style.cursor = 'pointer';  
    });  

    // 2. مثال على وظيفة لتحديث البيانات ديناميكيًا (وهمي)  
    function updateDashboardData() {  
        // يمكنك هنا إجراء طلب AJAX لجلب أحدث البيانات من الخادم  
        // ثم تحديث العناصر في الصفحة.  
        console.log("Updating dashboard data...");  

        // مثال وهمي لتحديث الأرقام  
        const totalStudentsElement = document.querySelector('.stats-card:nth-child(1) h3');  
        const totalUsersElement = document.querySelector('.stats-card:nth-child(2) h3');  
        // ... وهكذا لباقي العناصر  

        if (totalStudentsElement) {  
            totalStudentsElement.textContent = Math.floor(Math.random() * 500) + 100; // رقم عشوائي  
        }  
        if (totalUsersElement) {  
            totalUsersElement.textContent = Math.floor(Math.random() * 50) + 10;  
        }  

        // يمكنك جدولة هذا للتشغيل كل فترة زمنية  
        // setTimeout(updateDashboardData, 30000); // تحديث كل 30 ثانية  
    }  

    // قم بتشغيل وظيفة التحديث عند تحميل الصفحة  
    // updateDashboardData();  

    // 3. إضافة تأثير عند التحويم على روابط الإجراءات السريعة (إذا لم يكن CSS كافيًا)  
    const quickLinks = document.querySelectorAll('.list-group-item-action');  
    quickLinks.forEach(link => {  
        link.addEventListener('mouseenter', function() {  
            this.querySelector('i').style.transition = 'color 0.2s ease';  
            this.querySelector('i').style.color = '#007bff'; // تغيير لون الأيقونة  
        });  
        link.addEventListener('mouseleave', function() {  
            this.querySelector('i').style.color = '#6c757d'; // إعادة اللون الأصلي  
        });  
    });  


    // مثال بسيط لتأكيد أن السكريبت يعمل  
    // alert("أهلاً بك في لوحة تحكم الإدارة!");  
});