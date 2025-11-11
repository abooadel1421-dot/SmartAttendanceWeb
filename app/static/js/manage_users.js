// static/js/admin_manage_users.js  

document.addEventListener('DOMContentLoaded', function() {  
    console.log("Admin Manage Users JavaScript loaded!");  

    // 1. تفعيل DataTables  
    // تأكد من أن jQuery و DataTables JS تم تحميلهما قبل هذا السكريبت  
    // في هذا التحديث، قمنا بتضمين روابط CDN في manage_users.html  
    if ($.fn.DataTable) { // التحقق من وجود DataTables  
        $('#usersDataTable').DataTable({  
            "language": {  
                "url": "//cdn.datatables.net/plug-ins/1.11.5/i18n/ar.json" // تحديث لـ DataTables v1.11.5  
            },  
            "pagingType": "full_numbers", // أزرار ترقيم كاملة  
            "lengthMenu": [  
                [10, 25, 50, -1],  
                [10, 25, 50, "الكل"]  
            ], // خيارات عدد الصفوف  
            "order": [  
                [0, "asc"]  
            ], // ترتيب افتراضي حسب ID تصاعدي  
            "columnDefs": [{  
                "targets": -1, // العمود الأخير (الإجراءات)  
                "orderable": false, // تعطيل الترتيب لهذا العمود  
                "searchable": false // تعطيل البحث لهذا العمود  
            }]  
        });  
    } else {  
        console.warn("DataTables library not found. Table functionality will be limited.");  
    }  

    // 2. تفعيل Modals (نوافذ Bootstrap المنبثقة)  
    // Bootstrap 5 Modals لا تتطلب تهيئة يدوية مثل Bootstrap 4  
    // ولكن يمكننا إضافة بعض الوظائف الإضافية إذا لزم الأمر.  
    // على سبيل المثال، التأكد من إغلاق المودال عند النقر خارجها (افتراضي في BS5)  

    // 3. تحسين رسائل الفلاش (Fade out)  
    // هذا الجزء تم تغطيته بالفعل في public_base.js  
    // ولكن يمكننا إضافة تأثيرات خاصة هنا إذا أردت.  
    // حاليًا، public_base.js يتعامل معها بشكل عام.  

    // 4. تأثيرات الأزرار (إذا لم تكن مغطاة بالكامل بواسطة CSS)  
    // تم تغطية معظم تأثيرات الأزرار بواسطة CSS، ولكن يمكن إضافة المزيد هنا إذا لزم الأمر.  

    // 5. وظيفة البحث الفوري في الجدول (إذا لم تستخدم DataTables)  
    // بما أننا نستخدم DataTables، فهي توفر وظيفة البحث الافتراضية.  
    // إذا أردت بحثًا مخصصًا، يمكن إضافته هنا.  
});