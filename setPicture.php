<?php

$picture = $_GET['picture'];

exec("./python/interface_setPicture.py $picture",$output);
print_r($output);

?>
