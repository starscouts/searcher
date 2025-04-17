<div style="border-bottom: 1px solid rgba(0, 0, 0, .25); padding-top: 15px; padding-left: 75px; display: grid; grid-gap: 10px; grid-template-columns: max-content 1fr;">
    <img src="/logo.svg" style="width: 42px; height: 42px;" alt="">
    <div style="display: flex; align-items: center;">
        <input type="text" value="<?= str_replace('"', '&quot;', $_GET['q']) ?>">
    </div>
</div>
