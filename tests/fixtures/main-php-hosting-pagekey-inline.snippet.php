<?php
// Minimal php -l repro: live main.php ~382-386 (pagekey inside open <?php block)
// page_container
$temp = array('pagekey' => '8');
?>
<body>
<?php

    echo $temp['pagekey'];
    include('./template/parts/online.php');
?>
</body>
