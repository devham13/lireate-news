	<?php
	$_lireate_seo_head = dirname(__DIR__) . '/data/lireate-seo-head.inc.php';
	if (is_file($_lireate_seo_head)) {
		require_once $_lireate_seo_head;
		lireate_seo_render_head_tags();
	}
	?>
