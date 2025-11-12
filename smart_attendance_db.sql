-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 28, 2025 at 06:17 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_attendance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('94912fa31ac9');

-- --------------------------------------------------------

--
-- Table structure for table `attendance_log`
--

DROP TABLE IF EXISTS `attendance_log`;
CREATE TABLE `attendance_log` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `device_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` enum('ENTER','EXIT') NOT NULL,
  `card_id` int(11) DEFAULT NULL,
  `final_status` enum('PRESENT','LATE','ABSENT','EXCUSED','UNKNOWN') DEFAULT NULL,
  `report_generated_at` datetime DEFAULT NULL,
  `report_generated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_log`
--

INSERT INTO `attendance_log` (`id`, `student_id`, `device_id`, `timestamp`, `status`, `card_id`, `final_status`, `report_generated_at`, `report_generated_by`) VALUES
(1, 1, 1, '2025-10-23 05:46:35', 'ENTER', 2, NULL, NULL, NULL),
(2, 1, 1, '2025-10-23 05:46:39', 'EXIT', 2, 'EXCUSED', '2025-10-23 06:22:04', 3),
(3, 1, 1, '2025-10-23 06:59:11', 'ENTER', 2, NULL, NULL, NULL),
(4, 1, 1, '2025-10-23 06:59:16', 'EXIT', 2, NULL, NULL, NULL),
(5, 1, 1, '2025-10-23 06:59:22', 'ENTER', 2, NULL, NULL, NULL),
(6, 1, 1, '2025-10-23 06:59:26', 'EXIT', 2, NULL, NULL, NULL),
(7, 1, 1, '2025-10-23 07:00:35', 'ENTER', 2, NULL, NULL, NULL),
(8, 1, 1, '2025-10-23 07:00:40', 'EXIT', 2, NULL, NULL, NULL),
(9, 1, 1, '2025-10-23 07:01:15', 'ENTER', 2, NULL, NULL, NULL),
(10, 1, 1, '2025-10-23 07:11:47', 'EXIT', 2, NULL, NULL, NULL),
(11, NULL, 1, '2025-10-23 07:11:54', 'ENTER', NULL, NULL, NULL, NULL),
(12, NULL, 1, '2025-10-23 07:11:58', 'EXIT', NULL, NULL, NULL, NULL),
(13, NULL, 1, '2025-10-23 07:14:20', 'ENTER', NULL, NULL, NULL, NULL),
(14, 1, 1, '2025-10-23 07:28:27', 'ENTER', 2, NULL, NULL, NULL),
(15, 4, 1, '2025-10-23 07:28:32', 'ENTER', 5, NULL, NULL, NULL),
(16, 4, 1, '2025-10-23 07:28:37', 'EXIT', 5, NULL, NULL, NULL),
(17, 1, 1, '2025-10-27 01:45:33', 'EXIT', 2, NULL, NULL, NULL),
(18, 1, 1, '2025-10-27 01:45:55', 'ENTER', 2, NULL, NULL, NULL),
(19, 1, 1, '2025-10-27 01:46:05', 'EXIT', 2, NULL, NULL, NULL),
(20, 5, 1, '2025-10-27 01:50:29', 'ENTER', 6, NULL, NULL, NULL),
(21, 5, 1, '2025-10-27 01:50:46', 'EXIT', 6, 'ABSENT', '2025-10-27 06:36:16', 3),
(22, 1, 1, '2025-10-27 05:27:01', 'ENTER', 2, NULL, NULL, NULL),
(23, 1, 1, '2025-10-27 05:29:46', 'EXIT', 2, NULL, NULL, NULL),
(24, 1, 1, '2025-10-27 05:33:09', 'ENTER', 2, NULL, NULL, NULL),
(25, 1, 1, '2025-10-27 05:34:14', 'EXIT', 2, NULL, NULL, NULL),
(26, 1, 1, '2025-10-27 06:07:32', 'ENTER', 2, NULL, NULL, NULL),
(27, 1, 1, '2025-10-27 06:07:35', 'EXIT', 2, 'PRESENT', '2025-10-27 06:10:36', 3),
(28, 7, 1, '2025-10-27 06:07:46', 'ENTER', 10, 'PRESENT', '2025-10-27 06:10:24', 3),
(29, 7, 1, '2025-10-27 06:07:50', 'EXIT', 10, 'LATE', '2025-10-27 06:36:16', 3),
(30, 4, 1, '2025-10-26 21:00:00', 'ENTER', NULL, 'ABSENT', '2025-10-27 06:10:36', 3),
(31, 6, 1, '2025-10-26 21:00:00', 'ENTER', NULL, 'ABSENT', '2025-10-27 06:10:36', 3),
(32, 1, 1, '2025-10-27 06:32:32', 'ENTER', 2, 'PRESENT', '2025-10-27 06:36:16', 3),
(33, 8, 1, '2025-10-27 06:32:42', 'ENTER', 11, 'EXCUSED', '2025-10-27 06:36:16', 3),
(34, 4, 1, '2025-10-26 21:00:00', 'ENTER', NULL, 'ABSENT', '2025-10-27 06:36:16', 3),
(35, 6, 1, '2025-10-26 21:00:00', 'ENTER', NULL, 'ABSENT', '2025-10-27 06:36:16', 3);

