-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 28, 2023 at 10:53 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gentext`
--

-- --------------------------------------------------------

--
-- Table structure for table `authapi_user`
--

CREATE TABLE `authapi_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(200) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `OTP` int(11) DEFAULT NULL,
  `OTP_generation_time` datetime(6) NOT NULL,
  `meta_data` longtext DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  `login_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `authapi_user`
--

INSERT INTO `authapi_user` (`id`, `password`, `last_login`, `email`, `name`, `is_active`, `is_admin`, `OTP`, `OTP_generation_time`, `meta_data`, `remarks`, `created_at`, `updated_at`, `created_by`, `modified_by`, `image`, `login_id`) VALUES
(3, 'pbkdf2_sha256$600000$x1yaFR4S5S9XN8rptmmYkK$b69tiUOGH2AxE2uVBwQE0Z1g6tHJYwV/rkbw+9WJ7pQ=', '2023-12-19 05:18:02.887103', 'admin@gmail.com', 'admin', 1, 1, NULL, '2023-11-23 06:11:03.822748', NULL, NULL, '2023-11-23 06:11:03.822748', '2023-11-23 06:11:03.822748', NULL, NULL, NULL, 'admin@gmail.com'),
(35, 'pbkdf2_sha256$600000$Qh4J4cY01ote3Ql6TURZTP$X5v1by2LpREF+x6HvkNYW5n94PsSG+xE77L4j/6Z7tk=', '2023-12-27 10:55:16.245873', 'alamin2514@student.nstu.edu.bd', 'Al-Amin', 1, 0, 712285, '2023-12-28 11:07:20.048541', NULL, NULL, '2023-12-26 04:21:07.395836', '2023-12-26 04:21:07.395836', NULL, NULL, NULL, 'alamin');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add pdf details', 7, 'add_pdfdetails'),
(26, 'Can change pdf details', 7, 'change_pdfdetails'),
(27, 'Can delete pdf details', 7, 'delete_pdfdetails'),
(28, 'Can view pdf details', 7, 'view_pdfdetails'),
(29, 'Can add pdf files', 8, 'add_pdffiles'),
(30, 'Can change pdf files', 8, 'change_pdffiles'),
(31, 'Can delete pdf files', 8, 'delete_pdffiles'),
(32, 'Can view pdf files', 8, 'view_pdffiles');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(3, '2023-11-23 09:14:42.540440', '1', 'example.pdf - Page 1', 1, '[{\"added\": {}}]', 7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(6, 'authapi', 'user'),
(4, 'contenttypes', 'contenttype'),
(7, 'ocrapi', 'pdfdetails'),
(8, 'ocrapi', 'pdffiles'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-11-23 05:52:12.535664'),
(2, 'authapi', '0001_initial', '2023-11-23 05:52:12.809242'),
(3, 'admin', '0001_initial', '2023-11-23 05:52:15.011643'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-11-23 05:52:15.061751'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-23 05:52:15.109883'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-11-23 05:52:16.015482'),
(7, 'auth', '0001_initial', '2023-11-23 05:52:21.623138'),
(8, 'auth', '0002_alter_permission_name_max_length', '2023-11-23 05:52:22.647584'),
(9, 'auth', '0003_alter_user_email_max_length', '2023-11-23 05:52:22.699799'),
(10, 'auth', '0004_alter_user_username_opts', '2023-11-23 05:52:22.746257'),
(11, 'auth', '0005_alter_user_last_login_null', '2023-11-23 05:52:22.816763'),
(12, 'auth', '0006_require_contenttypes_0002', '2023-11-23 05:52:22.859348'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2023-11-23 05:52:22.910465'),
(14, 'auth', '0008_alter_user_username_max_length', '2023-11-23 05:52:22.994951'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2023-11-23 05:52:23.044154'),
(16, 'auth', '0010_alter_group_name_max_length', '2023-11-23 05:52:23.185438'),
(17, 'auth', '0011_update_proxy_permissions', '2023-11-23 05:52:23.244476'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2023-11-23 05:52:23.292619'),
(19, 'sessions', '0001_initial', '2023-11-23 05:52:23.833314'),
(20, 'ocrapi', '0001_initial', '2023-11-23 06:31:01.646214'),
(21, 'ocrapi', '0002_remove_pdfdetails_image_pdfdetails_image_location_and_more', '2023-12-07 02:51:38.212014'),
(22, 'ocrapi', '0003_pdffiles_total_page', '2023-12-07 03:51:08.597537'),
(23, 'ocrapi', '0004_pdffiles_total_size', '2023-12-07 04:51:59.877309'),
(24, 'ocrapi', '0005_alter_pdffiles_total_size', '2023-12-07 04:56:36.354972'),
(25, 'ocrapi', '0006_alter_pdffiles_uploaded_date', '2023-12-10 05:27:13.895601'),
(26, 'authapi', '0002_user_image_user_login_id', '2023-12-21 09:29:57.066459'),
(27, 'authapi', '0003_alter_user_login_id', '2023-12-24 03:14:51.548810'),
(28, 'ocrapi', '0007_pdffiles_uploaded_time_alter_pdffiles_uploaded_date', '2023-12-26 04:15:43.957424'),
(29, 'ocrapi', '0008_alter_pdffiles_uploaded_date', '2023-12-26 04:51:12.086701'),
(30, 'ocrapi', '0009_rename_upload_status_pdffiles_extraction_status', '2023-12-26 05:03:12.821955');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('c8r79qbx8gkmv5unfks9qrkvc9s9y1be', '.eJxVjMEOwiAQRP-FsyGypCAevfsNZJddpGogKe2p8d9tkx70MJd5b2ZVEZe5xKXLFEdWV2XV6bcjTC-pO-An1kfTqdV5Gknvij5o1_fG8r4d7t9BwV62dTbsLA2SWeDsh0DJYCZxCJDzxXtOYM0WMeIkgAdizgFJkoHk0anPFxWIOU0:1r62vl:lEM3egc8oQnBvuYwl5Jck5bKKreh7SKzVbYIXPKjVeM', '2023-12-07 06:11:17.826651'),
('l1p7lfydyeguwut0amq3a2dal1j1dmwp', '.eJxVjMEOwiAQRP-FsyGypCAevfsNZJddpGogKe2p8d9tkx70MJd5b2ZVEZe5xKXLFEdWV2XV6bcjTC-pO-An1kfTqdV5Gknvij5o1_fG8r4d7t9BwV62dTbsLA2SWeDsh0DJYCZxCJDzxXtOYM0WMeIkgAdizgFJkoHk0anPFxWIOU0:1rFSUV:b52yuPk-HSpEHHOZ48bgZzcHPUJUe2kr4oalFoA4QmQ', '2024-01-02 05:18:03.103806');

-- --------------------------------------------------------

--
-- Table structure for table `ocrapi_pdfdetails`
--

CREATE TABLE `ocrapi_pdfdetails` (
  `id` int(11) NOT NULL,
  `page_number` int(11) NOT NULL,
  `text` longtext NOT NULL,
  `meta_data` longtext DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `pdf_file_id_id` int(11) NOT NULL,
  `image_location` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ocrapi_pdffiles`
