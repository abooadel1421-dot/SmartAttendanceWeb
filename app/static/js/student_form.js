// static/js/student_form.js  

document.addEventListener('DOMContentLoaded', function() {  
    console.log("Student Form JavaScript loaded!");  

    // 1. تفعيل Flatpickr (مكتبة Datepicker)  
    const dateOfBirthField = document.querySelector('.datepicker');  
    if (dateOfBirthField) {  
        flatpickr(dateOfBirthField, {  
            locale: "ar", // تفعيل اللغة العربية  
            altInput: true, // عرض تاريخ منسق في حقل منفصل  
            altFormat: "F j, Y", // تنسيق عرض التاريخ (مثال: يناير 1, 2023)  
            dateFormat: "Y-m-d", // تنسيق إرسال التاريخ إلى الخادم  
            maxDate: "today", // لا يمكن اختيار تاريخ في المستقبل  
            // يمكن إضافة المزيد من الخيارات هنا حسب الحاجة  
        });  
    }  

    // 2. تفعيل Bootstrap form validation (إذا كنت تستخدمها)  
    // هذا الكود يمكن أن يكون موجودًا في ملف JS العام مثل public_base.js  
    // ولكن لضمان تفعيله لهذا النموذج بشكل خاص:  
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

    // 3. أي منطق JavaScript آخر خاص بهذا النموذج يمكن إضافته هنا  
    // على سبيل المثال، التفاعل مع حقول معينة، أو عمليات AJAX  
});