-- --------------------------------------------------------

--
-- Table structure for table `attendance_summary`
--

DROP TABLE IF EXISTS `attendance_summary`;
CREATE TABLE `attendance_summary` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `report_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `location` varchar(120) NOT NULL,
  `status` varchar(50) NOT NULL,
  `actual_entry_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
CREATE TABLE `card` (
  `id` int(11) NOT NULL,
  `card_uid` varchar(50) NOT NULL,
  `issued_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `status` enum('ACTIVE','INACTIVE','LOST','DAMAGED') NOT NULL,
  `student_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `card`
--

INSERT INTO `card` (`id`, `card_uid`, `issued_at`, `expires_at`, `status`, `student_id`) VALUES
(2, 'BAB9C501', '2025-10-23 00:00:00', NULL, 'ACTIVE', 1),
(4, '1D0B65E00B1080', '2025-10-23 00:00:00', NULL, 'ACTIVE', NULL),
(5, '1D0A65E00B1080', '2025-10-23 00:00:00', NULL, 'ACTIVE', 4),
(6, '1D0965E00B1080', '2025-10-27 00:00:00', NULL, 'DAMAGED', 5),
(7, '1D0865E00B1080', '2025-10-27 00:00:00', NULL, 'INACTIVE', NULL),
(10, '1D0765E00B1080', '2025-10-27 00:00:00', NULL, 'ACTIVE', 7),
(11, '1D0565E00B1080', '2025-10-27 00:00:00', NULL, 'ACTIVE', 8);

-- --------------------------------------------------------

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `id` int(11) NOT NULL,
  `serial_number` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `added_at` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `status` enum('ONLINE','OFFLINE','DISABLED','ERROR','MAINTENANCE') NOT NULL,
  `manager_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `device`
--

INSERT INTO `device` (`id`, `serial_number`, `name`, `location`, `added_at`, `last_seen`, `status`, `manager_id`) VALUES
(1, 'ESP32_LAB_001', 'ESP32_LAB_001', 'مختبر الكيمياء', '2025-10-23 05:45:45', '2025-10-27 06:32:42', 'ONLINE', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `excuse`
--

DROP TABLE IF EXISTS `excuse`;
CREATE TABLE `excuse` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `date_of_absence` date NOT NULL,
  `reason` text NOT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `status` enum('PENDING','APPROVED','REJECTED') NOT NULL,
  `reviewer_id` int(11) DEFAULT NULL,
  `review_notes` text DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `excuse`
--

INSERT INTO `excuse` (`id`, `student_id`, `date_of_absence`, `reason`, `submitted_at`, `status`, `reviewer_id`, `review_notes`, `reviewed_at`) VALUES
(1, 1, '2025-10-23', 'صار علي حادث مروري استاذي الفاضل \r\nقبكمتلبكمسل\r\nلنمكيبقستل\r\n', '2025-10-23 06:39:25', 'APPROVED', 3, 'تم السماح', '2025-10-23 06:52:41'),
(2, 7, '2025-10-27', 'تجربة ارسال الاعذار الى الاعظاء هيئة التدريس ', '2025-10-27 06:11:18', 'REJECTED', 3, '', '2025-10-27 06:11:54'),
(3, 8, '2025-10-27', 'االتأخر بسبب زحمة الطريق ', '2025-10-27 06:37:32', 'APPROVED', 3, '', '2025-10-27 06:39:40');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `status` enum('UNREAD','READ') NOT NULL,
  `type` enum('GENERAL','ATTENDANCE_UPDATE','EXCUSE_STATUS') NOT NULL,
  `link` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`id`, `sender_id`, `receiver_id`, `message`, `timestamp`, `status`, `type`, `link`) VALUES
(1, 3, 2, 'تم تحديث حالة حضورك بتاريخ 2025-10-23 إلى \'غائب\'.', '2025-10-23 21:22:04', 'READ', 'ATTENDANCE_UPDATE', NULL),
(2, 2, 3, 'تم تقديم عذر جديد من الطالب ahmed2225 A5لdel لتاريخ 2025-10-23.', '2025-10-23 06:39:25', 'UNREAD', 'EXCUSE_STATUS', NULL),
(3, 3, 2, 'تم قبول عذرك لغياب بتاريخ 2025-10-23.', '2025-10-23 09:52:41', 'READ', '', '/student/my_attendance'),
(4, 3, 5, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'غائب\'.', '2025-10-27 06:10:36', 'UNREAD', 'ATTENDANCE_UPDATE', NULL),
(5, 3, 7, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'غائب\'.', '2025-10-27 06:10:36', 'UNREAD', 'ATTENDANCE_UPDATE', NULL),
(6, 8, 3, 'تم تقديم عذر جديد من الطالب badir aljasir لتاريخ 2025-10-27.', '2025-10-27 06:11:18', 'UNREAD', 'EXCUSE_STATUS', NULL),
(7, 3, 8, 'تم رفض عذرك لغياب بتاريخ 2025-10-27.', '2025-10-27 06:11:54', 'UNREAD', '', '/student/my_attendance'),
(8, 3, 5, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'غائب\'.', '2025-10-27 06:36:16', 'UNREAD', 'ATTENDANCE_UPDATE', NULL),
(9, 3, 7, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'غائب\'.', '2025-10-27 06:36:16', 'UNREAD', 'ATTENDANCE_UPDATE', NULL),
(10, 3, 8, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'متأخر\'.', '2025-10-27 06:36:16', 'UNREAD', 'ATTENDANCE_UPDATE', NULL),
(11, 3, 9, 'تم تحديث حالة حضورك بتاريخ 2025-10-27 إلى \'غائب\'.', '2025-10-27 21:36:16', 'READ', 'ATTENDANCE_UPDATE', NULL),
(12, 9, 3, 'تم تقديم عذر جديد من الطالب faisal ahmed لتاريخ 2025-10-27.', '2025-10-27 06:37:32', 'UNREAD', 'EXCUSE_STATUS', NULL),
(13, 3, 9, 'تم قبول عذرك لغياب بتاريخ 2025-10-27.', '2025-10-27 09:39:40', 'READ', '', '/student/my_attendance');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `student_id_number` varchar(50) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `parent_email` varchar(120) DEFAULT NULL,
  `parent_phone_number` varchar(20) DEFAULT NULL,
  `grade` varchar(10) DEFAULT NULL,
  `major` varchar(64) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `enrollment_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`id`, `user_id`, `student_id_number`, `first_name`, `last_name`, `parent_email`, `parent_phone_number`, `grade`, `major`, `date_of_birth`, `created_at`, `updated_at`, `is_active`, `enrollment_date`) VALUES
