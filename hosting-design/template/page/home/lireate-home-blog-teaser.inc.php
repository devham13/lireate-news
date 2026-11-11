<?php
/**
 * Главная: 3 последние статьи блога (карточки).
 * Подключается из template/main.php (home).
 */
if (!isset($db)) {
    return;
}
$_lx_home_blog_items = get_news($db, 'news', 3, 0, false);
if (empty($_lx_home_blog_items) || !is_array($_lx_home_blog_items)) {
    return;
}
$_lx_home_blog_prefix = isset($cit_in) ? (string) $cit_in : '';
?>
<div class="lireate-home-blog-cards" aria-label="Последние статьи блога">
<?php foreach ($_lx_home_blog_items as $_lx_item) :
    if (empty($_lx_item['seo_url'])) {
        continue;
    }
    $_lx_title = isset($_lx_item['title']) ? (string) $_lx_item['title'] : '';
    if ($_lx_title === '' && isset($_lx_item['name'])) {
        $_lx_title = (string) $_lx_item['name'];
    }
    $_lx_href = $_lx_home_blog_prefix . '/' . rawurlencode((string) $_lx_item['seo_url']);
    $_lx_excerpt = '';
    if (!empty($_lx_item['description'])) {
        $_lx_excerpt = (string) $_lx_item['description'];
    } elseif (!empty($_lx_item['short_story'])) {
        $_lx_excerpt = strip_tags((string) $_lx_item['short_story']);
    }
    if (function_exists('mb_substr') && mb_strlen($_lx_excerpt, 'UTF-8') > 140) {
        $_lx_excerpt = mb_substr($_lx_excerpt, 0, 137, 'UTF-8') . '…';
    } elseif (strlen($_lx_excerpt) > 140) {
        $_lx_excerpt = substr($_lx_excerpt, 0, 137) . '…';
    }
    ?>
  <article class="lireate-home-blog-card">
    <h3 class="lireate-home-blog-card-title">
      <a href="<?php echo htmlspecialchars($_lx_href, ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars($_lx_title, ENT_QUOTES, 'UTF-8'); ?></a>
    </h3>
    <?php if ($_lx_excerpt !== '') : ?>
    <p class="lireate-home-blog-card-excerpt"><?php echo htmlspecialchars($_lx_excerpt, ENT_QUOTES, 'UTF-8'); ?></p>
    <?php endif; ?>
    <a class="lireate-home-blog-card-more" href="<?php echo htmlspecialchars($_lx_href, ENT_QUOTES, 'UTF-8'); ?>">Читать</a>
  </article>
<?php endforeach; ?>
</div>
