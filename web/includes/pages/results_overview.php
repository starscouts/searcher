<?php require_once $_SERVER['DOCUMENT_ROOT'] . "/includes/templates/header.php";

$results = json_decode(file_get_contents("http://127.0.0.1:25190/overview?ss=" . rawurlencode($_GET["safe"] ?? "moderate") . "&q=" . rawurlencode($_GET["q"])), true);

?>
<?php require_once $_SERVER['DOCUMENT_ROOT'] . "/includes/templates/results.php"; ?>

<hr>
<pre><?= htmlentities(print_r($results, true)); ?></pre>
<?php require_once $_SERVER['DOCUMENT_ROOT'] . "/includes/templates/footer.php"; ?>
