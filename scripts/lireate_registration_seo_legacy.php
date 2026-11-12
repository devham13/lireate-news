<?php
/**
 * Update the published fees article and two related legacy news rows.
 * php scripts/lireate_registration_seo_legacy.php <DOCROOT> [--apply <new-backup.json>]
 */
function lireate_registration_seo_plan($rows)
{
    $feeSlug = 'kakie_gosposhlinyi_neobxodimo_oplatit_za_registraciyu_tovarnogo_znaka';
    $guide = '/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026/';
    $links = array(
        'kak_zapolnit_zayavku_na_tovarnyiy_znak' =>
            'После заполнения формы сверяйтесь с <a href="' . $guide . '">порядком самостоятельной регистрации товарного знака</a>. В инструкции есть способы подачи, расчёт пошлин и этапы экспертизы.',
        'proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta' =>
            'Если проверка завершена, переходите к <a href="' . $guide . '">пошаговой инструкции по регистрации товарного знака</a>. Она поможет подготовить перечень товаров и услуг, подать заявку и рассчитать платежи.',
    );
    $feeBody = <<<'HTML'
<p id="poshliny-rospatenta">Базовые госпошлины за регистрацию товарного знака составляют <strong>35 000 ₽</strong> за один класс МКТУ с перечнем до 10 наименований и электронным свидетельством. Из них 17 000 ₽ платят на этапе подачи и экспертизы, 18 000 ₽ — после положительного решения Роспатента.</p>
<h2>Из чего складываются пошлины</h2>
<table>
<thead><tr><th scope="col">Действие</th><th scope="col">Пункт</th><th scope="col">Сумма и доплаты</th></tr></thead>
<tbody>
<tr><td>Регистрация заявки и формальная экспертиза</td><td>2.1</td><td>4 000 ₽ + 1 000 ₽ за каждый класс сверх первого.</td></tr>
<tr><td>Экспертиза обозначения по существу</td><td>2.4</td><td>13 000 ₽ + 2 500 ₽ за каждый класс сверх первого + 500 ₽ за каждое наименование сверх 10 отдельно в каждом классе.</td></tr>
<tr><td>Регистрация знака и электронное свидетельство</td><td>2.11</td><td>18 000 ₽ + 2 000 ₽ за каждый класс сверх пятого. Платёж после положительного решения.</td></tr>
<tr><td>Бумажное свидетельство по ходатайству</td><td>2.14</td><td>3 000 ₽ при необходимости.</td></tr>
</tbody>
</table>
<h2>Примеры расчёта</h2>
<ul>
<li>Два класса, до 10 наименований в каждом — 38 500 ₽.</li>
<li>Три класса, до 10 наименований в каждом — 42 000 ₽.</li>
<li>Один класс, 12 наименований — 36 000 ₽.</li>
</ul>
<p>Базовые ставки одинаковы при электронной и бумажной подаче. Оплата услуг бюро рассчитывается отдельно по договору. Сверяйте действующие суммы и реквизиты перед платежом в <a href="https://rospatent.gov.ru/ru/activities/dues/table">таблице пошлин Роспатента</a> или на <a href="https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-tovarnogo-znaka-znaka-obsluzhivaniya-kollektivnogo-znaka-i-vydacha-svidetelstv-na-tovarnyy-znak-znak-obsluzhivaniya-kollektivnyy-znak-ih-dublikatov">странице государственной услуги</a>.</p>
<p>Данные сверены 12 ноября 2026 года. Для подготовки заявки используйте <a href="/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026/">инструкцию по самостоятельной регистрации</a>. Состав сопровождения указан на <a href="/registraciya_tovarnogo_znaka/">странице услуги Лирейт</a>.</p>
HTML;
    $planned = array();
    foreach (array_merge(array($feeSlug), array_keys($links)) as $slug) {
        if (!isset($rows[$slug])) {
            throw new RuntimeException('Не найдена активная запись: ' . $slug);
        }
        $before = $rows[$slug];
        $after = $before;
        $body = (string) $before['full_story'];
        if ($slug === $feeSlug) {
            if (strpos($body, 'id="poshliny-rospatenta"') === false) {
                $pattern = '~<p\b[^>]*>\s*При регистрации товарного знака вам будет необходимо оплатить'
                    . '.*?<p\b[^>]*>\s*Ну и наконец, третья пошлина\b.*?</p>~su';
                $body = preg_replace_callback($pattern, function () use ($feeBody) {
                    return $feeBody;
                }, $body, 1, $count);
                if ($body === null || $count !== 1) {
                    throw new RuntimeException('Текст статьи о пошлинах изменился. Нужна сверка записи.');
                }
            }
            $after['seo_title'] = 'Госпошлины за регистрацию товарного знака: ставки и расчёт — Лирейт';
            $after['seo_description'] = 'Пошлины за регистрацию товарного знака в Роспатенте: 35 000 ₽ за базовый цикл, доплаты по МКТУ и примеры расчёта.';
        } elseif (strpos($body, $guide) === false) {
            $body = rtrim($body) . "\n<p>" . $links[$slug] . "</p>\n";
        }
        $after['full_story'] = $body;
        if ($after !== $before) {
            $planned[$slug] = array('before' => $before, 'after' => $after);
        }
    }
    return $planned;
}

