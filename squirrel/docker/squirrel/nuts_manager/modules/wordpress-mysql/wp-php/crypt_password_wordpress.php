<?php

// php check_password_admin_wordpress.php USER_PASSWORD WORDPRESS_DATABASE_USER WORDPRESS_DATABASE_PASSWORD MARIADB_HOST MARIADB_PORT_NUMBER WORDPRESS_DATABASE_NAME PATH_WP_INCLUDES
// UPDATE wp_users SET user_pass='$P$BB4kS2WrEJu4333566c15.' WHERE id=1;

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

function wp_hash_password( $password ) {
    global $wp_hasher;
 
    if ( empty( $wp_hasher ) ) {
        require_once($path_wp_includes . 'pluggable.php' );
        // By default, use the portable hash from phpass
        $wp_hasher = new PasswordHash( 8, true );
    }
 
    return $wp_hasher->HashPassword( trim( $password ) );
}

echo wp_hash_password($password);
?>