(1, 2, '23132132153552', 'ahmed2225', 'A5لdel', 'alhabiبli142521@gmail.com', '05025557944', '6', 'امن معلومات', '2006-10-18', '2025-10-23 05:44:01', '2025-10-23 05:44:01', 1, '2025-10-23 05:44:01'),
(4, 5, '231321321355', 'Mohammed', 'al3areeg', 'abooadel1421@gmail.com', '5025557944', '6', 'امن سيبراني', '2025-10-16', '2025-10-23 07:23:44', '2025-10-23 07:23:44', 1, '2025-10-23 07:23:44'),
(5, NULL, '23132135521355', 'Mkohammed', 'al3areeg', 'abooadel1421@gmail.com', '5025557944', '6', 'يبسؤيسب', '2000-10-23', '2025-10-27 01:47:53', '2025-10-27 01:47:53', 1, '2025-10-27 01:47:53'),
(6, 7, '2313213213545', 'khaled', 'alfaris', 'abooeadel1421@gmail.com', '5025557944', '6', 'امن سيبراني', '2000-10-23', '2025-10-27 01:55:22', '2025-10-27 01:55:22', 1, '2025-10-27 01:55:22'),
(7, 8, '231321321374', 'badir', 'aljasir', 'abooadelf1421@gmail.com', '050599988', '6', 'هندسة حاسب', '2009-10-22', '2025-10-27 06:02:27', '2025-10-27 06:02:27', 1, '2025-10-27 06:02:27'),
(8, 9, '231325413215355', 'faisal', 'ahmed', 'alprinads@gmail.com', '0502557484', '5', 'طب', '2000-10-25', '2025-10-27 06:30:13', '2025-10-27 06:30:13', 1, '2025-10-27 06:30:13');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(64) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role` enum('ADMIN','TEACHER','STUDENT') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`, `last_seen`) VALUES
(1, 'admin', 'admin@example.com', 'pbkdf2:sha256:600000$KqRx8YmJ5UwJLNBr$d6cfb84a76ddc7d331802703426a9a40345c4e17d5402968dc35f6bffd2f5aa2', 'ADMIN', '2025-10-23 05:40:20', NULL),
(2, 'student1', 'aboioadel1421@gmail.com', 'pbkdf2:sha256:600000$u2zhslyVwopH21Yd$233e4954d87f00eee9b96c1d13c2a4833c37489dd78c7b98c41de75a4750f90f', 'STUDENT', '2025-10-23 05:43:50', NULL),
(3, 'teacher2', 'sadaskjdm@gmail.com', 'pbkdf2:sha256:600000$hZrxMhvn9z3TiwAD$b7b94101504c7096a9ca28b5b338b171bd3f407972649024ef0ec2687af86a39', 'TEACHER', '2025-10-23 05:57:42', NULL),
(5, 'student3', 'sdfdsf@gmail.com', 'pbkdf2:sha256:600000$fogSWFWrbFfUfqTj$c0ac96eed21f6b6635c19ddfa84435dd7af103dd192da18b4ce86cbef209f9cc', 'STUDENT', '2025-10-23 07:13:46', NULL),
(6, 'student4', 'dtgsdfdg@gmail.com', 'pbkdf2:sha256:600000$wlZFALBnwlqGsmXK$f4decd58374bbec84dd447425db4dd8f25372989cfbad0a3776a4605498748a4', 'STUDENT', '2025-10-27 01:48:30', NULL),
(7, 'student5', 'sadasksjdm@gmail.com', 'pbkdf2:sha256:600000$OqKkaVp6cnw9UKNm$dbb9328f4f668a2a8ea4482d840a14db2b75e82060f7a0ad3bce639003a6debf', 'STUDENT', '2025-10-27 01:54:39', NULL),
(8, 'student7', 'dtgsdffdg@gmail.com', 'pbkdf2:sha256:600000$v1aB7H2lIds1lhxx$eb3ad1741fe24705f58ae6bb4382186117d12d37b851ac18cf025fc2a5fc572e', 'STUDENT', '2025-10-27 06:01:03', NULL),
(9, 'student8', 'dtgsdfddsg@gmail.com', 'pbkdf2:sha256:600000$M5Ry76YDWD1j3eri$fb0c7ec8524539825c35943ea73358129496f49ca68bb886a78adbe9eb3371ea', 'STUDENT', '2025-10-27 06:29:04', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `attendance_log`
--
ALTER TABLE `attendance_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_id` (`device_id`),
  ADD KEY `report_generated_by` (`report_generated_by`),
  ADD KEY `card_id` (`card_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `attendance_summary`
--
ALTER TABLE `attendance_summary`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `_student_attendance_summary_uc` (`student_id`,`report_date`,`start_time`,`location`);

--
-- Indexes for table `card`
--
ALTER TABLE `card`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_card_card_uid` (`card_uid`),
  ADD UNIQUE KEY `ix_card_student_id` (`student_id`);

--
-- Indexes for table `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_device_serial_number` (`serial_number`),
  ADD KEY `manager_id` (`manager_id`);

--
-- Indexes for table `excuse`
--
ALTER TABLE `excuse`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reviewer_id` (`reviewer_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_student_student_id_number` (`student_id_number`),
  ADD UNIQUE KEY `ix_student_user_id` (`user_id`),
  ADD KEY `ix_student_parent_email` (`parent_email`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_user_email` (`email`),
  ADD UNIQUE KEY `ix_user_username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_log`
--
ALTER TABLE `attendance_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `attendance_summary`
--
ALTER TABLE `attendance_summary`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `card`
--
ALTER TABLE `card`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `device`
--
ALTER TABLE `device`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `excuse`
--
ALTER TABLE `excuse`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance_log`
--
ALTER TABLE `attendance_log`
  ADD CONSTRAINT `attendance_log_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`),
  ADD CONSTRAINT `attendance_log_ibfk_3` FOREIGN KEY (`report_generated_by`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `attendance_log_ibfk_5` FOREIGN KEY (`card_id`) REFERENCES `card` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `attendance_log_ibfk_6` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `attendance_summary`
--
ALTER TABLE `attendance_summary`
  ADD CONSTRAINT `attendance_summary_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`);

--
-- Constraints for table `card`
--
ALTER TABLE `card`
  ADD CONSTRAINT `card_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`);

--
-- Constraints for table `device`
--
ALTER TABLE `device`
  ADD CONSTRAINT `device_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `excuse`
--
ALTER TABLE `excuse`
  ADD CONSTRAINT `excuse_ibfk_1` FOREIGN KEY (`reviewer_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `excuse_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `notification_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