function lireate_registration_seo_run($argv)
{
    $count = count($argv);
    if ($count !== 2 && !($count === 4 && $argv[2] === '--apply')) {
        throw new RuntimeException('Укажите DOCROOT и, для записи, --apply <новый-файл-бэкапа.json>.');
    }
    $config = rtrim($argv[1], '/') . '/data/db.php';
    if (!is_file($config)) {
        throw new RuntimeException('Файл настроек CMS не найден.');
    }
    require $config;
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    $db = new mysqli(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
    $db->set_charset('utf8mb4');
    $apply = $count === 4;
    if ($apply) {
        $db->begin_transaction();
    }
    try {
        $query = "SELECT id, seo_url, full_story, seo_title, seo_description FROM news WHERE active=1 AND seo_url IN ("
            . "'kakie_gosposhlinyi_neobxodimo_oplatit_za_registraciyu_tovarnogo_znaka',"
            . "'kak_zapolnit_zayavku_na_tovarnyiy_znak',"
            . "'proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta')";
        $result = $db->query($query . ($apply ? ' FOR UPDATE' : ''));
        $rows = array();
        while ($row = $result->fetch_assoc()) {
            if (isset($rows[$row['seo_url']])) {
                throw new RuntimeException('Обнаружены дублирующиеся URL в CMS.');
            }
            $rows[$row['seo_url']] = $row;
        }
        $planned = lireate_registration_seo_plan($rows);
        if ($apply && $planned) {
            $backup = json_encode(array_column($planned, 'before'), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
            if ($backup === false) {
                throw new RuntimeException('Не удалось сформировать бэкап.');
            }
            $previousMask = umask(0077);
            $handle = @fopen($argv[3], 'xb');
            umask($previousMask);
            if (!$handle) {
                throw new RuntimeException('Не удалось создать новый файл бэкапа.');
            }
            $written = fwrite($handle, $backup);
            fclose($handle);
            if ($written !== strlen($backup)) {
                throw new RuntimeException('Бэкап записан не полностью. База не изменена.');
            }
            $update = $db->prepare('UPDATE news SET full_story=?, seo_title=?, seo_description=? WHERE id=? AND seo_url=?');
            foreach ($planned as $change) {
                $row = $change['after'];
                $update->bind_param('sssis', $row['full_story'], $row['seo_title'], $row['seo_description'], $row['id'], $row['seo_url']);
                $update->execute();
                if ($update->affected_rows !== 1) {
                    throw new RuntimeException('Не удалось обновить ровно одну строку CMS.');
                }
            }
        }
        if ($apply) {
            $db->commit();
        }
        echo json_encode(array('applied' => $apply, 'slugs' => array_keys($planned)), JSON_UNESCAPED_UNICODE) . "\n";
    } catch (Exception $error) {
        if ($apply) {
            $db->rollback();
        }
        throw $error;
    }
}

if (PHP_SAPI === 'cli' && isset($_SERVER['SCRIPT_FILENAME']) && realpath($_SERVER['SCRIPT_FILENAME']) === __FILE__) {
    try {
        lireate_registration_seo_run($argv);
    } catch (mysqli_sql_exception $error) {
        fwrite(STDERR, 'Ошибка MySQL. Изменения не подтверждены. Код: ' . $error->getCode() . "\n");
        exit(1);
    } catch (Exception $error) {
        fwrite(STDERR, $error->getMessage() . "\n");
        exit(1);
    }
}
