-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Мар 30 2026 г., 20:51
-- Версия сервера: 10.8.4-MariaDB
-- Версия PHP: 8.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `tramplin`
--

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_permission`
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
(25, 'Can add opportunity', 7, 'add_opportunity'),
(26, 'Can change opportunity', 7, 'change_opportunity'),
(27, 'Can delete opportunity', 7, 'delete_opportunity'),
(28, 'Can view opportunity', 7, 'view_opportunity'),
(29, 'Can add application', 8, 'add_application'),
(30, 'Can change application', 8, 'change_application'),
(31, 'Can delete application', 8, 'delete_application'),
(32, 'Can view application', 8, 'view_application'),
(33, 'Can add recommendation', 9, 'add_recommendation'),
(34, 'Can change recommendation', 9, 'change_recommendation'),
(35, 'Can delete recommendation', 9, 'delete_recommendation'),
(36, 'Can view recommendation', 9, 'view_recommendation'),
(37, 'Can add contact', 10, 'add_contact'),
(38, 'Can change contact', 10, 'change_contact'),
(39, 'Can delete contact', 10, 'delete_contact'),
(40, 'Can view contact', 10, 'view_contact'),
(41, 'Can add company review', 11, 'add_companyreview'),
(42, 'Can change company review', 11, 'change_companyreview'),
(43, 'Can delete company review', 11, 'delete_companyreview'),
(44, 'Can view company review', 11, 'view_companyreview'),
(45, 'Can add company profile', 12, 'add_companyprofile'),
(46, 'Can change company profile', 12, 'change_companyprofile'),
(47, 'Can delete company profile', 12, 'delete_companyprofile'),
(48, 'Can view company profile', 12, 'view_companyprofile'),
(49, 'Can add Мероприятие', 13, 'add_eventproxy'),
(50, 'Can change Мероприятие', 13, 'change_eventproxy'),
(51, 'Can delete Мероприятие', 13, 'delete_eventproxy'),
(52, 'Can view Мероприятие', 13, 'view_eventproxy'),
(53, 'Can add Стажировка', 14, 'add_internshipproxy'),
(54, 'Can change Стажировка', 14, 'change_internshipproxy'),
(55, 'Can delete Стажировка', 14, 'delete_internshipproxy'),
(56, 'Can view Стажировка', 14, 'view_internshipproxy'),
(57, 'Can add Вакансия', 15, 'add_vacancyproxy'),
(58, 'Can change Вакансия', 15, 'change_vacancyproxy'),
(59, 'Can delete Вакансия', 15, 'delete_vacancyproxy'),
(60, 'Can view Вакансия', 15, 'view_vacancyproxy'),
(61, 'Can add message', 16, 'add_message'),
(62, 'Can change message', 16, 'change_message'),
(63, 'Can delete message', 16, 'delete_message'),
(64, 'Can view message', 16, 'view_message'),
(65, 'Can add Заявка на менторство', 17, 'add_mentorapplication'),
(66, 'Can change Заявка на менторство', 17, 'change_mentorapplication'),
(67, 'Can delete Заявка на менторство', 17, 'delete_mentorapplication'),
(68, 'Can view Заявка на менторство', 17, 'view_mentorapplication'),
(69, 'Can add Профиль куратора', 18, 'add_curatorprofile'),
(70, 'Can change Профиль куратора', 18, 'change_curatorprofile'),
(71, 'Can delete Профиль куратора', 18, 'delete_curatorprofile'),
(72, 'Can view Профиль куратора', 18, 'view_curatorprofile'),
(73, 'Can add Запись журнала модерации', 19, 'add_moderationlog'),
(74, 'Can change Запись журнала модерации', 19, 'change_moderationlog'),
(75, 'Can delete Запись журнала модерации', 19, 'delete_moderationlog'),
(76, 'Can view Запись журнала модерации', 19, 'view_moderationlog');

-- --------------------------------------------------------

--
-- Структура таблицы `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(8, 'tramplin', 'application'),
(12, 'tramplin', 'companyprofile'),
(11, 'tramplin', 'companyreview'),
(10, 'tramplin', 'contact'),
(18, 'tramplin', 'curatorprofile'),
(13, 'tramplin', 'eventproxy'),
(14, 'tramplin', 'internshipproxy'),
(17, 'tramplin', 'mentorapplication'),
(16, 'tramplin', 'message'),
(19, 'tramplin', 'moderationlog'),
(7, 'tramplin', 'opportunity'),
(9, 'tramplin', 'recommendation'),
(6, 'tramplin', 'user'),
(15, 'tramplin', 'vacancyproxy');

