<?php
/**
 * Главная: 3 последние статьи блога (карточки).
 */
if (!isset($db)) {
    return;
}
require_once __DIR__ . '/lireate-home-url.inc.php';
$_lx_home_blog_items = get_news($db, 'news', 3, 0, false);
if (empty($_lx_home_blog_items) || !is_array($_lx_home_blog_items)) {
    return;
}
?>
<div class="lireate-home-blog-cards" aria-label="Последние статьи блога">
<?php foreach ($_lx_home_blog_items as $_lx_item) :
    if (empty($_lx_item['seo_url'])) {
        continue;
    }
    $_lx_title = '';
    if (!empty($_lx_item['seo_title'])) {
        $_lx_title = trim((string) $_lx_item['seo_title']);
    }
    if ($_lx_title === '' && !empty($_lx_item['title'])) {
        $_lx_title = trim((string) $_lx_item['title']);
    }
    if (($_lx_title === '' || $_lx_title === '1') && isset($_lx_item['name'])) {
        $_lx_title = trim((string) $_lx_item['name']);
    }
    if ($_lx_title === '' || $_lx_title === '1') {
        continue;
    }
    $_lx_href = lireate_home_abs_url((string) $_lx_item['seo_url']);
    $_lx_date = '';
    $_lx_ts = 0;
    if (!empty($_lx_item['datetime'])) {
        $_lx_ts = strtotime((string) $_lx_item['datetime']);
        if ($_lx_ts) {
            $_lx_date = date('d.m.Y', $_lx_ts);
        }
    }
    ?>
  <article class="lireate-home-blog-card">
    <?php if ($_lx_date !== '') : ?>
    <time class="lireate-home-blog-card-date" datetime="<?php echo htmlspecialchars(date('Y-m-d', $_lx_ts), ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars($_lx_date, ENT_QUOTES, 'UTF-8'); ?></time>
    <?php endif; ?>
    <h3 class="lireate-home-blog-card-title">
      <a href="<?php echo htmlspecialchars($_lx_href, ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars($_lx_title, ENT_QUOTES, 'UTF-8'); ?></a>
    </h3>
    <a class="lireate-home-blog-card-more" href="<?php echo htmlspecialchars($_lx_href, ENT_QUOTES, 'UTF-8'); ?>">Читать</a>
  </article>
<?php endforeach; ?>
</div>
