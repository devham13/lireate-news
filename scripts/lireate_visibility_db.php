<?php
/** Targeted, reversible CMS maintenance. CLI only; never outputs article bodies or credentials. */
function lireate_visibility_link($body, $old, $new)
{
    return preg_replace_callback('~(<a\b[^>]*\bhref\s*=\s*)([\x22\x27])(.*?)\2~is',
        function ($m) use ($old, $new) {
            $url = html_entity_decode($m[3], ENT_QUOTES, 'UTF-8');
            $parts = parse_url($url);
            if ($parts === false || (isset($parts['host'])
                && !in_array(strtolower($parts['host']), array('lireate.ru', 'www.lireate.ru'), true))) {
                return $m[0];
            }
            if (!isset($parts['path']) || $parts['path'] !== $old) {
                return $m[0];
            }
            $suffix = (isset($parts['query']) ? '?' . $parts['query'] : '')
                . (isset($parts['fragment']) ? '#' . $parts['fragment'] : '');
            return $m[1] . $m[2] . htmlspecialchars($new . $suffix, ENT_QUOTES, 'UTF-8') . $m[2];
        }, $body);
}

function lireate_visibility_plan($rows, $config)
{
    $changes = array();
    foreach (array_merge($config['titles'], $config['links']) as $fix) {
        $slug = $fix['slug'];
        if (!isset($rows[$slug])) {
            throw new RuntimeException('Missing active article: ' . $slug);
        }
        if (!isset($changes[$slug])) {
            $changes[$slug] = array('before' => $rows[$slug], 'after' => $rows[$slug]);
        }
        $after = $changes[$slug]['after'];
        if (isset($fix['name'])) {
            foreach (array('name', 'seo_title') as $field) {
                if ($after[$field] !== $fix[$field] && $after[$field] !== $fix['expected_old']) {
                    throw new RuntimeException('Article changed; review required: ' . $slug . ' ' . $field);
                }
                $after[$field] = $fix[$field];
            }
        } else {
            $after['full_story'] = lireate_visibility_link($after['full_story'], $fix['old'], $fix['new']);
        }
        $changes[$slug]['after'] = $after;
    }
    foreach ($changes as $slug => $change) {
        if ($change['before'] === $change['after']) {
            unset($changes[$slug]);
        }
    }
    return $changes;
}

function lireate_visibility_update($db, $before, $after)
{
    $stmt = $db->prepare("UPDATE news SET name=?, seo_title=?, full_story=? WHERE id=? AND seo_url=?"
        . " AND BINARY COALESCE(name,'')=BINARY ? AND BINARY COALESCE(seo_title,'')=BINARY ?"
        . " AND BINARY COALESCE(full_story,'')=BINARY ?");
    $stmt->bind_param('sssissss', $after['name'], $after['seo_title'], $after['full_story'],
        $before['id'], $before['seo_url'], $before['name'], $before['seo_title'], $before['full_story']);
    $stmt->execute();
    $count = $stmt->affected_rows;
    $stmt->close();
    if ($count !== 1) {
        throw new RuntimeException('Concurrent article edit; update refused: ' . $before['seo_url']);
    }
}