-- --------------------------------------------------------

--
-- Структура таблицы `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-03-28 16:36:13.712267'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-03-28 16:36:13.760453'),
(3, 'auth', '0001_initial', '2026-03-28 16:36:13.871023'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-03-28 16:36:13.893889'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-03-28 16:36:13.896630'),
(6, 'auth', '0004_alter_user_username_opts', '2026-03-28 16:36:13.899750'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-03-28 16:36:13.902355'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-03-28 16:36:13.903400'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-03-28 16:36:13.912963'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-03-28 16:36:13.916167'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-03-28 16:36:13.918761'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-03-28 16:36:13.931220'),
(13, 'auth', '0011_update_proxy_permissions', '2026-03-28 16:36:13.934472'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-03-28 16:36:13.937592'),
(15, 'tramplin', '0001_initial', '2026-03-28 16:36:14.068590'),
(16, 'admin', '0001_initial', '2026-03-28 16:36:14.119160'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-03-28 16:36:14.123999'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-28 16:36:14.127637'),
(19, 'sessions', '0001_initial', '2026-03-28 16:36:14.149073'),
(20, 'tramplin', '0002_user_about_user_company_description_and_more', '2026-03-28 16:36:14.453015'),
(21, 'tramplin', '0003_user_favorite_ids_user_is_profile_public_and_more', '2026-03-28 16:36:14.621528'),
(22, 'tramplin', '0004_company_profile_and_reviews', '2026-03-28 16:54:54.479662'),
(23, 'tramplin', '0005_add_curator_role_and_block', '2026-03-28 17:17:06.119835'),
(24, 'tramplin', '0006_add_moderation_status_to_opportunity', '2026-03-28 17:32:49.929326'),
(25, 'tramplin', '0007_add_coordinates_to_opportunity_and_company', '2026-03-28 18:18:38.311940'),
(26, 'tramplin', '0008_contact_status', '2026-03-29 16:28:37.077356'),
(27, 'tramplin', '0009_message', '2026-03-29 16:32:03.364258'),
(28, 'tramplin', '0010_add_mentor_application', '2026-03-29 17:38:00.385727'),
(29, 'tramplin', '0011_add_is_mentor_flag', '2026-03-29 17:48:22.258736'),
(30, 'tramplin', '0012_mentor_status_and_activity', '2026-03-29 18:16:37.690015'),
(31, 'tramplin', '0013_add_avatar_to_user', '2026-03-29 18:28:19.646575'),
(32, 'tramplin', '0014_add_curator_profile_and_moderation_log', '2026-03-30 16:48:04.438160'),
(33, 'tramplin', '0015_add_block_details', '2026-03-30 16:48:04.498165'),
(34, 'tramplin', '0016_opportunity_submissions_and_postal', '2026-06-04 21:00:00.000000');

-- --------------------------------------------------------

--
-- Структура таблицы `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3jt5havcpzas7twkbke8345vrwnt4gal', '.eJxVjMsOwiAQRf9l1oZQHoW6dO83kBkYLWrAlDbRGP9dm3TT7T3n3A-Exq3lWgK_nnl6w1EeIOAyj2FpPIWc4AgKdhthvHNZQbphuVYRa5mnTGJVxEabONfEj9Pm7g5GbOO_7tnjQOx0kkj9YDvtSaFXhgeSyTE7G40lGTUad2FC3RnLrDqHWirj4fsDGz0_NQ:1w7Fbr:tYClGeWgu1LmMLCzNdzwdqirsp9nxCWF8R40HBKCBoI', '2026-04-13 16:37:03.188174'),
('5vi10jrukkqghsac5u2i0su8quknbtth', '.eJxVjMkOwiAURf-FtSHIYIele7-B8AYsasBAm2iM_65Nuun2nnPuR_jGraWSPb-eqb7FqA7Ch2We_NK4-kRiFEbsNgh457wCuoV8LRJLnmsCuSpyo01eCvHjvLm7gym06V8DdzZEE2AYOoUIvSZEIhMUuxMqtNwbsJqdi0AqOtJHxcYapAF0H5X4_gBF4kBM:1w6vEL:YqNpTKiDxMlO_QSgqEaz4EhbaKqQAZFKjZiMIyl0q-U', '2026-04-12 18:51:25.546826'),
('h7f5634stgw8uj9hzp6n2ny23njp2ah8', '.eJxVjMsOwiAURP-FtSE8Srh06d5vIBe4WtSAgTbRGP_dNummy5lzZr7Md-o91-Lp_crtw0ZxYh6XefJLp-ZzYiOT7NAFjA8qG0h3LLfKYy1zy4FvCt9p55ea6Hne3cPBhH1a11oaQjBRinQFbdYEWkDUoMFJKTBBcEEMympCBGdIKqucsnGwQYgY2O8P5FA-FQ:1w6sOf:lPlNlvO9hZ39-dEwvk-PxrHgZwiMV0mhFec6ZlvPe80', '2026-04-12 15:49:53.045689'),
('i1ecjrtxq7051thtzecykuueq8778bae', '.eJxVjMsOwiAQRf9l1oZQHoW6dO83kBkYLWrAlDbRGP9dm3TT7T3n3A-Exq3lWgK_nnl6w1EeIOAyj2FpPIWc4AgKdhthvHNZQbphuVYRa5mnTGJVxEabONfEj9Pm7g5GbOO_7tnjQOx0kkj9YDvtSaFXhgeSyTE7G40lGTUad2FC3RnLrDqHWirj4fsDGz0_NQ:1w6YVx:HbYjzmgtqktf4xc6Lv4wHfQ-RTdA1j-xBCx3Ekdkg4s', '2026-04-11 18:36:05.915807');

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_application`
--

CREATE TABLE `tramplin_application` (
  `id` bigint(20) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cover_letter` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `applicant_id` bigint(20) NOT NULL,
  `opportunity_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_application`
