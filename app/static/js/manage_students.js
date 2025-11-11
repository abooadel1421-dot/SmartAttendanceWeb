// static/js/admin_manage_students.js  

document.addEventListener('DOMContentLoaded', function() {  
    console.log("Admin Manage Students JavaScript loaded!");  

    // 1. تفعيل DataTables  
    // تأكد من أن jQuery و DataTables JS تم تحميلهما قبل هذا السكريبت  
    if ($.fn.DataTable) { // التحقق من وجود DataTables  
        $('#studentsDataTable').DataTable({ // تم تغيير ID الجدول إلى studentsDataTable  
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
            ], // ترتيب افتراضي حسب العمود الأول (#) تصاعدي  
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

    // 3. تحسين رسائل الفلاش (Fade out)  
    // هذا الجزء تم تغطيته بالفعل في public_base.js  
    // ولكن يمكننا إضافة تأثيرات خاصة هنا إذا أردت.  
});