function lireate_visibility_db_run($argv)
{
    if (count($argv) < 4 || !in_array($argv[1], array('plan', 'apply', 'restore'), true)) {
        throw new RuntimeException('Usage: plan|apply|restore DOCROOT CONFIG [NEW_BACKUP]');
    }
    $mode = $argv[1];
    $docroot = realpath($argv[2]);
    $config = json_decode(file_get_contents($argv[3]), true);
    if (!$docroot || !is_array($config) || empty($config['titles']) || empty($config['links'])) {
        throw new RuntimeException('Invalid docroot or maintenance config');
    }
    require $docroot . '/data/db.php';
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    $db = new mysqli(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
    $db->set_charset('utf8mb4');
    $slugs = array();
    foreach (array_merge($config['titles'], $config['links']) as $fix) {
        if (!preg_match('/^[a-z0-9_-]+$/D', $fix['slug'])) {
            throw new RuntimeException('Invalid configured slug');
        }
        $slugs[$fix['slug']] = true;
    }
    $changed = array();
    $applied = array();
    if ($mode !== 'plan') {
        $db->begin_transaction();
    }
    try {
        if ($mode === 'restore') {
            if (count($argv) !== 5) { throw new RuntimeException('Backup required'); }
            $backup = json_decode(file_get_contents($argv[4]), true);
            if (!isset($backup['version']) || $backup['version'] !== $config['version']) {
                throw new RuntimeException('Unexpected backup version');
            }
            foreach ($backup['changes'] as $slug => $change) {
                if (!isset($slugs[$slug])) { throw new RuntimeException('Unexpected backup article'); }
                lireate_visibility_update($db, $change['after'], $change['before']);
                $changed[] = $slug;
            }
        } else {
            $quoted = array();
            foreach (array_keys($slugs) as $slug) { $quoted[] = "'" . $db->real_escape_string($slug) . "'"; }
            $sql = "SELECT id,seo_url,COALESCE(name,'') AS name,COALESCE(seo_title,'') AS seo_title,"
                . "COALESCE(full_story,'') AS full_story FROM news WHERE active=1 AND seo_url IN ("
                . implode(',', $quoted) . ')' . ($mode === 'apply' ? ' FOR UPDATE' : '');
            $result = $db->query($sql);
            $rows = array();
            while ($row = $result->fetch_assoc()) {
                if (isset($rows[$row['seo_url']])) { throw new RuntimeException('Duplicate active article'); }
                $rows[$row['seo_url']] = $row;
            }
            $changes = lireate_visibility_plan($rows, $config);
            $changed = array_keys($changes);
            if ($mode === 'apply' && $changes) {
                if (count($argv) !== 5 || !realpath(dirname($argv[4]))
                    || strpos(realpath(dirname($argv[4])) . '/', $docroot . '/') === 0) {
                    throw new RuntimeException('A new backup outside docroot is required');
                }
                $data = json_encode(array('version' => $config['version'], 'changes' => $changes), JSON_UNESCAPED_UNICODE);
                if ($data === false) { throw new RuntimeException('Backup encoding failed'); }
                $mask = umask(0077);
                $stream = fopen($argv[4], 'xb');
                umask($mask);
                if (!$stream) { throw new RuntimeException('Cannot create new backup'); }
                $written = fwrite($stream, $data);
                $closed = fclose($stream);
                if ($written !== strlen($data) || !$closed) { throw new RuntimeException('Incomplete backup'); }
                foreach ($changes as $slug => $change) {
                    lireate_visibility_update($db, $change['before'], $change['after']);
                    $applied[] = $change;
                }
            }
        }
        if ($mode !== 'plan') { $db->commit(); }
        $db->close();
        return array('ok' => true, 'mode' => $mode, 'changed_slugs' => $changed);
    } catch (Exception $error) {
        if ($mode !== 'plan') {
            $db->rollback();
            // MyISAM does not roll back: restore only rows still matching our writes.
            foreach (array_reverse($applied) as $change) {
                try { lireate_visibility_update($db, $change['after'], $change['before']); }
                catch (Exception $ignored) { /* InnoDB already rolled back, or a newer edit must be preserved. */ }
            }
        }
        throw $error;
    }
}

if (PHP_SAPI === 'cli' && realpath($_SERVER['SCRIPT_FILENAME']) === __FILE__) {
    try {
        echo json_encode(lireate_visibility_db_run($argv), JSON_UNESCAPED_UNICODE) . "\n";
    } catch (mysqli_sql_exception $error) {
        fwrite(STDERR, 'CMS maintenance SQL error; code: ' . $error->getCode() . "\n");
        exit(1);
    } catch (Exception $error) {
        fwrite(STDERR, $error->getMessage() . "\n");
        exit(1);
    }
}
