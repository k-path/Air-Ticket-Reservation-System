-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 09, 2022 at 05:13 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `atrs`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airlinestaff`
--

CREATE TABLE `airlinestaff` (
  `username` varchar(200) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  `fname` varchar(200) DEFAULT NULL,
  `lname` varchar(200) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airlinestaff`
--

INSERT INTO `airlinestaff` (`username`, `password`, `fname`, `lname`, `date_of_birth`, `email`) VALUES
('bobsburger', '', 'bob', 'duncan', '0000-00-00', '4refre@nyu.edu'),
('p4th', 'b3f2530d3ba6772c25be428f6597e692', 'Jerry', 'Path', '2002-12-27', 'jpath@yahoo.com');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `a_id` int(11) NOT NULL,
  `num_seats` int(11) DEFAULT NULL,
  `manufacturer` varchar(200) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `airline_name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`a_id`, `num_seats`, `manufacturer`, `age`, `airline_name`) VALUES
(1234, 50, 'Boeing', 2, 'Jet Blue'),
(2343, 540, 'Boeing', 4, 'Jet Blue'),
(3425, 520, 'Boeing', 7, 'Jet Blue'),
(4321, 500, 'Boeing', 5, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(200) NOT NULL,
  `city` varchar(200) DEFAULT NULL,
  `country` varchar(200) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `city`, `country`, `type`) VALUES
('JFK', 'NYC', 'USA', 'both'),
('LAX', 'LA', 'USA', 'both'),
('PVG', 'PVG', 'CHINA', 'both');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(200) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `building_number` decimal(10,0) DEFAULT NULL,
  `street` varchar(200) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(200) DEFAULT NULL,
  `phone_number` decimal(10,0) DEFAULT NULL,
  `passport_number` int(11) DEFAULT NULL,
  `passport_exp` date DEFAULT NULL,
  `passport_country` varchar(200) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `password`, `name`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_exp`, `passport_country`, `date_of_birth`) VALUES
