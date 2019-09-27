<?php

// php check_password_admin_wordpress.php USER_PASSWORD WORDPRESS_DATABASE_USER WORDPRESS_DATABASE_PASSWORD MARIADB_HOST MARIADB_PORT_NUMBER WORDPRESS_DATABASE_NAME PATH_WP_INCLUDES

// Arguments
var_dump($argv);

$password = $argv[1];
$db_user = getenv($argv[2]);
$db_pass = getenv($argv[3]);
$db_host = getenv($argv[4]);
$db_port = getenv($argv[5]);
$db_database = getenv($argv[6]);
$path_wp_includes = getenv($argv[7]);

// include_once(dirname(dirname(dirname(__FILE__))) . DIRECTORY_SEPARATOR . "wp-includes" . DIRECTORY_SEPARATOR . "class-phpass.php");
include_once($path_wp_includes . "class-phpass.php");

$conn = new mysqli($db_host,$db_user,$db_pass,$db_database,$db_port);

//$result_query = mysqli_query($conn, "SELECT user_pass FROM wp_users WHERE id=1;");
$result_query = $conn->query("SELECT user_pass FROM wp_users WHERE id=1;");
$row = mysqli_fetch_assoc($result_query);

$wp_hasher = new PasswordHash(8, true);
$check = $wp_hasher->CheckPassword($password, $row['user_pass']);
if($check) {
   echo "0";
} else {
   echo "1";
}

?>