--

CREATE TABLE `ocrapi_pdffiles` (
  `id` int(11) NOT NULL,
  `pdf_file_name` varchar(255) NOT NULL,
  `uploaded_date` date NOT NULL,
  `extraction_status` varchar(20) NOT NULL,
  `meta_data` longtext DEFAULT NULL,
  `remarks` longtext DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `modified_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `modified_by` int(11) DEFAULT NULL,
  `uploaded_by_id` bigint(20) NOT NULL,
  `file_location` varchar(300) DEFAULT NULL,
  `total_page` int(11) DEFAULT NULL,
  `total_size` double DEFAULT NULL,
  `uploaded_time` time(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authapi_user`
--
ALTER TABLE `authapi_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `authapi_user_login_id_a5a8a087_uniq` (`login_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_authapi_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `ocrapi_pdfdetails`
--
ALTER TABLE `ocrapi_pdfdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ocrapi_pdfdetails_pdf_file_id_id_3448781a_fk_ocrapi_pdffiles_id` (`pdf_file_id_id`);

--
-- Indexes for table `ocrapi_pdffiles`
--
ALTER TABLE `ocrapi_pdffiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ocrapi_pdffiles_uploaded_by_id_d68a0106_fk_authapi_user_id` (`uploaded_by_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `authapi_user`
--
ALTER TABLE `authapi_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `ocrapi_pdfdetails`
--
ALTER TABLE `ocrapi_pdfdetails`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=307;

--
-- AUTO_INCREMENT for table `ocrapi_pdffiles`
--
ALTER TABLE `ocrapi_pdffiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_authapi_user_id` FOREIGN KEY (`user_id`) REFERENCES `authapi_user` (`id`);

--
-- Constraints for table `ocrapi_pdfdetails`
--
ALTER TABLE `ocrapi_pdfdetails`
  ADD CONSTRAINT `ocrapi_pdfdetails_pdf_file_id_id_3448781a_fk_ocrapi_pdffiles_id` FOREIGN KEY (`pdf_file_id_id`) REFERENCES `ocrapi_pdffiles` (`id`);

--
-- Constraints for table `ocrapi_pdffiles`
--
ALTER TABLE `ocrapi_pdffiles`
  ADD CONSTRAINT `ocrapi_pdffiles_uploaded_by_id_d68a0106_fk_authapi_user_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `authapi_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