('bobsburger@nyu.edu', 'ballislif33', 'Bobs Burger', '343', 'Gold St', 'Brooklyn', 'NY', '4345456784', 13, '0000-00-00', 'USA', '0000-00-00'),
('ft@aol.com', '2d061102432defe9b7be67879b999c14', 'finer things', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('gw@gmail.com', 'fb289605d3e6ba84fecb32b0aa2f83cb', 'gunnar willworks', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
('kevsapathyjr@gmail.com', '4b10c03a722acb389b47f3b29cd2dcfb', 'Kelvin Sapathy Jr', '343', 'Gold St', 'Brooklyn', 'NY', '9292629365', 12345678, '2032-07-22', 'USA', '2018-12-31'),
('kjs10010@nyu.edu', 'ballislife2', 'KJ Sapathy', '343', 'Gold St', 'Brooklyn', 'NY', '4324234444', 11, '0000-00-00', 'USA', '0000-00-00'),
('yams@nyu.edu', 'ballislife', 'Yams Gupta', '343', 'Gold St', 'Brooklyn', 'NY', '6127504936', 12, '0000-00-00', 'USA', '0000-00-00');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `flight_num` varchar(10) NOT NULL,
  `d_date` date DEFAULT NULL,
  `d_time` time DEFAULT NULL,
  `d_airport` varchar(200) DEFAULT NULL,
  `a_date` date DEFAULT NULL,
  `a_time` time DEFAULT NULL,
  `a_airport` varchar(200) DEFAULT NULL,
  `base_price` decimal(50,0) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `airline_name` varchar(200) NOT NULL,
  `a_id` decimal(20,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`flight_num`, `d_date`, `d_time`, `d_airport`, `a_date`, `a_time`, `a_airport`, `base_price`, `status`, `airline_name`, `a_id`) VALUES
('127002', '2022-12-27', '04:04:00', 'JFK', '2022-12-28', '12:04:00', 'PVG', '499', 'Delayed', 'Jet Blue', '1234'),
('127122', '2022-12-27', '04:04:00', 'JFK', '2022-12-28', '12:04:00', 'PVG', '499', 'on-time', 'Jet Blue', '2343'),
('127202', '2022-12-27', '04:04:00', 'JFK', '2022-12-28', '12:04:00', 'PVG', '499', 'canceled', 'Jet Blue', '1234'),
('127222', '2022-12-27', '06:17:00', 'jfk', '2022-12-27', '10:17:00', 'LAX', '300', 'ontime', 'Jet Blue', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `has`
--

CREATE TABLE `has` (
  `t_id` int(11) NOT NULL,
  `flight_num` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `operates`
--

CREATE TABLE `operates` (
  `flight_num` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `owns`
--

CREATE TABLE `owns` (
  `a_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `email` varchar(200) NOT NULL,
  `t_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`email`, `t_id`) VALUES
('kevsapathyjr@gmail.com', 1217),
('kjs10010@nyu.edu', 3345),
('yams@nyu.edu', 2323);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `email` varchar(20) NOT NULL,
  `flight_num` varchar(10) NOT NULL,
  `rating` decimal(1,0) DEFAULT NULL,
  `comment` varchar(50) DEFAULT NULL,
  `airline_name` varchar(200) NOT NULL,
  `d_date` date NOT NULL,
  `d_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `siteuser`
--

CREATE TABLE `siteuser` (
  `email` varchar(200) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  `type` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `siteuser`
--

INSERT INTO `siteuser` (`email`, `username`, `password`, `type`) VALUES
('ft@aol.com', '', '2d061102432defe9b7be67879b999c14', 2),
('gw@gmail.com', '', 'fb289605d3e6ba84fecb32b0aa2f83cb', 2),
('jpath@yahoo.com', 'p4th', 'b3f2530d3ba6772c25be428f6597e692', 1),
('kevsapathyjr@gmail.com', '', '4b10c03a722acb389b47f3b29cd2dcfb', 2);

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `t_id` int(11) NOT NULL,
  `airline_name` varchar(200) DEFAULT NULL,
  `sold_price` decimal(20,0) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `flight_num` varchar(200) DEFAULT NULL,
  `card_type` varchar(200) DEFAULT NULL,
  `card_number` int(20) DEFAULT NULL,
  `card_name` varchar(200) DEFAULT NULL,
  `card_exp` varchar(10) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_time` time DEFAULT NULL,
  `d_date` date DEFAULT NULL,
  `d_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`t_id`, `airline_name`, `sold_price`, `email`, `flight_num`, `card_type`, `card_number`, `card_name`, `card_exp`, `purchase_date`, `purchase_time`, `d_date`, `d_time`) VALUES
(1217, 'Jet Blue', '300', 'kevsapathyjr@gmail.com', '127222', 'VISA', 2147483647, 'Kelvin Sapathy', '2027-12-01', '2022-12-08', '08:43:52', '2022-12-27', '06:17:00'),
(2323, 'Jet Blue', '550', 'yams@nyu.edu', '127002', 'AMEX', 1234423434, 'Yams Gupta', '04/27', '2022-12-01', '00:00:01', '2022-12-27', '04:04:00'),
(3345, 'Jet Blue', '570', 'kjs10010@nyu.edu', '127202', 'VISA', 2147483647, 'Kelvin Sapathy', '12/27', '2022-12-01', '00:00:04', '2022-12-27', '04:04:00');

-- --------------------------------------------------------

--
-- Table structure for table `travels`
--

CREATE TABLE `travels` (
  `flight_num` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `works_at`
--

CREATE TABLE `works_at` (
  `username` varchar(20) NOT NULL,
  `airline_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `works_at`
--

INSERT INTO `works_at` (`username`, `airline_name`) VALUES
('bobsburger', 'Jet Blue'),
('p4th', 'Jet Blue');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airlinestaff`
--
ALTER TABLE `airlinestaff`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_num`);

--
-- Indexes for table `has`
--
ALTER TABLE `has`
  ADD PRIMARY KEY (`t_id`,`flight_num`),
  ADD KEY `flight_num` (`flight_num`);

--
-- Indexes for table `operates`
--
ALTER TABLE `operates`
  ADD PRIMARY KEY (`flight_num`,`name`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `owns`
--
ALTER TABLE `owns`
  ADD PRIMARY KEY (`a_id`,`name`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`email`,`t_id`),
  ADD KEY `t_id` (`t_id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`email`,`flight_num`),
  ADD KEY `flight_num` (`flight_num`);

--
-- Indexes for table `siteuser`
--
ALTER TABLE `siteuser`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`t_id`);

--
-- Indexes for table `travels`
--
ALTER TABLE `travels`
  ADD PRIMARY KEY (`flight_num`,`name`),
  ADD KEY `name` (`name`);

--
-- Indexes for table `works_at`
--
ALTER TABLE `works_at`
  ADD PRIMARY KEY (`username`,`airline_name`),
  ADD KEY `name` (`airline_name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `has`
--
ALTER TABLE `has`
  ADD CONSTRAINT `has_ibfk_1` FOREIGN KEY (`t_id`) REFERENCES `ticket` (`t_id`),
  ADD CONSTRAINT `has_ibfk_2` FOREIGN KEY (`flight_num`) REFERENCES `flight` (`flight_num`);

--
-- Constraints for table `operates`
--
ALTER TABLE `operates`
  ADD CONSTRAINT `operates_ibfk_1` FOREIGN KEY (`flight_num`) REFERENCES `flight` (`flight_num`),
  ADD CONSTRAINT `operates_ibfk_2` FOREIGN KEY (`name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `owns`
--
ALTER TABLE `owns`
  ADD CONSTRAINT `owns_ibfk_1` FOREIGN KEY (`a_id`) REFERENCES `airplane` (`a_id`),
  ADD CONSTRAINT `owns_ibfk_2` FOREIGN KEY (`name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`t_id`) REFERENCES `ticket` (`t_id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`flight_num`) REFERENCES `flight` (`flight_num`);

--
-- Constraints for table `travels`
--
ALTER TABLE `travels`
  ADD CONSTRAINT `travels_ibfk_1` FOREIGN KEY (`flight_num`) REFERENCES `flight` (`flight_num`),
  ADD CONSTRAINT `travels_ibfk_2` FOREIGN KEY (`name`) REFERENCES `airport` (`airport_name`);

--
-- Constraints for table `works_at`
--
ALTER TABLE `works_at`
  ADD CONSTRAINT `works_at_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airlinestaff` (`username`),
  ADD CONSTRAINT `works_at_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
