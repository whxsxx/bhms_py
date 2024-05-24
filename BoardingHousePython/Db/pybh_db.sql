-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2024 at 08:51 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pybh_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `account_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `expense`
--

CREATE TABLE `expense` (
  `expense_id` int(11) NOT NULL,
  `expense_name` varchar(50) NOT NULL,
  `expense_amount` decimal(10,2) NOT NULL,
  `expense_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expense`
--

INSERT INTO `expense` (`expense_id`, `expense_name`, `expense_amount`, `expense_date`) VALUES
(2, 'Pasuyop og Tae', 5000.00, '2003-10-10');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_id`, `room_number`, `room_price`) VALUES
(1, '1', 2500.00),
(2, '2', 3000.00),
(3, '3', 5000.00);

-- --------------------------------------------------------

--
-- Table structure for table `tenants`
--

CREATE TABLE `tenants` (
  `tenant_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `due` date NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tenants`
--

INSERT INTO `tenants` (`tenant_id`, `first_name`, `last_name`, `address`, `date`, `due`, `room_number`, `room_price`) VALUES
(1, 'TestDaw', 'TestLangasd', 'Prk. Manatad', '2003-10-10', '2003-11-10', '1', 2500.00),
(2, 'Kurikung', 'asd', 'asd', '2024-05-24', '2024-06-24', '3', 5000.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `expense`
--
ALTER TABLE `expense`
  ADD PRIMARY KEY (`expense_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_id`),
  ADD UNIQUE KEY `room_number` (`room_number`);

--
-- Indexes for table `tenants`
--
ALTER TABLE `tenants`
  ADD PRIMARY KEY (`tenant_id`),
  ADD KEY `room_number` (`room_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `expense`
--
ALTER TABLE `expense`
  MODIFY `expense_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tenants`
--
ALTER TABLE `tenants`
  MODIFY `tenant_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tenants`
--
ALTER TABLE `tenants`
  ADD CONSTRAINT `tenants_ibfk_1` FOREIGN KEY (`room_number`) REFERENCES `rooms` (`room_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
