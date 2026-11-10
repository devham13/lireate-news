<?php
/**
 * Замена тела db_result() в engine/func/function.php (PHP 5.6+).
 * Причина: mysqli_fetch_array() на false даёт warning/fatal в логах.
 * Не трогать data/db.php.
 */
function db_result($result)
{
    $res_array = array();
    if ($result === false || !($result instanceof mysqli_result)) {
        return $res_array;
    }
    $count = 0;
    while ($row = mysqli_fetch_array($result, MYSQLI_BOTH)) {
        $res_array[$count] = $row;
        $count++;
    }
    return $res_array;
}
