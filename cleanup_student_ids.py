import mysql.connector  

# قم بتعديل هذه المتغيرات لتتناسب مع إعدادات قاعدة البيانات الخاصة بك  
DB_CONFIG = {  
    'host': 'localhost',  
    'user': 'root',  
    'password': '',  
    'database': 'smart_attendance_db', # تأكد من صحته  
    'autocommit': True  
}  

def cleanup_duplicate_student_ids_direct_db():  
    print("Connecting directly to database...")  
    cnx = None  
    try:  
        cnx = mysql.connector.connect(**DB_CONFIG)  
        cursor = cnx.cursor()  

        # طباعة اسم قاعدة البيانات المتصل بها  
        cursor.execute("SELECT DATABASE();")  
        connected_db = cursor.fetchone()[0]  
        print(f"Successfully connected to database: {connected_db}")  

        # --- هنا يجب أن يبدأ كل كود التنظيف الذي أرسلته لك سابقًا ---  
        print("--- PHASE 1: Cleaning student_id = 0 duplicates ---")  
        
        # استرجاع الطلاب الذين لديهم student_id = 0  
        cursor.execute("SELECT id, student_id FROM student WHERE student_id = 0 ORDER BY id")  
        students_with_zero_id = cursor.fetchall()  

        if not students_with_zero_id:  
            print("No students found with student_id = 0. Skipping Phase 1.")  
        else:  
            print(f"Found {len(students_with_zero_id)} students with student_id = 0 initially.")  
            
            if len(students_with_zero_id) > 1:  
                print("Multiple students found with student_id = 0. Attempting to set duplicates to NULL.")  
                first_student_id_to_keep_pk = students_with_zero_id[0][0] # الـ PK لأول طالب  

                for s_pk, s_val in students_with_zero_id:  
                    if s_pk != first_student_id_to_keep_pk:  
                        # التحقق قبل التحديث  
                        cursor.execute("SELECT student_id FROM student WHERE id = %s", (s_pk,))  
                        pre_update_val = cursor.fetchone()[0]  
                        print(f"  Student (PK: {s_pk}) pre-update value: {pre_update_val}")  

                        update_query = "UPDATE student SET student_id = NULL WHERE id = %s"  
                        cursor.execute(update_query, (s_pk,))  
                        print(f"  Attempted update for Student (PK: {s_pk}), old student_id: {s_val} to NULL")  
                        
                        # التحقق بعد التحديث مباشرة  
                        cursor.execute("SELECT student_id FROM student WHERE id = %s", (s_pk,))  
                        post_update_val = cursor.fetchone()[0]  
                        print(f"  Student (PK: {s_pk}) post-update value: {post_update_val}")  
                        if post_update_val is None:  
                            print(f"  SUCCESS: student_id for PK {s_pk} is now NULL.")  
                        else:  
                            print(f"  FAILURE: student_id for PK {s_pk} is still {post_update_val}. THIS IS A CRITICAL ISSUE!")  
                
                print("Phase 1: All individual updates for student_id = 0 processed.")  

                # التحقق النهائي بعد كل تحديثات المرحلة الأولى  
                print("\nVerifying final state for student_id = 0 after Phase 1:")  
                cursor.execute("SELECT id, student_id FROM student WHERE student_id = 0 ORDER BY id")  
                remaining_zero_ids = cursor.fetchall()  

                if len(remaining_zero_ids) > 1:  
                    print("CRITICAL WARNING: Multiple students with student_id = 0 still exist after Phase 1 completion!")  
                    print("  This indicates a fundamental issue with database writes or wrong database selected.")  
                    for s_pk, s_val in remaining_zero_ids:  
                        print(f"  Student ID (PK): {s_pk}, student_id (value): {s_val}")  
                elif len(remaining_zero_ids) == 1:  
                    print("Verification successful: Only one student with student_id = 0 remains (as intended).")  
                    print(f"  Remaining student: ID (PK): {remaining_zero_ids[0][0]}, student_id: {remaining_zero_ids[0][1]}")  
                else:  
                    print("Verification successful: No students with student_id = 0 remain.")  
            else:  
                print("Only one student found with student_id = 0. No duplicates to clean for '0' in Phase 1.")  

        print("\n--- PHASE 2: Cleaning other duplicate student_id values (excluding NULL and 0) ---")  
        cursor.execute("""  
            SELECT student_id, COUNT(student_id)  
            FROM student  
            WHERE student_id IS NOT NULL AND student_id != 0  
            GROUP BY student_id  
            HAVING COUNT(student_id) > 1;  
        """)  
        other_duplicate_ids = cursor.fetchall()  

        if not other_duplicate_ids:  
            print("No other duplicate student_id values found (excluding NULL and '0'). Skipping Phase 2.")  
        else:  
            print(f"Found other duplicate student_id values: {other_duplicate_ids}")  

            for student_id_val, count in other_duplicate_ids:  
                print(f"Processing duplicate student_id: {student_id_val} (count: {count})")  
                cursor.execute("SELECT id FROM student WHERE student_id = %s ORDER BY id", (student_id_val,))  
                students_to_update = cursor.fetchall()  

                for i, (s_pk,) in enumerate(students_to_update):  
                    if i > 0: # لا نغير أول نسخة  
                        # التحقق قبل التحديث  
                        cursor.execute("SELECT student_id FROM student WHERE id = %s", (s_pk,))  
                        pre_update_val = cursor.fetchone()[0]  
                        print(f"  Student (PK: {s_pk}) pre-update value: {pre_update_val}")  

                        update_query = "UPDATE student SET student_id = NULL WHERE id = %s"  
                        cursor.execute(update_query, (s_pk,))  
                        print(f"  Attempted update for Student (PK: {s_pk}), old student_id: {student_id_val} to NULL")  
                        
                        # التحقق بعد التحديث مباشرة  
                        cursor.execute("SELECT student_id FROM student WHERE id = %s", (s_pk,))  
                        post_update_val = cursor.fetchone()[0]  
                        print(f"  Student (PK: {s_pk}) post-update value: {post_update_val}")  
                        if post_update_val is None:  
                            print(f"  SUCCESS: student_id for PK {s_pk} is now NULL.")  
                        else:  
                            print(f"  FAILURE: student_id for PK {s_pk} is still {post_update_val}. THIS IS A CRITICAL ISSUE!")  
            
            print("Phase 2: All individual updates for other duplicates processed.")  

        print("\n--- FINAL VERIFICATION: Checking for ALL remaining duplicate student_id values (excluding NULL) ---")  
        cursor.execute("""  
            SELECT student_id, COUNT(student_id)  
            FROM student  
            WHERE student_id IS NOT NULL  
            GROUP BY student_id  
            HAVING COUNT(student_id) > 1;  
        """)  
        any_remaining_duplicates = cursor.fetchall()  

        if not any_remaining_duplicates:  
            print("Final verification: No duplicate student_id values found (excluding NULL).")  
            print("Cleanup complete. You should now be able to run 'flask db upgrade'.")  
        else:  
            print("Final verification: Remaining duplicate student_id values:")  
            for s_id, count in any_remaining_duplicates:  
                print(f"  Student_id: {s_id}, Count: {count}")  
            print("WARNING: Cleanup incomplete. Duplicates still exist after all attempts. Deeper issue likely.")  

    except mysql.connector.Error as err:  
        print(f"Database error: {err}")  
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")  
    finally:  
        if cnx:  
            cursor.close()  
            cnx.close()  
            print("Database connection closed.")  

if __name__ == '__main__':  
    cleanup_duplicate_student_ids_direct_db()