--

INSERT INTO `tramplin_application` (`id`, `status`, `cover_letter`, `created_at`, `applicant_id`, `opportunity_id`) VALUES
(1, 'reserve', 'привет пупсики', '2026-03-29 16:01:01.586862', 1, 2),
(2, 'accepted', '', '2026-03-29 16:48:51.286434', 4, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_companyprofile`
--

CREATE TABLE `tramplin_companyprofile` (
  `id` bigint(20) NOT NULL,
  `cover_image_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tech_stack_json` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `values_json` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `perks_json` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `linkedin_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telegram_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `vk_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `office_address` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `founded_year` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `team_size` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `employer_id` bigint(20) NOT NULL,
  `office_latitude` double DEFAULT NULL,
  `office_longitude` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_companyprofile`
--

INSERT INTO `tramplin_companyprofile` (`id`, `cover_image_url`, `tech_stack_json`, `values_json`, `perks_json`, `linkedin_url`, `telegram_url`, `vk_url`, `office_address`, `founded_year`, `team_size`, `employer_id`, `office_latitude`, `office_longitude`) VALUES
(1, 'https://ru.freepik.com/free-photo/high-angle-shot-lake-surrounded-by-green-mountains-covered-fog-cloudy-sky_10809983.htm#fromView=keyword&page=1&position=0&uuid=a31a65fd-5d4c-44d8-b379-b8a039ea34fa&qu', '{пупупу}', '[пупупу]', '[пупупу]', '', '', '', '3-й Кадашевский пер., ДОМ 8, Москва, Россия, 115035', '2010', '100', 3, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_companyreview`
--

CREATE TABLE `tramplin_companyreview` (
  `id` bigint(20) NOT NULL,
  `rating` smallint(5) UNSIGNED NOT NULL CHECK (`rating` >= 0),
  `text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `vacancy_tag` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_moderated` tinyint(1) NOT NULL,
  `author_id` bigint(20) NOT NULL,
  `company_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_companyreview`
--

INSERT INTO `tramplin_companyreview` (`id`, `rating`, `text`, `vacancy_tag`, `created_at`, `is_moderated`, `author_id`, `company_id`) VALUES
(1, 5, 'фывфывфыв', 'фывфыв', '2026-03-28 17:38:19.136556', 1, 2, 3),
(2, 5, 'ввввввв', 'ффффф', '2026-03-29 16:04:16.464539', 1, 4, 3);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_contact`
--

CREATE TABLE `tramplin_contact` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `from_user_id` bigint(20) NOT NULL,
  `to_user_id` bigint(20) NOT NULL,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_contact`
--

INSERT INTO `tramplin_contact` (`id`, `created_at`, `from_user_id`, `to_user_id`, `status`) VALUES
(4, '2026-03-29 16:37:15.262914', 5, 4, 'accepted'),
(5, '2026-03-29 17:53:56.540658', 1, 4, 'accepted'),
(6, '2026-03-29 18:19:12.831578', 4, 5, 'accepted');

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_curatorprofile`
--

CREATE TABLE `tramplin_curatorprofile` (
  `id` bigint(20) NOT NULL,
  `responsibility_area` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `availability_schedule` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_mentors_count` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_curatorprofile`
--

INSERT INTO `tramplin_curatorprofile` (`id`, `responsibility_area`, `availability_schedule`, `approved_mentors_count`, `user_id`) VALUES
(1, '', '', 0, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_mentorapplication`
--

CREATE TABLE `tramplin_mentorapplication` (
  `id` bigint(20) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `experience_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `skills_to_teach` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied_at` datetime(6) NOT NULL,
  `accepted_privacy_policy` tinyint(1) NOT NULL,
  `accepted_terms_of_service` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_mentorapplication`
--

INSERT INTO `tramplin_mentorapplication` (`id`, `status`, `experience_description`, `skills_to_teach`, `applied_at`, `accepted_privacy_policy`, `accepted_terms_of_service`, `user_id`) VALUES
(1, 'approved', 'люблю кушать картошку фри, и ходить в кино', 'гта 5', '2026-03-29 17:50:24.258497', 1, 1, 4);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_message`
--

CREATE TABLE `tramplin_message` (
  `id` bigint(20) NOT NULL,
  `text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_attachment` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `sender_id` bigint(20) NOT NULL,
  `receiver_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_message`
--

INSERT INTO `tramplin_message` (`id`, `text`, `file_attachment`, `timestamp`, `is_read`, `sender_id`, `receiver_id`) VALUES
(1, 'привет', '', '2026-03-29 16:34:45.523699', 1, 4, 1),
(2, '', 'chat_attachments/2026/03/2.webp', '2026-03-29 16:34:52.353163', 1, 4, 1),
(3, 'хай пуп', '', '2026-03-29 16:35:35.622456', 1, 1, 4),
(4, 'привет машка', '', '2026-03-29 16:39:32.479702', 1, 5, 4),
(5, 'скинь трусики', '', '2026-03-29 16:39:34.916170', 1, 5, 4),
(6, '', 'chat_attachments/2026/03/2_cNecPZn.webp', '2026-03-29 16:39:39.204009', 1, 5, 4),
(7, '', 'chat_attachments/2026/03/УП.Тасуев.docx', '2026-03-29 16:39:56.421320', 1, 5, 4),
(8, '', 'chat_attachments/2026/03/voice_1774803862762.webm', '2026-03-29 17:04:22.770241', 1, 4, 1),
(9, '', 'chat_attachments/2026/03/voice_1774803884379.webm', '2026-03-29 17:04:44.383865', 1, 4, 1),
(10, '', 'chat_attachments/2026/03/voice_1774803986646.webm', '2026-03-29 17:06:26.653535', 1, 1, 4),
(11, 'Здравствуйте! Я бы хотел попросить вас о менторстве по направлению Js, html, css...', '', '2026-03-29 18:18:14.319225', 1, 5, 4),
(12, '', 'chat_attachments/2026/03/voice_1774808298065.webm', '2026-03-29 18:18:18.071197', 1, 5, 4),
(13, 'привет', '', '2026-03-29 18:19:24.472719', 0, 4, 5),
(14, 'я помогу тебе', '', '2026-03-29 18:19:28.149867', 0, 4, 5),
(15, 'првиет машка', '', '2026-03-29 18:38:25.183398', 0, 1, 4),
(16, 'как дела', '', '2026-03-29 18:38:27.442240', 0, 1, 4);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_moderationlog`
--

CREATE TABLE `tramplin_moderationlog` (
  `id` bigint(20) NOT NULL,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target_description` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `curator_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_moderationlog`
--

INSERT INTO `tramplin_moderationlog` (`id`, `action`, `target_description`, `created_at`, `curator_id`) VALUES
(2, 'approve_opportunity', 'ннннннн (ООО Работа)', '2026-03-30 16:58:48.497640', 2);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_opportunity`
--

CREATE TABLE `tramplin_opportunity` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `format` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `salary` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `requirements` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `skills_required` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` date DEFAULT NULL,
  `employer_id` bigint(20) NOT NULL,
  `moderation_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `postal_code` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `company_display` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_opportunity`
--

INSERT INTO `tramplin_opportunity` (`id`, `title`, `type`, `format`, `status`, `salary`, `location`, `description`, `requirements`, `skills_required`, `created_at`, `expires_at`, `employer_id`, `moderation_status`, `latitude`, `longitude`) VALUES
(1, 'стрип', 'vacancy', 'remote', 'active', '1000000', '3-й Кадашевский пер., ДОМ 8, Москва, Россия, 115035', 'пупупу', 'пупупу', 'пупупу', '2026-03-28 17:01:36.820055', NULL, 3, 'approved', 55.7422356, 37.6233071),
(2, 'Doika', 'internship', 'office', 'active', '100', 'Излучинск', 'Доить тити коров', '4 класса, садик', 'JavaScript, Python', '2026-03-28 17:57:15.872089', '2026-04-04', 3, 'approved', 60.956284, 76.8895405),
(3, 'Senior', 'vacancy', 'hybrid', 'active', '1233451', '3-й Кадашевский пер., ДОМ 8, Москва, Россия, 115035', 'Приходите продавайте пирожки', 'Красные трусы', 'JavaScript, Python, Go', '2026-03-28 18:23:12.131864', '2032-11-18', 3, 'approved', 55.7422356, 37.6233071),
(4, 'Чипсоеды', 'event', 'office', 'active', '', 'Нижневартовск, Дзержинского 17', 'Приходите кушать чипсы', '', '', '2026-03-28 18:35:53.137539', NULL, 3, 'approved', 60.9442667, 76.593724),
(5, 'ннннннн', 'event', 'office', 'active', '121111', 'ооооо', 'аввапаа', 'смисмисми', 'вапвапвап', '2026-03-30 16:58:02.034756', '2026-04-02', 3, 'approved', 52.145721, 21.0452112),
(6, 'фыфчуцф', 'internship', 'remote', 'planned', '12644', 'фычйыфай', 'муфывйцв', 'ваымвеы', 'цфскпыавы', '2026-03-30 16:58:33.895946', '2026-04-04', 3, 'pending', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_opportunitysubmission`
--

CREATE TABLE `tramplin_opportunitysubmission` (
  `id` bigint(20) NOT NULL,
  `company_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `format` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `salary` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `postal_code` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `requirements` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `skills_required` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` date DEFAULT NULL,
  `moderation_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_comment` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `published_opportunity_id` bigint(20) DEFAULT NULL,
  `submitter_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_recommendation`
--

CREATE TABLE `tramplin_recommendation` (
  `id` bigint(20) NOT NULL,
  `opportunity_id` int(11) NOT NULL,
  `opportunity_title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `opportunity_company` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `recipient_id` bigint(20) NOT NULL,
  `sender_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_user`
--

CREATE TABLE `tramplin_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `inn` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `corporate_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `professional_network_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_verified_employer` tinyint(1) NOT NULL,
  `about` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_industry` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_video_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_website` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `github_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `graduation_year` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `portfolio_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `skills` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `university` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `favorite_ids` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_profile_public` tinyint(1) NOT NULL,
  `blocked_reason` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_blocked` tinyint(1) NOT NULL,
  `is_mentor` tinyint(1) NOT NULL,
  `mentor_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_message_sent_at` datetime(6) DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blocked_by_id_val` int(11) DEFAULT NULL,
  `blocked_by_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `blocked_until` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `tramplin_user`
--

INSERT INTO `tramplin_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `display_name`, `inn`, `corporate_email`, `professional_network_url`, `is_verified_employer`, `about`, `company_description`, `company_industry`, `company_name`, `company_video_url`, `company_website`, `github_url`, `graduation_year`, `portfolio_url`, `skills`, `university`, `favorite_ids`, `is_profile_public`, `blocked_reason`, `is_blocked`, `is_mentor`, `mentor_status`, `last_message_sent_at`, `avatar`, `blocked_by_id_val`, `blocked_by_name`, `blocked_until`) VALUES
(1, 'pbkdf2_sha256$870000$nbKok7glFHEAou5gHxhEZx$PkcCkLse0yyqRi4R4RXnet1fIS/DPovnAYSQIiPoKEs=', '2026-03-29 18:38:15.367612', 0, 'ivan@gmail.com', '', '', 'ivan@gmail.com', 0, 1, '2026-03-28 16:37:26.737347', 'seeker', 'Иван Иванов', '', '', '', 0, '40к кубков в бравл старс', '', '', '', '', '', '', '2 курс', '', 'Html, css', 'МФТИ', '[]', 1, '', 0, 0, 'available', NULL, 'avatars/1.webp', NULL, '', NULL),
(2, 'pbkdf2_sha256$870000$rnje9k8ElBHjCqSuowR3PA$izIja0wKhCi/WaC0JwI/ThwkC6Zvo7Su13lbYzzP/Dk=', '2026-03-30 16:58:43.355543', 1, 'admin@gmail.com', '', '', 'admin@gmail.com', 1, 1, '2026-03-28 16:40:57.866944', 'seeker', '', '', '', '', 0, '', '', '', '', '', '', '', '', '', '', '', '[]', 0, '', 0, 0, 'available', NULL, NULL, NULL, '', NULL),
(3, 'pbkdf2_sha256$870000$8BLNb7EAk7rAk0IrFSKpPi$sc67GGzinzCQO2Iz4kJLFeUqGw3ebbeFvN6QzqlCmTg=', '2026-03-30 16:57:27.380500', 0, 'rabota@gmail.com', '', '', 'rabota@gmail.com', 0, 1, '2026-03-28 16:58:04.391446', 'employer', 'Работа', '1234567899', 'rabota1@gmail.com', '', 1, '', '', '', 'ООО Работа', '', '', '', '', '', '', '', '[]', 0, '', 0, 0, 'available', NULL, NULL, NULL, '', NULL),
(4, 'pbkdf2_sha256$870000$s297jIRg4cjMORSuL17EmP$XrZRFVo4jO2bbMOmhmO7SxR1pyFjAeZXtOJHrwdK7q4=', '2026-03-29 18:50:21.752947', 0, 'masha@gmail.com', '', '', 'masha@gmail.com', 0, 1, '2026-03-29 16:03:04.939224', 'seeker', 'masha', '', '', '', 0, 'Я люблю готовить пряники', '', '', '', '', '', '', '4 курс', '', 'Js, html, css', 'МГУ', '[]', 1, '', 0, 1, 'available', '2026-03-29 18:19:28.149867', 'avatars/2.webp', NULL, '', NULL),
(5, 'pbkdf2_sha256$870000$HLgQFnqeFVVeDQ2AvnCZG9$jlIU3ZwbN69RtDzgzIFrxi5E0SVH3lYyQkhOtikoRhE=', '2026-03-29 18:17:50.165892', 0, 'gosha@gmail.com', '', '', 'gosha@gmail.com', 0, 1, '2026-03-29 16:37:00.599982', 'seeker', 'Гоша', '', '', '', 0, '', '', '', '', '', '', '', '', '', '', '', '[]', 1, '', 0, 0, 'available', NULL, NULL, NULL, '', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_user_groups`
--

CREATE TABLE `tramplin_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tramplin_user_user_permissions`
--

CREATE TABLE `tramplin_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индексы таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_tramplin_user_id` (`user_id`);

--
-- Индексы таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индексы таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Индексы таблицы `tramplin_application`
--
ALTER TABLE `tramplin_application`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tramplin_application_opportunity_id_applicant_id_566225de_uniq` (`opportunity_id`,`applicant_id`),
  ADD KEY `tramplin_application_applicant_id_0dc0d225_fk_tramplin_user_id` (`applicant_id`);

--
-- Индексы таблицы `tramplin_companyprofile`
--
ALTER TABLE `tramplin_companyprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `employer_id` (`employer_id`);

--
-- Индексы таблицы `tramplin_companyreview`
--
ALTER TABLE `tramplin_companyreview`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tramplin_companyreview_company_id_author_id_30ef7dd8_uniq` (`company_id`,`author_id`),
  ADD KEY `tramplin_companyreview_author_id_22edf717_fk_tramplin_user_id` (`author_id`);

--
-- Индексы таблицы `tramplin_contact`
--
ALTER TABLE `tramplin_contact`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tramplin_contact_from_user_id_to_user_id_db6f22ab_uniq` (`from_user_id`,`to_user_id`),
  ADD KEY `tramplin_contact_to_user_id_0021b5ee_fk_tramplin_user_id` (`to_user_id`);

--
-- Индексы таблицы `tramplin_curatorprofile`
--
ALTER TABLE `tramplin_curatorprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Индексы таблицы `tramplin_mentorapplication`
--
ALTER TABLE `tramplin_mentorapplication`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `tramplin_mentorapplication_status_5b0b54b6` (`status`);

--
-- Индексы таблицы `tramplin_message`
--
ALTER TABLE `tramplin_message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tramplin_message_sender_id_968ce2ec_fk_tramplin_user_id` (`sender_id`),
  ADD KEY `tramplin_message_receiver_id_99b82e1c_fk_tramplin_user_id` (`receiver_id`);

--
-- Индексы таблицы `tramplin_moderationlog`
--
ALTER TABLE `tramplin_moderationlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tramplin_moderationlog_curator_id_3b67c0ee_fk_tramplin_user_id` (`curator_id`);

--
-- Индексы таблицы `tramplin_opportunity`
--
ALTER TABLE `tramplin_opportunity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tramplin_opportunity_employer_id_6a2dcd20_fk_tramplin_user_id` (`employer_id`);

--
-- Индексы таблицы `tramplin_recommendation`
--
ALTER TABLE `tramplin_recommendation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tramplin_recommendat_recipient_id_5025cefb_fk_tramplin_` (`recipient_id`),
  ADD KEY `tramplin_recommendation_sender_id_60dfc682_fk_tramplin_user_id` (`sender_id`);

--
-- Индексы таблицы `tramplin_user`
--
ALTER TABLE `tramplin_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `tramplin_user_is_mentor_9318351e` (`is_mentor`),
  ADD KEY `tramplin_user_mentor_status_43ce6568` (`mentor_status`);

--
-- Индексы таблицы `tramplin_user_groups`
--
ALTER TABLE `tramplin_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tramplin_user_groups_user_id_group_id_359ba740_uniq` (`user_id`,`group_id`),
  ADD KEY `tramplin_user_groups_group_id_3ea6cad1_fk_auth_group_id` (`group_id`);

--
-- Индексы таблицы `tramplin_user_user_permissions`
--
ALTER TABLE `tramplin_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tramplin_user_user_permi_user_id_permission_id_935adb49_uniq` (`user_id`,`permission_id`),
  ADD KEY `tramplin_user_user_p_permission_id_ddb09ef5_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT для таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT для таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT для таблицы `tramplin_application`
--
ALTER TABLE `tramplin_application`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `tramplin_companyprofile`
--
ALTER TABLE `tramplin_companyprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `tramplin_companyreview`
--
ALTER TABLE `tramplin_companyreview`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `tramplin_contact`
--
ALTER TABLE `tramplin_contact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `tramplin_curatorprofile`
--
ALTER TABLE `tramplin_curatorprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `tramplin_mentorapplication`
--
ALTER TABLE `tramplin_mentorapplication`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `tramplin_message`
--
ALTER TABLE `tramplin_message`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT для таблицы `tramplin_moderationlog`
--
ALTER TABLE `tramplin_moderationlog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `tramplin_opportunity`
--
ALTER TABLE `tramplin_opportunity`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `tramplin_recommendation`
--
ALTER TABLE `tramplin_recommendation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `tramplin_user`
--
ALTER TABLE `tramplin_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `tramplin_user_groups`
--
ALTER TABLE `tramplin_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `tramplin_user_user_permissions`
--
ALTER TABLE `tramplin_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_tramplin_user_id` FOREIGN KEY (`user_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_application`
--
ALTER TABLE `tramplin_application`
  ADD CONSTRAINT `tramplin_application_applicant_id_0dc0d225_fk_tramplin_user_id` FOREIGN KEY (`applicant_id`) REFERENCES `tramplin_user` (`id`),
  ADD CONSTRAINT `tramplin_application_opportunity_id_f31ac2ca_fk_tramplin_` FOREIGN KEY (`opportunity_id`) REFERENCES `tramplin_opportunity` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_companyprofile`
--
ALTER TABLE `tramplin_companyprofile`
  ADD CONSTRAINT `tramplin_companyprofile_employer_id_43b48ae6_fk_tramplin_user_id` FOREIGN KEY (`employer_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_companyreview`
--
ALTER TABLE `tramplin_companyreview`
  ADD CONSTRAINT `tramplin_companyreview_author_id_22edf717_fk_tramplin_user_id` FOREIGN KEY (`author_id`) REFERENCES `tramplin_user` (`id`),
  ADD CONSTRAINT `tramplin_companyreview_company_id_ab5dd5f2_fk_tramplin_user_id` FOREIGN KEY (`company_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_contact`
--
ALTER TABLE `tramplin_contact`
  ADD CONSTRAINT `tramplin_contact_from_user_id_dd76f02d_fk_tramplin_user_id` FOREIGN KEY (`from_user_id`) REFERENCES `tramplin_user` (`id`),
  ADD CONSTRAINT `tramplin_contact_to_user_id_0021b5ee_fk_tramplin_user_id` FOREIGN KEY (`to_user_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_curatorprofile`
--
ALTER TABLE `tramplin_curatorprofile`
  ADD CONSTRAINT `tramplin_curatorprofile_user_id_c9a19d83_fk_tramplin_user_id` FOREIGN KEY (`user_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_mentorapplication`
--
ALTER TABLE `tramplin_mentorapplication`
  ADD CONSTRAINT `tramplin_mentorapplication_user_id_b7cf74fc_fk_tramplin_user_id` FOREIGN KEY (`user_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_message`
--
ALTER TABLE `tramplin_message`
  ADD CONSTRAINT `tramplin_message_receiver_id_99b82e1c_fk_tramplin_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `tramplin_user` (`id`),
  ADD CONSTRAINT `tramplin_message_sender_id_968ce2ec_fk_tramplin_user_id` FOREIGN KEY (`sender_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_moderationlog`
--
ALTER TABLE `tramplin_moderationlog`
  ADD CONSTRAINT `tramplin_moderationlog_curator_id_3b67c0ee_fk_tramplin_user_id` FOREIGN KEY (`curator_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_opportunity`
--
ALTER TABLE `tramplin_opportunity`
  ADD CONSTRAINT `tramplin_opportunity_employer_id_6a2dcd20_fk_tramplin_user_id` FOREIGN KEY (`employer_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_recommendation`
--
ALTER TABLE `tramplin_recommendation`
  ADD CONSTRAINT `tramplin_recommendat_recipient_id_5025cefb_fk_tramplin_` FOREIGN KEY (`recipient_id`) REFERENCES `tramplin_user` (`id`),
  ADD CONSTRAINT `tramplin_recommendation_sender_id_60dfc682_fk_tramplin_user_id` FOREIGN KEY (`sender_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_user_groups`
--
ALTER TABLE `tramplin_user_groups`
  ADD CONSTRAINT `tramplin_user_groups_group_id_3ea6cad1_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `tramplin_user_groups_user_id_eee888b4_fk_tramplin_user_id` FOREIGN KEY (`user_id`) REFERENCES `tramplin_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `tramplin_user_user_permissions`
--
ALTER TABLE `tramplin_user_user_permissions`
  ADD CONSTRAINT `tramplin_user_user_p_permission_id_ddb09ef5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `tramplin_user_user_p_user_id_242456d3_fk_tramplin_` FOREIGN KEY (`user_id`) REFERENCES `tramplin_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
