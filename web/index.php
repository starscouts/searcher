<?php

$page = "home";

function process() {
    global $page;

    foreach ($_GET as $key => $value) {
        switch ($key) {
            case "type":
                if (!isset($_GET["q"])) {
                    $page = "bad";
                    return;
                }

                $page = match ($value) {
                    "all" => "results_overview",
                    "text" => "results_text",
                    "images" => "results_images",
                    "videos" => "results_videos",
                    "news" => "results_news",
                };
                break;

            case "q":
                if (!isset($_GET["type"])) {
                    $page = "results_overview";
                }
                break;

            case "safe":
                if (!isset($_GET["q"]) || ($value !== "off" && $value !== "moderate" && $value !== "strict")) {
                    $page = "bad";
                    return;
                }
                break;

            default:
                $page = "bad";
                return;
        }
    }
}

process();
require_once $_SERVER['DOCUMENT_ROOT'] . "/includes/pages/" . $page . ".php";
